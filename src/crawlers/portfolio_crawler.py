from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import pandas as pd
from typing import List, Dict
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

class PortfolioCrawler:
    def __init__(self):
        self.setup_selenium()
        self.sector_keywords = {
            'climate_tech': ['climate', 'renewable', 'sustainability', 'clean energy', 'carbon'],
            'health_tech': ['healthcare', 'medical', 'biotech', 'health', 'pharma'],
            'ai': ['artificial intelligence', 'machine learning', 'deep learning', 'neural network'],
            'saas': ['software service', 'cloud', 'platform', 'subscription'],
            # Add more sectors and keywords as needed
        }

    def setup_selenium(self):
        """Setup Selenium WebDriver with Chrome"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

    def extract_portfolio_data(self, url: str) -> List[Dict]:
        """Extract portfolio company data from a given URL"""
        try:
            self.driver.get(url)
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # This is a basic implementation - you'll need to customize the selectors
            # based on the specific website structure
            companies = []
            
            # Example: finding company cards/sections
            company_elements = soup.find_all('div', class_='company-card')
            
            for element in company_elements:
                company_data = {
                    'name': self._extract_text(element.find('h2')),
                    'description': self._extract_text(element.find('p', class_='description')),
                    'founders': self._extract_text(element.find('div', class_='founders')),
                    'problem': self._extract_text(element.find('div', class_='problem')),
                    'solution': self._extract_text(element.find('div', class_='solution')),
                    'usp': self._extract_text(element.find('div', class_='usp')),
                }
                
                # Add sector tags
                company_data.update(self._identify_sectors(
                    f"{company_data['description']} {company_data['problem']} {company_data['solution']}"
                ))
                
                companies.append(company_data)
            
            return companies
            
        except Exception as e:
            print(f"Error crawling {url}: {str(e)}")
            return []

    def _extract_text(self, element) -> str:
        """Safely extract text from a BeautifulSoup element"""
        return element.get_text(strip=True) if element else ""

    def _identify_sectors(self, text: str) -> Dict[str, bool]:
        """Identify relevant sectors based on text content"""
        text = text.lower()
        sectors = {}
        
        for sector, keywords in self.sector_keywords.items():
            sectors[sector] = any(keyword.lower() in text for keyword in keywords)
        
        return sectors

    def close(self):
        """Close the Selenium WebDriver"""
        self.driver.quit()

    def __del__(self):
        """Destructor to ensure WebDriver is closed"""
        try:
            self.close()
        except:
            pass 