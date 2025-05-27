from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from typing import Dict, List, Optional
from pydantic import BaseModel

from src.utils.sheets import GoogleSheetsClient
from src.crawlers.portfolio_crawler import PortfolioCrawler
from src.models.scoring import CompanyScorer

# Load environment variables
load_dotenv()

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
sheets_client = GoogleSheetsClient()
portfolio_crawler = PortfolioCrawler()
company_scorer = CompanyScorer()

class ThesisInput(BaseModel):
    thesis_text: str

@app.get("/")
async def root():
    return {"message": "Welcome to MCP Server", "status": "active"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/incubators")
async def get_incubators():
    """Get list of all incubators from the database"""
    try:
        df = sheets_client.get_incubators_data()
        return {"incubators": df.to_dict('records')}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/crawl-portfolio/{incubator_name}")
async def crawl_portfolio(incubator_name: str, background_tasks: BackgroundTasks):
    """Crawl portfolio data for a specific incubator"""
    try:
        # Get incubator URL from database
        df = sheets_client.get_incubators_data()
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
        df = sheets_client.get_portfolio_data(incubator_name)
        return {"portfolio": df.to_dict('records')}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/score-company")
async def score_company(company_data: Dict, thesis: Optional[ThesisInput] = None):
    """Score a company based on investment criteria and thesis"""
    try:
        # Get base scores
        scores = company_scorer.score_company(company_data)
        
        # Add thesis relevance if provided
        if thesis:
            scores['thesis_relevance'] = company_scorer.calculate_thesis_relevance(
                company_data,
                thesis.thesis_text
            )
        
        return scores
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def crawl_and_store_portfolio(incubator_name: str, portfolio_url: str):
    """Background task to crawl and store portfolio data"""
    try:
        # Crawl portfolio data
        portfolio_data = portfolio_crawler.extract_portfolio_data(portfolio_url)
        
        # Store in Google Sheets
        sheets_client.update_portfolio_data(incubator_name, portfolio_data)
    except Exception as e:
        print(f"Error processing portfolio for {incubator_name}: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 