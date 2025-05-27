from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from typing import Dict, List, Optional
from pydantic import BaseModel
from datetime import datetime

from src.utils.affinity_client import AffinityClient
from src.crawlers.portfolio_crawler import PortfolioCrawler
from src.models.scoring import CompanyScorer
from src.data_processing.email_processor import EmailProcessor
from src.data_processing.market_intelligence import MarketIntelligence

# Load environment variables
load_dotenv()

# Affinity Configuration
AFFINITY_API_KEY=os.getenv("AFFINITY_API_KEY")
AFFINITY_INCUBATORS_LIST_ID=os.getenv("AFFINITY_INCUBATORS_LIST_ID")
AFFINITY_PORTFOLIO_LIST_ID=os.getenv("AFFINITY_PORTFOLIO_LIST_ID")

# Email Configuration
EMAIL_SERVER=os.getenv("EMAIL_SERVER")
EMAIL_ADDRESS=os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD=os.getenv("EMAIL_PASSWORD")

# API Keys
NEWS_API_KEY=os.getenv("NEWS_API_KEY")
TWITTER_BEARER_TOKEN=os.getenv("TWITTER_BEARER_TOKEN")
CRUNCHBASE_API_KEY=os.getenv("CRUNCHBASE_API_KEY")

# Server Configuration
PORT=int(os.getenv("PORT", 8000))

app = FastAPI(
    title="Model Context Protocol Server",
    description="Automated outbound sourcing and investment opportunity analysis",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize clients
affinity_client = AffinityClient()
portfolio_crawler = PortfolioCrawler()
company_scorer = CompanyScorer()
email_processor = EmailProcessor()
market_intelligence = MarketIntelligence()

class ThesisInput(BaseModel):
    thesis_text: str

class CompanyInput(BaseModel):
    name: str
    description: str
    founders: List[str]
    problem: str
    solution: str
    usp: str
    sectors: List[str]

@app.get("/")
async def root():
    return {"message": "Welcome to MCP Server", "status": "active"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/daily-dealflow")
async def get_daily_dealflow():
    """Process and return daily deal flow from emails"""
    try:
        deals = email_processor.process_daily_dealflow()
        return {"deals": deals}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/market-insights")
async def get_market_insights():
    """Get market insights and trends"""
    try:
        insights = await market_intelligence.gather_market_insights()
        return insights
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/company-insights/{company_name}")
async def get_company_insights(company_name: str):
    """Get comprehensive insights for a specific company"""
    try:
        insights = await market_intelligence.get_company_insights(company_name)
        return insights
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/incubators")
async def get_incubators():
    """Get list of all incubators from the database"""
    try:
        df = affinity_client.get_incubators_data()
        return {"incubators": df.to_dict('records')}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/crawl-portfolio/{incubator_name}")
async def crawl_portfolio(incubator_name: str, background_tasks: BackgroundTasks):
    """Crawl portfolio data for a specific incubator"""
    try:
        # Get incubator URL from database
        df = affinity_client.get_incubators_data()
        incubator = df[df['name'] == incubator_name].iloc[0]
        
        # Add crawling task to background
        background_tasks.add_task(
            crawl_and_store_portfolio,
            incubator_name,
            incubator['portfolio_url']
        )
        
        return {
            "message": f"Started crawling portfolio for {incubator_name}",
            "status": "processing"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/portfolio/{incubator_name}")
async def get_portfolio(incubator_name: str):
    """Get portfolio data for a specific incubator"""
    try:
        df = affinity_client.get_portfolio_data(incubator_name)
        return {"portfolio": df.to_dict('records')}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/score-company")
async def score_company(company: CompanyInput, thesis: Optional[ThesisInput] = None):
    """Score a company based on investment criteria and thesis"""
    try:
        # Convert company input to dict
        company_data = company.dict()
        
        # Get base scores
        scores = company_scorer.score_company(company_data)
        
        # Add thesis relevance if provided
        if thesis:
            scores['thesis_relevance'] = company_scorer.calculate_thesis_relevance(
                company_data,
                thesis.thesis_text
            )
        
        # Get market insights
        market_data = await market_intelligence.get_company_insights(company.name)
        scores['market_insights'] = market_data
        
        return scores
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/investment-memo/{company_name}")
async def generate_investment_memo(company_name: str):
    """Generate an investment committee memo"""
    try:
        # Get company data
        company_data = affinity_client.get_company_data(company_name)
        
        # Get market insights
        market_data = await market_intelligence.get_company_insights(company_name)
        
        # Get scoring
        scores = company_scorer.score_company(company_data)
        
        # Combine all data into memo format
        memo = {
            'company_overview': company_data,
            'market_analysis': market_data,
            'scoring': scores,
            'recommendation': _generate_recommendation(scores, market_data),
            'generated_at': datetime.now().isoformat()
        }
        
        return memo
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def _generate_recommendation(scores: Dict, market_data: Dict) -> Dict:
    """Generate investment recommendation based on scores and market data"""
    # Implement recommendation logic
    return {
        'recommendation': 'pending',
        'key_factors': [],
        'risks': [],
        'next_steps': []
    }

async def crawl_and_store_portfolio(incubator_name: str, portfolio_url: str):
    """Background task to crawl and store portfolio data"""
    try:
        # Crawl portfolio data
        portfolio_data = portfolio_crawler.extract_portfolio_data(portfolio_url)
        
        # Store in Affinity
        affinity_client.update_portfolio_data(incubator_name, portfolio_data)
    except Exception as e:
        print(f"Error processing portfolio for {incubator_name}: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT) 