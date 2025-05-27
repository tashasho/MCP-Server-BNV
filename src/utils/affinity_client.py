import os
from typing import List, Dict
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

class AffinityClient:
    def __init__(self):
        self.api_key = os.getenv('AFFINITY_API_KEY')
        self.base_url = "https://api.affinity.co/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Initialize list IDs for different entity types
        self.incubators_list_id = os.getenv('AFFINITY_INCUBATORS_LIST_ID')
        self.portfolio_list_id = os.getenv('AFFINITY_PORTFOLIO_LIST_ID')

    def get_incubators_data(self) -> pd.DataFrame:
        """Fetch incubators data from Affinity"""
        try:
            url = f"{self.base_url}/lists/{self.incubators_list_id}/list-entries"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            # Extract relevant fields from response
            incubators = []
            for entry in response.json():
                incubator = {
                    'name': entry.get('name', ''),
                    'portfolio_url': self._get_field_value(entry, 'portfolio_url'),
                    'location': self._get_field_value(entry, 'location'),
                    'focus_areas': self._get_field_value(entry, 'focus_areas'),
                    'status': entry.get('status', '')
                }
                incubators.append(incubator)
            
            return pd.DataFrame(incubators)
            
        except Exception as e:
            raise Exception(f"Failed to fetch incubators data: {str(e)}")

    def update_portfolio_data(self, incubator_name: str, portfolio_data: List[Dict]):
        """Update portfolio company data in Affinity"""
        try:
            # Create a new list for the incubator's portfolio if it doesn't exist
            list_name = f"Portfolio_{incubator_name}"
            portfolio_list_id = self._get_or_create_list(list_name)
            
            # Process each company
            for company in portfolio_data:
                self._create_or_update_company(portfolio_list_id, company)
                
        except Exception as e:
            raise Exception(f"Failed to update portfolio data: {str(e)}")

    def get_portfolio_data(self, incubator_name: str) -> pd.DataFrame:
        """Fetch portfolio data for a specific incubator"""
        try:
            # Get the list ID for this incubator's portfolio
            list_name = f"Portfolio_{incubator_name}"
            list_id = self._get_list_id_by_name(list_name)
            
            if not list_id:
                return pd.DataFrame()  # Return empty DataFrame if list doesn't exist
            
            # Fetch all companies in this list
            url = f"{self.base_url}/lists/{list_id}/list-entries"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            # Extract company data
            companies = []
            for entry in response.json():
                company = {
                    'name': entry.get('name', ''),
                    'description': self._get_field_value(entry, 'description'),
                    'founders': self._get_field_value(entry, 'founders'),
                    'problem': self._get_field_value(entry, 'problem'),
                    'solution': self._get_field_value(entry, 'solution'),
                    'usp': self._get_field_value(entry, 'usp'),
                    'sectors': self._get_field_value(entry, 'sectors'),
                }
                companies.append(company)
            
            return pd.DataFrame(companies)
            
        except Exception as e:
            raise Exception(f"Failed to fetch portfolio data: {str(e)}")

    def _get_or_create_list(self, list_name: str) -> str:
        """Get or create a list in Affinity"""
        list_id = self._get_list_id_by_name(list_name)
        if list_id:
            return list_id
            
        # Create new list
        url = f"{self.base_url}/lists"
        response = requests.post(
            url,
            headers=self.headers,
            json={"name": list_name}
        )
        response.raise_for_status()
        return response.json()['id']

    def _get_list_id_by_name(self, list_name: str) -> str:
        """Get list ID by name"""
        url = f"{self.base_url}/lists"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        for list_info in response.json():
            if list_info['name'] == list_name:
                return list_info['id']
        return None

    def _create_or_update_company(self, list_id: str, company_data: Dict):
        """Create or update a company entry in Affinity"""
        # Check if company exists
        url = f"{self.base_url}/lists/{list_id}/list-entries"
        params = {"term": company_data['name']}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        
        existing_entries = response.json()
        
        if existing_entries:
            # Update existing company
            entry_id = existing_entries[0]['id']
            url = f"{self.base_url}/lists/{list_id}/list-entries/{entry_id}"
            requests.put(
                url,
                headers=self.headers,
                json=self._prepare_company_data(company_data)
            )
        else:
            # Create new company
            requests.post(
                url,
                headers=self.headers,
                json=self._prepare_company_data(company_data)
            )

    def _prepare_company_data(self, company_data: Dict) -> Dict:
        """Prepare company data for Affinity API"""
        return {
            "name": company_data['name'],
            "fields": {
                "description": company_data.get('description', ''),
                "founders": company_data.get('founders', ''),
                "problem": company_data.get('problem', ''),
                "solution": company_data.get('solution', ''),
                "usp": company_data.get('usp', ''),
                "sectors": company_data.get('sectors', [])
            }
        }

    def _get_field_value(self, entry: Dict, field_name: str) -> str:
        """Helper method to get field value from Affinity entry"""
        fields = entry.get('fields', {})
        return fields.get(field_name, '') 