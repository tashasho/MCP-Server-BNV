# Model Context Protocol (MCP) Server

An intelligent automation system for venture capital operations that streamlines deal flow, market intelligence, and investment analysis.

## Features

### 1. Deal Flow Management
- **Automated Email Processing**
  - Parses inbound deal flow emails
  - Extracts company information, funding stages, and team details
  - Identifies warm introductions
  - Categorizes opportunities by sector

- **Pipeline Organization**
  - Integrates with Affinity CRM
  - Maintains structured data on companies and founders
  - Tracks relationship history and interaction context

### 2. Market Intelligence
- **Real-time Monitoring**
  - News aggregation across target sectors
  - Social media trend analysis
  - Funding round tracking
  - Competitor analysis

- **Trend Analysis**
  - Sector momentum tracking
  - Investment pattern analysis
  - Emerging technology identification
  - Market positioning assessment

### 3. Investment Analysis
- **Company Scoring**
  - Multi-factor evaluation framework
  - Team assessment
  - Business model analysis
  - Technology evaluation
  - Impact/ESG scoring

- **Due Diligence Support**
  - Automated research compilation
  - Competitive landscape analysis
  - Market size validation
  - Risk factor identification

### 4. Portfolio Management
- **Automated Portfolio Tracking**
  - Company performance monitoring
  - News and social media tracking
  - Milestone tracking
  - Relationship management

## Setup

### 1. Environment Setup
Create a `.env` file with the following configurations:
```bash
# Affinity Configuration
AFFINITY_API_KEY=your_affinity_api_key
AFFINITY_INCUBATORS_LIST_ID=your_incubators_list_id
AFFINITY_PORTFOLIO_LIST_ID=your_portfolio_list_id

# Email Configuration
EMAIL_SERVER=imap.gmail.com
EMAIL_ADDRESS=your_email
EMAIL_PASSWORD=your_password

# API Keys
NEWS_API_KEY=your_news_api_key
TWITTER_BEARER_TOKEN=your_twitter_token
CRUNCHBASE_API_KEY=your_crunchbase_key

# Server Configuration
PORT=8000
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Server
```bash
python -m uvicorn src.main:app --reload
```

## API Documentation

### Deal Flow Endpoints
- `GET /daily-dealflow`: Process and return daily deal flow from emails
- `GET /market-insights`: Get market insights and trends
- `GET /company-insights/{company_name}`: Get comprehensive company analysis

### Portfolio Management
- `GET /incubators`: List all incubators
- `POST /crawl-portfolio/{incubator_name}`: Crawl portfolio data
- `GET /portfolio/{incubator_name}`: Get portfolio company data

### Investment Analysis
- `POST /score-company`: Score a company based on investment criteria
- `GET /investment-memo/{company_name}`: Generate investment committee memo

## Project Structure
```
.
├── src/
│   ├── crawlers/         # Web crawling modules
│   ├── data_processing/  # Email and market data processing
│   ├── models/          # Scoring and evaluation models
│   ├── schemas/         # Data models and schemas
│   └── utils/           # Helper functions and clients
├── data/               # Storage for CSV files
├── tests/             # Test cases
└── config/            # Configuration files
```

## Configuration

The system is highly configurable through `config/config.py`, including:
- Sector keywords and classifications
- Investment criteria weights
- Team evaluation parameters
- Market intelligence settings
- Deal flow processing rules

## Testing

### Setup Testing Environment
```bash
pip install -U pytest
```

### Running Tests
```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run tests in a specific directory
pytest tests/

# Run a specific test file
pytest tests/test_email_processor.py

# Run tests matching a specific pattern
pytest -k "email or market"
```

### Test Structure
```
tests/
├── conftest.py              # Shared test fixtures
├── test_email_processor.py  # Email processing tests
├── test_market_intel.py     # Market intelligence tests
├── test_scoring.py          # Company scoring tests
└── test_portfolio.py        # Portfolio management tests
```

### Writing Tests
Each test file should follow these conventions:
1. Use descriptive test names with `test_` prefix
2. Group related tests in classes with `Test` prefix
3. Use fixtures for common setup
4. Mock external API calls
5. Include both positive and negative test cases

Example:
```python
def test_email_processing_warm_intro():
    processor = EmailProcessor()
    email_content = "I wanted to introduce you to..."
    result = processor._is_warm_intro(email_content)
    assert result == True
```

## Security Notes

1. Store all API keys and credentials securely in `.env`
2. Never commit sensitive credentials to version control
3. Use appropriate access controls for the API endpoints
4. Regularly rotate API keys and credentials
5. Monitor API usage and implement rate limiting

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details 