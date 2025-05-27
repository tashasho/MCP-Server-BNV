from typing import Dict, List, Union
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class CompanyScorer:
    def __init__(self):
        self.criteria_weights = {
            'team': 0.35,
            'business': 0.30,
            'technology': 0.20,
            'impact': 0.15
        }
        
        self.team_indicators = {
            'education': [
                'IIT', 'IIM', 'Harvard', 'Stanford', 'MIT', 'top university',
                'prestigious institution'
            ],
            'experience': [
                'years experience', 'worked at', 'former', 'led', 'founded',
                'serial entrepreneur', 'leadership'
            ],
            'skills': [
                'technical expertise', 'business acumen', 'visionary',
                'communication skills', 'team management'
            ]
        }
        
        self.business_indicators = {
            'market_size': [
                'large market', 'billion dollar', 'massive opportunity',
                'growing market', 'scale', 'expansion'
            ],
            'growth_potential': [
                'rapid growth', 'scalable', 'exponential', 'traction',
                'revenue growth'
            ],
            'innovation': [
                'unique', 'innovative', 'disrupting', 'revolutionary',
                'breakthrough'
            ]
        }
        
        self.technology_indicators = {
            'innovation': [
                'patent', 'proprietary', 'novel technology', 'breakthrough',
                'cutting edge'
            ],
            'feasibility': [
                'proven', 'validated', 'working product', 'prototype',
                'production ready'
            ],
            'competitive_advantage': [
                'barrier to entry', 'competitive advantage', 'unique technology',
                '10x better', 'superior'
            ]
        }
        
        self.impact_indicators = {
            'social_impact': [
                'social impact', 'sustainability', 'environmental',
                'community', 'welfare'
            ],
            'esg': [
                'ESG', 'governance', 'sustainable', 'responsible',
                'ethical'
            ]
        }

    def score_company(self, company_data: Dict) -> Dict[str, Union[float, Dict[str, float]]]:
        """Score a company based on all criteria"""
        scores = {}
        
        # Calculate individual component scores
        scores['team'] = self._score_team(company_data)
        scores['business'] = self._score_business(company_data)
        scores['technology'] = self._score_technology(company_data)
        scores['impact'] = self._score_impact(company_data)
        
        # Calculate weighted total score
        total_score = sum(
            scores[component] * weight
            for component, weight in self.criteria_weights.items()
        )
        
        return {
            'total_score': total_score,
            'component_scores': scores
        }

    def _calculate_indicator_score(self, text: str, indicators: List[str]) -> float:
        """Calculate score based on presence of indicators in text"""
        text = text.lower()
        matches = sum(1 for indicator in indicators if indicator.lower() in text)
        return min(matches / len(indicators), 1.0)

    def _score_team(self, company_data: Dict) -> float:
        """Score the team based on education, experience, and skills"""
        text = f"{company_data.get('founders', '')} {company_data.get('description', '')}"
        
        education_score = self._calculate_indicator_score(text, self.team_indicators['education'])
        experience_score = self._calculate_indicator_score(text, self.team_indicators['experience'])
        skills_score = self._calculate_indicator_score(text, self.team_indicators['skills'])
        
        return (education_score + experience_score + skills_score) / 3

    def _score_business(self, company_data: Dict) -> float:
        """Score the business potential"""
        text = f"{company_data.get('description', '')} {company_data.get('usp', '')}"
        
        market_score = self._calculate_indicator_score(text, self.business_indicators['market_size'])
        growth_score = self._calculate_indicator_score(text, self.business_indicators['growth_potential'])
        innovation_score = self._calculate_indicator_score(text, self.business_indicators['innovation'])
        
        return (market_score + growth_score + innovation_score) / 3

    def _score_technology(self, company_data: Dict) -> float:
        """Score the technology aspects"""
        text = f"{company_data.get('solution', '')} {company_data.get('usp', '')}"
        
        innovation_score = self._calculate_indicator_score(text, self.technology_indicators['innovation'])
        feasibility_score = self._calculate_indicator_score(text, self.technology_indicators['feasibility'])
        advantage_score = self._calculate_indicator_score(text, self.technology_indicators['competitive_advantage'])
        
        return (innovation_score + feasibility_score + advantage_score) / 3

    def _score_impact(self, company_data: Dict) -> float:
        """Score the impact and ESG aspects"""
        text = f"{company_data.get('description', '')} {company_data.get('problem', '')} {company_data.get('solution', '')}"
        
        impact_score = self._calculate_indicator_score(text, self.impact_indicators['social_impact'])
        esg_score = self._calculate_indicator_score(text, self.impact_indicators['esg'])
        
        return (impact_score + esg_score) / 2

    def calculate_thesis_relevance(self, company_data: Dict, thesis_text: str) -> float:
        """Calculate relevance score based on investment thesis"""
        company_text = f"{company_data.get('description', '')} {company_data.get('problem', '')} {company_data.get('solution', '')} {company_data.get('usp', '')}"
        
        # Create TF-IDF vectors
        vectorizer = TfidfVectorizer()
        try:
            tfidf_matrix = vectorizer.fit_transform([thesis_text, company_text])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except:
            return 0.0 