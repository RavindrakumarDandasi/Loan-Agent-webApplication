# Multi-Agent Agentic AI Loan Application System

A distributed, microservices-based AI system that automates loan application analysis using multiple specialized agents working through an orchestration layer.

## Architecture Overview

```
┌─────────────────┐
│  Streamlit UI   │ (Presentation Layer)
└────────┬────────┘
         │ HTTP
┌────────▼──────────┐
│   FastAPI REST    │ (Microservice Layer)
└────────┬──────────┘
         │
┌────────▼─────────────────┐
│  LangGraph Orchestrator   │ (Orchestration Layer)
└────────┬──────────────────┘
         │
    ┌────┴────────────────────────────┐
    │                                  │
┌───▼─────────────┐ ┌────────────────▼──┐
│   Agents        │ │   MCP Servers     │
├─────────────────┤ ├───────────────────┤
│ • Applicant     │ │ • ApplicantDB      │
│ • Financial     │ │ • RiskRulesDB     │
│ • Decision      │ │ • DecisionRules   │
│ • Compliance    │ │ • Notification    │
└─────────────────┘ └───────────────────┘
```

## Key Features

- **Multi-Agent Architecture**: Independent agents handling specific responsibilities
- **Automated Decision Making**: Intelligent routing for Approved/Rejected/Manual Review
- **Risk Analysis**: Comprehensive financial risk assessment
- **Explainable Decisions**: Detailed reasoning for each decision
- **Audit Trail**: Complete compliance logging with case IDs
- **Scalable Design**: Loosely coupled microservices architecture

## Project Structure

```
Loan_Agent/
├── agents/                    # Domain-specific agents
│   ├── applicant_agent.py    # Applicant profile evaluation
│   ├── financial_risk_agent.py # Risk analysis
│   ├── decision_agent.py      # Decision synthesis
│   └── compliance_agent.py    # Compliance & notifications
├── mcp_servers/              # MCP server implementations
│   ├── applicant_db.py       # Applicant data access
│   ├── risk_rules_db.py      # Risk calculation rules
│   ├── decision_synthesis.py # Decision rules engine
│   └── notification_system.py # Notification handling
├── orchestration/            # Workflow orchestration
│   └── orchestrator.py       # LangGraph orchestration engine
├── Api/                      # FastAPI microservice
│   └── main.py              # REST API endpoints
├── Ui/                       # User interface
│   └── app.py               # Streamlit chatbot UI
├── utils/                    # Utility modules
│   └── bedrock_client.py    # Bedrock API client
├── models.py                # Data models & schemas
├── config.py                # Configuration settings
└── requirements.txt         # Python dependencies
```

## Installation

1. **Clone/Navigate to project**:
```bash
cd /home/ubuntu/Desktop/Loan_Agent
```

2. **Create virtual environment** (if needed):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment**:
Update `.env` file with your API keys:
```
ANTHROPIC_API_KEY=your-key-here
```

## Running the System

### Option 1: Run API and UI Separately

**Terminal 1 - Start API Server**:
```bash
chmod +x run_api.sh
./run_api.sh
# API runs on http://localhost:8000
```

**Terminal 2 - Start Streamlit UI**:
```bash
chmod +x run_ui.sh
./run_ui.sh
# UI runs on http://localhost:8501
```

### Option 2: Run Individual Components

**API Server**:
```bash
python -m uvicorn Api.main:app --host 0.0.0.0 --port 8000 --reload
```

**Streamlit UI**:
```bash
streamlit run Ui/app.py
```

**Test Direct Evaluation**:
```bash
python test_system.py
```

## API Endpoints

### Health Check
```
GET /health
Response: {"status": "healthy", "timestamp": "..."}
```

