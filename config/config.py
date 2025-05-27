import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Google Sheets Configuration
    GOOGLE_SHEETS_CREDENTIALS = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
    SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
    
    # Server Configuration
    HOST = "0.0.0.0"
    PORT = int(os.getenv('PORT', '8000'))
    
    # Crawler Configuration
    CRAWLER_TIMEOUT = 30  # seconds
    MAX_RETRIES = 3
    
    # Scoring Configuration
    MINIMUM_SCORE_THRESHOLD = 0.5
    THESIS_RELEVANCE_WEIGHT = 0.4
    
    # Sector Keywords (can be extended)
    SECTOR_KEYWORDS = {
        'climate_tech': [
            'climate', 'renewable', 'sustainability', 'clean energy',
            'carbon', 'environmental', 'green tech'
        ],
        'health_tech': [
            'healthcare', 'medical', 'biotech', 'health', 'pharma',
            'diagnostics', 'telemedicine'
        ],
        'ai': [
            'artificial intelligence', 'machine learning', 'deep learning',
            'neural network', 'AI', 'NLP', 'computer vision'
        ],
        'saas': [
            'software service', 'cloud', 'platform', 'subscription',
            'enterprise software', 'B2B software'
        ],
        'fintech': [
            'financial technology', 'payments', 'banking', 'insurance',
            'blockchain', 'cryptocurrency'
        ],
        'edtech': [
            'education technology', 'learning platform', 'e-learning',
            'online education', 'educational'
        ]
    }
    
    # Investment Criteria Weights
    CRITERIA_WEIGHTS = {
        'team': 0.35,
        'business': 0.30,
        'technology': 0.20,
        'impact': 0.15
    }
    
    # Team Evaluation Criteria
    TEAM_CRITERIA = {
        'education': {
            'weight': 0.3,
            'keywords': [
                'IIT', 'IIM', 'Harvard', 'Stanford', 'MIT',
                'top university', 'prestigious institution'
            ]
        },
        'experience': {
            'weight': 0.4,
            'keywords': [
                'years experience', 'worked at', 'former', 'led',
                'founded', 'serial entrepreneur', 'leadership'
            ]
        },
        'skills': {
            'weight': 0.3,
            'keywords': [
                'technical expertise', 'business acumen', 'visionary',
                'communication skills', 'team management'
            ]
        }
    }
    
    # Business Evaluation Criteria
    BUSINESS_CRITERIA = {
        'market_size': {
            'weight': 0.4,
            'keywords': [
                'large market', 'billion dollar', 'massive opportunity',
                'growing market', 'scale', 'expansion'
            ]
        },
        'growth_potential': {
            'weight': 0.3,
            'keywords': [
                'rapid growth', 'scalable', 'exponential', 'traction',
                'revenue growth'
            ]
        },
        'innovation': {
            'weight': 0.3,
            'keywords': [
                'unique', 'innovative', 'disrupting', 'revolutionary',
                'breakthrough'
            ]
        }
    }
    
    # Technology Evaluation Criteria
    TECHNOLOGY_CRITERIA = {
        'innovation': {
            'weight': 0.4,
            'keywords': [
                'patent', 'proprietary', 'novel technology',
                'breakthrough', 'cutting edge'
            ]
        },
        'feasibility': {
            'weight': 0.3,
            'keywords': [
                'proven', 'validated', 'working product', 'prototype',
                'production ready'
            ]
        },
        'competitive_advantage': {
            'weight': 0.3,
            'keywords': [
                'barrier to entry', 'competitive advantage',
                'unique technology', '10x better', 'superior'
            ]
        }
    }
    
    # Impact/ESG Evaluation Criteria
    IMPACT_CRITERIA = {
        'social_impact': {
            'weight': 0.5,
            'keywords': [
                'social impact', 'sustainability', 'environmental',
                'community', 'welfare'
            ]
        },
        'esg': {
            'weight': 0.5,
            'keywords': [
                'ESG', 'governance', 'sustainable', 'responsible',
                'ethical'
            ]
        }
    } 