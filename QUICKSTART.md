# Quick Start Guide

## 🚀 Get Started in 2 Minutes

### Prerequisites
- Python 3.10+
- Virtual environment already created at `venv/`

### Step 1: Activate Virtual Environment
```bash
cd /home/ubuntu/Desktop/Loan_Agent
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Tests (Verify Everything Works)
```bash
python3 test_system.py
```

You should see:
```
✅ Total Tests Passed: 5/5
```

### Step 4a: Start API Server (Terminal 1)
```bash
chmod +x run_api.sh
./run_api.sh
```

API will be available at: `http://localhost:8000`

Test the API:
```bash
curl -X POST http://localhost:8000/health
```

### Step 4b: Start Streamlit UI (Terminal 2 - in new terminal)
```bash
cd /home/ubuntu/Desktop/Loan_Agent
source venv/bin/activate
chmod +x run_ui.sh
./run_ui.sh
```

UI will be available at: `http://localhost:8501`

### Step 5: Submit a Loan Application

1. Open http://localhost:8501 in your browser
2. Fill in the application form with sample data
3. Click "🚀 Evaluate Application"
4. Review the decision and risk assessment

## Sample Test Data

### Good Applicant (Likely Approval)
- Applicant ID: APP001
- Age: 35
- Annual Income: $100,000
- Employment: SALARIED
- Credit Score: 780
- Loan Amount: $100,000
- Tenure: 60 months
- Existing Liabilities: $10,000
- Location: New York

### Risky Applicant (Likely Rejection)
- Applicant ID: APP002
- Age: 25
- Annual Income: $30,000
- Employment: FREELANCE
- Credit Score: 480
- Loan Amount: $150,000
- Tenure: 36 months
- Existing Liabilities: $50,000
- Location: Chicago

### Borderline Applicant (Manual Review)
- Applicant ID: APP003
- Age: 45
- Annual Income: $60,000
- Employment: SALARIED
- Credit Score: 680
- Loan Amount: $100,000
- Tenure: 72 months
- Existing Liabilities: $15,000
- Location: Los Angeles

## Direct API Testing

### Health Check
```bash
curl http://localhost:8000/health
```

### Evaluate Application
```bash
curl -X POST http://localhost:8000/evaluate-loan \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "APP001",
    "age": 35,
    "income": 100000,
    "employment_type": "SALARIED",
    "credit_score": 780,
    "loan_amount": 100000,
    "tenure_months": 60,
    "existing_liabilities": 10000,
    "location": "New York"
  }'
```

### API Documentation
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## File Structure

```
Loan_Agent/
├── agents/                    # 4 specialized agents
├── mcp_servers/              # 4 MCP servers for data access
├── orchestration/            # LangGraph orchestration engine
├── Api/                      # FastAPI REST service
├── Ui/                       # Streamlit web interface
├── models.py                 # Data models & Pydantic schemas
├── config.py                 # Configuration settings
├── test_system.py            # Comprehensive test suite
├── requirements.txt          # Python dependencies
├── README.md                 # Full documentation
└── QUICKSTART.md            # This file
```

## Key Decision Rules

| Metric | Threshold | Impact |
|--------|-----------|--------|
| DTI Ratio ≤ 0.40 | Green | Supports approval |
| DTI Ratio ≥ 0.70 | Red | Supports rejection |
| Credit Score ≥ 700 | Green | Supports approval |
| Credit Score ≤ 500 | Red | Supports rejection |
| Employment Risk | LOW | Supports approval |
| Anomalies | Any | Increases risk score |

## Troubleshooting

**Port Already in Use**
```bash
# Change port in .env
API_PORT=8001
STREAMLIT_PORT=8502
```

**Module Not Found**
```bash
# Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**API Connection Error in UI**
```bash
# Ensure API is running on port 8000
# Check API logs for errors
curl http://localhost:8000/health
```

## Next Steps

1. ✅ Run tests to verify installation
2. ✅ Start API server
3. ✅ Open Streamlit UI
4. ✅ Submit sample applications
5. 📚 Read README.md for architecture details
6. 🔧 Customize decision rules in `config.py`
7. 💾 Add database persistence for production

## Learn More

- [Architecture Overview](README.md#architecture-overview)
- [API Endpoints Documentation](README.md#api-endpoints)
- [Agent Responsibilities](README.md#agent-responsibilities)
- [Decision Rules](README.md#decision-rules)

## Support

For issues:
1. Check test output: `python3 test_system.py`
2. Review logs in API/UI terminals
3. Verify all dependencies installed
4. Ensure ports 8000 and 8501 are available
