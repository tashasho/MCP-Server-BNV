import os
from typing import Dict, List
import requests
from datetime import datetime, timedelta
import json
from nltk.tokenize import sent_tokenize
import pandas as pd

class MarketIntelligence:
    def __init__(self):
        self.news_api_key = os.getenv('NEWS_API_KEY')
        self.twitter_bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        self.crunchbase_api_key = os.getenv('CRUNCHBASE_API_KEY')
        
        # Load sector keywords and trends to monitor
        self.monitored_sectors = {
            'ai': ['artificial intelligence', 'machine learning', 'deep learning', 'AI'],
            'fintech': ['financial technology', 'payments', 'banking', 'defi'],
            'healthtech': ['digital health', 'biotech', 'healthcare', 'medtech'],
            'climate': ['climate tech', 'clean energy', 'sustainability', 'carbon']
        }

    async def gather_market_insights(self) -> Dict:
        """Gather market insights from various sources"""
        insights = {
            'news': await self._fetch_news(),
            'social_trends': await self._fetch_social_trends(),
            'funding_data': await self._fetch_funding_data(),
            'market_trends': await self._analyze_market_trends()
        }
        return insights

    async def _fetch_news(self) -> List[Dict]:
        """Fetch relevant news articles"""
        news_items = []
        
        for sector, keywords in self.monitored_sectors.items():
            for keyword in keywords:
                url = f"https://newsapi.org/v2/everything"
                params = {
                    'q': keyword,
                    'from': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
                    'sortBy': 'relevancy',
                    'apiKey': self.news_api_key
                }
                
                try:
                    response = requests.get(url, params=params)
                    response.raise_for_status()
                    articles = response.json().get('articles', [])
                    
                    for article in articles:
                        news_items.append({
                            'sector': sector,
                            'keyword': keyword,
                            'title': article['title'],
                            'description': article['description'],
                            'url': article['url'],
                            'published_at': article['publishedAt'],
                            'source': article['source']['name']
                        })
                except Exception as e:
                    print(f"Error fetching news for {keyword}: {str(e)}")
        
        return news_items

    async def _fetch_social_trends(self) -> List[Dict]:
        """Fetch relevant social media trends"""
        trends = []
        
        # Twitter API v2 endpoint
        url = "https://api.twitter.com/2/tweets/search/recent"
        headers = {
            "Authorization": f"Bearer {self.twitter_bearer_token}"
        }
        
        for sector, keywords in self.monitored_sectors.items():
            query = ' OR '.join(keywords)
            params = {
                'query': query,
                'tweet.fields': 'public_metrics,created_at',
                'max_results': 100
            }
            
            try:
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()
                tweets = response.json().get('data', [])
                
                for tweet in tweets:
                    trends.append({
                        'sector': sector,
                        'content': tweet['text'],
                        'engagement': tweet['public_metrics'],
                        'created_at': tweet['created_at']
                    })
            except Exception as e:
                print(f"Error fetching social trends for {sector}: {str(e)}")
        
        return trends

    async def _fetch_funding_data(self) -> List[Dict]:
        """Fetch recent funding data"""
        funding_rounds = []
        
        # Crunchbase API endpoint
        url = "https://api.crunchbase.com/v3.1/funding-rounds"
        headers = {
            "Authorization": f"Bearer {self.crunchbase_api_key}"
        }
        params = {
            'updated_since': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
            'sort_order': 'created_at DESC'
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            rounds = response.json().get('data', {}).get('items', [])
            
            for round_data in rounds:
                funding_rounds.append({
                    'company_name': round_data['relationships']['organization']['properties']['name'],
                    'amount': round_data['properties']['money_raised_usd'],
                    'series': round_data['properties']['series'],
                    'announced_on': round_data['properties']['announced_on'],
                    'investors': [inv['properties']['name'] for inv in round_data['relationships']['investors']]
                })
        except Exception as e:
            print(f"Error fetching funding data: {str(e)}")
        
        return funding_rounds

    async def _analyze_market_trends(self) -> Dict:
        """Analyze market trends from collected data"""
        trends = {
            'sector_momentum': {},
            'emerging_topics': {},
            'investment_patterns': {}
        }
        
        # Calculate sector momentum
        news_df = pd.DataFrame(await self._fetch_news())
        if not news_df.empty:
            sector_counts = news_df['sector'].value_counts()
            for sector in sector_counts.index:
                trends['sector_momentum'][sector] = {
                    'news_volume': int(sector_counts[sector]),
                    'trend': self._calculate_trend(sector)
                }
        
        # Analyze funding patterns
        funding_df = pd.DataFrame(await self._fetch_funding_data())
        if not funding_df.empty:
            trends['investment_patterns'] = {
                'average_round_size': funding_df['amount'].mean(),
                'most_active_investors': funding_df['investors'].explode().value_counts().head(5).to_dict(),
                'stage_distribution': funding_df['series'].value_counts().to_dict()
            }
        
        return trends

    def _calculate_trend(self, sector: str) -> str:
        """Calculate trend direction for a sector"""
        # Implement trend calculation logic
        # This could compare current volume with historical averages
        return "stable"  # placeholder

    async def get_company_insights(self, company_name: str) -> Dict:
        """Get comprehensive insights for a specific company"""
        insights = {
            'news': await self._fetch_company_news(company_name),
            'social_mentions': await self._fetch_company_social(company_name),
            'competitors': await self._identify_competitors(company_name),
            'market_position': await self._analyze_market_position(company_name)
        }
        return insights

    async def _fetch_company_news(self, company_name: str) -> List[Dict]:
        """Fetch news specific to a company"""
        # Implementation similar to _fetch_news but focused on company
        return []

    async def _fetch_company_social(self, company_name: str) -> List[Dict]:
        """Fetch social media mentions of a company"""
        # Implementation similar to _fetch_social_trends but focused on company
        return []

    async def _identify_competitors(self, company_name: str) -> List[Dict]:
        """Identify potential competitors"""
        # Implement competitor identification logic
        return []

    async def _analyze_market_position(self, company_name: str) -> Dict:
        """Analyze company's market position"""
        # Implement market position analysis
        return {} 