### Evaluate Loan Application
```
POST /evaluate-loan
Content-Type: application/json

Request:
{
  "applicant_id": "APP001",
  "age": 35,
  "income": 60000,
  "employment_type": "SALARIED",
  "credit_score": 720,
  "loan_amount": 100000,
  "tenure_months": 60,
  "existing_liabilities": 20000,
  "location": "New York"
}

Response:
{
  "status": "success",
  "applicant_id": "APP001",
  "decision": "APPROVED",
  "risk_score": 0.25,
  "confidence_level": 0.95,
  "case_id": "CASE-ABC123XY",
  "explanation": "..."
}
```

## Agent Responsibilities

### 1. Applicant Profile Agent
- Evaluates applicant's income stability
- Assesses employment risk
- Summarizes credit history
- Flags application completeness issues

### 2. Financial Risk Agent
- Calculates Debt-to-Income ratio
- Determines credit score risk level
- Assesses loan amount risk
- Detects anomalies in application

### 3. Loan Decision Agent
- Synthesizes decision from all risk factors
- Classifies as: APPROVED / REJECTED / MANUAL_REVIEW
- Calculates risk score and confidence level
- Provides detailed explanation

### 4. Compliance & Action Orchestrator
- Generates case IDs
- Creates audit trail
- Sends notifications
- Maintains compliance records

## Decision Rules

### Auto-Approval
- DTI Ratio ≤ 0.30
- Credit Score ≥ 750
- Employment Risk = LOW

### Auto-Rejection
- DTI Ratio ≥ 0.60
- Credit Score ≤ 500
- Critical anomalies detected

### Manual Review
- Any borderline case
- Missing critical information
- Conflicting risk indicators

## Data Models

### LoanApplication
```python
{
  "applicant_id": str,
  "age": int,
  "income": float,
  "employment_type": str,
  "credit_score": int,
  "loan_amount": float,
  "tenure_months": int,
  "existing_liabilities": float,
  "location": str,
  "application_timestamp": datetime
}
```

### LoanEvaluationState
```python
{
  "application": LoanApplication,
  "applicant_profile": ApplicantProfileResult,
  "financial_risk": FinancialRiskResult,
  "decision": LoanDecisionResult,
  "compliance": ComplianceResult,
  "error": str (optional)
}
```

## Testing

Run the comprehensive test suite:
```bash
python test_system.py
```

This will:
- Test each agent independently
- Verify orchestration workflow
- Test API endpoints
- Validate decision rules
- Check error handling

## Technology Stack

- **Orchestration**: LangGraph, LangChain
- **API Framework**: FastAPI, Uvicorn
- **UI Framework**: Streamlit
- **Agent SDK**: Anthropic Agent SDK
- **LLM**: Claude Sonnet 4.6
- **Communication**: MCP (Model Context Protocol)
- **Language**: Python 3.10+

## Configuration

Edit `config.py` to customize:
- Decision rules and thresholds
- DTI/Credit score limits
- Risk assessment parameters
- API host/port settings

## Monitoring & Logging

- API logs: Check console output from uvicorn
- Compliance logs: Stored in memory (can be persisted to database)
- Streamlit logs: Check console output

## Future Enhancements

1. **Database Persistence**
   - Store compliance records in PostgreSQL
   - Implement applicant history tracking

2. **Advanced Analytics**
   - Decision analytics dashboard
   - Approval/rejection trends
   - Risk metric analysis

3. **Integration**
   - Document verification service
   - Third-party credit bureau integration
   - Automated verification APIs

4. **ML Enhancement**
   - Train custom risk models
   - Implement fraud detection
   - Predictive analytics

## Troubleshooting

**API Connection Error**: Ensure API is running on `localhost:8000`
**Missing Dependencies**: Run `pip install -r requirements.txt`
**Port Already in Use**: Change port in `.env` or use different terminal
**Environment Variables**: Verify `.env` file is in project root

## Support

For issues or questions:
1. Check logs for error messages
2. Verify all dependencies are installed
3. Ensure API server is running when using UI
4. Review README and code documentation

## License

Internal Use Only

## Version

1.0.0 (Initial Release)
