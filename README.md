# Model Context Protocol (MCP) Server

An automated outbound sourcing system that analyzes and scores potential investment opportunities based on predefined investment criteria.

## Features

1. Database Access & Integration
   - Connects to Google Sheets database of incubators and grants
   - Automated portfolio data collection from incubator websites
   - Structured data storage in CSV format

2. Data Collection & Processing
   - Web crawling for portfolio companies
   - Company information extraction including descriptions, founder data, and problem-solution details
   - Automated sector and keyword tagging

3. Investment Analysis
   - Relevance scoring based on investment thesis
   - Multi-criteria evaluation (team, business model, technology, impact)
   - ESG and impact assessment

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
Create a `.env` file with:
```
GOOGLE_SHEETS_CREDENTIALS=path_to_your_credentials.json
SPREADSHEET_ID=your_spreadsheet_id
```

3. Run the server:
```bash
python -m uvicorn src.main:app --reload
```

## Project Structure

```
.
├── src/
│   ├── crawlers/         # Web crawling modules
│   ├── data_processing/  # Data processing and analysis
│   ├── models/          # Scoring and evaluation models
│   ├── schemas/         # Data models and schemas
│   └── utils/           # Helper functions
├── data/               # Storage for CSV files
├── tests/             # Test cases
└── config/            # Configuration files
```

## API Documentation

The API documentation is available at `http://localhost:8000/docs` when running the server locally. 