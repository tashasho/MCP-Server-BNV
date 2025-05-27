import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

class GoogleSheetsClient:
    def __init__(self):
        self.scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        self.creds_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
        self.spreadsheet_id = os.getenv('SPREADSHEET_ID')
        self.client = self._authenticate()

    def _authenticate(self) -> gspread.Client:
        """Authenticate with Google Sheets API"""
        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                self.creds_path, self.scope)
            return gspread.authorize(creds)
        except Exception as e:
            raise Exception(f"Authentication failed: {str(e)}")

    def get_incubators_data(self) -> pd.DataFrame:
        """Fetch incubators data from the Google Sheet"""
        try:
            sheet = self.client.open_by_key(self.spreadsheet_id).sheet1
            data = sheet.get_all_records()
            return pd.DataFrame(data)
        except Exception as e:
            raise Exception(f"Failed to fetch incubators data: {str(e)}")

    def update_portfolio_data(self, incubator_name: str, portfolio_data: List[Dict]):
        """Update portfolio data for a specific incubator"""
        try:
            # Create a new worksheet for the incubator if it doesn't exist
            workbook = self.client.open_by_key(self.spreadsheet_id)
            try:
                worksheet = workbook.worksheet(f"Portfolio_{incubator_name}")
            except:
                worksheet = workbook.add_worksheet(
                    f"Portfolio_{incubator_name}", 
                    rows=1000, 
                    cols=20
                )
            
            # Convert portfolio data to DataFrame and update sheet
            df = pd.DataFrame(portfolio_data)
            worksheet.clear()
            worksheet.update([df.columns.values.tolist()] + df.values.tolist())
            
        except Exception as e:
            raise Exception(f"Failed to update portfolio data: {str(e)}")

    def get_portfolio_data(self, incubator_name: str) -> pd.DataFrame:
        """Fetch portfolio data for a specific incubator"""
        try:
            worksheet = self.client.open_by_key(self.spreadsheet_id).worksheet(
                f"Portfolio_{incubator_name}")
            data = worksheet.get_all_records()
            return pd.DataFrame(data)
        except Exception as e:
            raise Exception(f"Failed to fetch portfolio data: {str(e)}") 