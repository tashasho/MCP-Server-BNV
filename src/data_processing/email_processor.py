import email
import imaplib
import os
from typing import Dict, List
from datetime import datetime, timedelta
import re
from email.utils import parseaddr
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

class EmailProcessor:
    def __init__(self):
        self.email_server = os.getenv('EMAIL_SERVER', 'imap.gmail.com')
        self.email = os.getenv('EMAIL_ADDRESS')
        self.password = os.getenv('EMAIL_PASSWORD')
        
        # Download required NLTK data
        nltk.download('punkt')
        nltk.download('stopwords')
        
        self.startup_indicators = [
            'startup', 'company', 'venture', 'founding', 'raised',
            'seed', 'series', 'pre-seed', 'angel'
        ]
        
        self.funding_stages = [
            'pre-seed', 'seed', 'series a', 'series b', 'series c',
            'growth', 'late stage'
        ]

    def process_daily_dealflow(self) -> List[Dict]:
        """Process last 24 hours of emails for deal flow"""
        deals = []
        
        # Connect to email server
        mail = imaplib.IMAP4_SSL(self.email_server)
        mail.login(self.email, self.password)
        mail.select('inbox')
        
        # Search for emails from last 24 hours
        date = (datetime.now() - timedelta(days=1)).strftime("%d-%b-%Y")
        _, messages = mail.search(None, f'(SINCE {date})')
        
        for msg_id in messages[0].split():
            _, msg_data = mail.fetch(msg_id, '(RFC822)')
            email_body = msg_data[0][1]
            email_message = email.message_from_bytes(email_body)
            
            # Process email content
            deal = self._extract_deal_info(email_message)
            if deal:
                deals.append(deal)
        
        mail.close()
        mail.logout()
        
        return deals

    def _extract_deal_info(self, email_message) -> Dict:
        """Extract relevant deal information from email"""
        subject = email_message['subject']
        sender = parseaddr(email_message['from'])[1]
        
        # Get email body
        body = ""
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = email_message.get_payload(decode=True).decode()
        
        # Skip if no startup indicators found
        if not any(indicator in body.lower() for indicator in self.startup_indicators):
            return None
        
        # Extract information
        company_name = self._extract_company_name(subject, body)
        if not company_name:
            return None
            
        return {
            'company_name': company_name,
            'sender': sender,
            'date_received': email_message['date'],
            'subject': subject,
            'funding_stage': self._extract_funding_stage(body),
            'sectors': self._extract_sectors(body),
            'team_info': self._extract_team_info(body),
            'warm_intro': self._is_warm_intro(body),
            'raw_content': body
        }

    def _extract_company_name(self, subject: str, body: str) -> str:
        """Extract company name from email"""
        # Try to find company name in common patterns
        patterns = [
            r'(?i)introducing\s+([A-Z][A-Za-z0-9]+)',
            r'(?i)company:\s+([A-Z][A-Za-z0-9]+)',
            r'(?i)startup:\s+([A-Z][A-Za-z0-9]+)',
            r'(?i)([A-Z][A-Za-z0-9]+)\s+is raising'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, subject + " " + body)
            if match:
                return match.group(1)
        
        return None

    def _extract_funding_stage(self, text: str) -> str:
        """Extract funding stage from text"""
        text = text.lower()
        for stage in self.funding_stages:
            if stage in text:
                return stage
        return 'unknown'

    def _extract_sectors(self, text: str) -> List[str]:
        """Extract sector information from text"""
        sectors = []
        # Add your sector extraction logic here
        # This could use keyword matching or more sophisticated NLP
        return sectors

    def _extract_team_info(self, text: str) -> Dict:
        """Extract team information from text"""
        team_info = {
            'founders': [],
            'background': [],
            'previous_companies': []
        }
        # Add your team information extraction logic here
        return team_info

    def _is_warm_intro(self, text: str) -> bool:
        """Determine if this is a warm introduction"""
        warm_indicators = [
            'introducing you to',
            'wanted to connect you with',
            'thought you might be interested in',
            'recommended I reach out',
            'mutual connection'
        ]
        
        text = text.lower()
        return any(indicator in text for indicator in warm_indicators) 