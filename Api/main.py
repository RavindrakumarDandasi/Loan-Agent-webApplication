from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import LoanApplication, LoanEvaluationState, EmploymentType, LoanType
from orchestration.orchestrator import LoanEvaluationOrchestrator
from utils.evaluator import SubmissionEvaluator

app = FastAPI(
    title="Loan Application Evaluation API",
    description="Multi-Agent Agentic AI system for loan approval decisions",
    version="1.0.0"
)

orchestrator = LoanEvaluationOrchestrator()

# Setup static files and templates
base_dir = Path(__file__).parent.parent
static_dir = base_dir / "static"
templates_dir = base_dir / "templates"

if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
if templates_dir.exists():
    templates = Jinja2Templates(directory=str(templates_dir))


class EvaluationResponse(BaseModel):
    status: str
    applicant_id: str
    applicant_name: Optional[str] = None
    city: Optional[str] = None
    loan_type: Optional[str] = None
    decision: str
    risk_score: float
    confidence_level: float
    case_id: str
    explanation: str
    estimated_emi: Optional[float] = None
    eligibility_score: Optional[float] = None
    credit_score_category: Optional[str] = None
    risk_level: Optional[str] = None
    debt_to_income_ratio: Optional[float] = None
    recommendation: Optional[str] = None
    error: str = None


@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/evaluate-loan", response_model=EvaluationResponse)
async def evaluate_loan(application: LoanApplication):
    try:
        application.application_timestamp = application.application_timestamp or datetime.now()

        result = orchestrator.evaluate_loan(application)

        if result.error:
            raise HTTPException(status_code=500, detail=result.error)

        if result.compliance is None or result.decision is None:
            raise HTTPException(
                status_code=500,
                detail="Evaluation process incomplete"
            )

        return EvaluationResponse(
            status="success",
            applicant_id=application.applicant_id,
            decision=result.decision.classification.value,
            risk_score=result.decision.risk_score,
            confidence_level=result.decision.confidence_level,
            case_id=result.compliance.case_id,
            explanation=result.decision.explanation
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/", response_class=HTMLResponse)
async def home():
    if templates_dir.exists():
        try:
            with open(templates_dir / "index.html", "r") as f:
                return f.read()
        except FileNotFoundError:
            pass
    return {
        "message": "Loan Application Evaluation System",
        "endpoints": {
            "health": "/health",
            "evaluate": "/evaluate-loan",
            "docs": "/docs"
        }
    }


@app.get("/cities")
async def get_cities():
    cities = [
        "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata",
        "Pune", "Ahmedabad", "Jaipur", "Kochi", "Coimbatore", "Madurai",
        "Trivandrum", "Vijayawada", "Visakhapatnam", "Lucknow", "Chandigarh",
        "Indore", "Bhopal", "Nagpur", "Surat", "Vadodara", "Goa", "Dehradun",
        "Siliguri", "Ranchi", "Patna", "Ludhiana", "Amritsar", "Varanasi",
        "Guwahati", "Nashik", "Jabalpur", "Aurangabad", "Srinagar", "Kota",
        "Udaipur", "Agra", "Kanpur", "Allahabad", "Bhopal", "Ghaziabad",
        "Noida", "Gurgaon", "Faridabad", "Durgapur", "Asansol", "Thiruvananthapuram"
    ]
    return {"cities": sorted(list(set(cities)))}


@app.get("/loan-types")
async def get_loan_types():
    loan_types = [
        {"value": "Personal Loan", "label": "Personal Loan", "icon": "💳"},
        {"value": "Home Loan", "label": "Home Loan", "icon": "🏠"},
        {"value": "Car Loan", "label": "Car Loan", "icon": "🚗"},
        {"value": "Education Loan", "label": "Education Loan", "icon": "🎓"},
        {"value": "Business Loan", "label": "Business Loan", "icon": "💼"}
    ]
    return {"loan_types": loan_types}


@app.get("/employment-types")
async def get_employment_types():
    employment_types = [e.value for e in EmploymentType]
    return {"employment_types": employment_types}


@app.post("/evaluate-submission")
async def evaluate_submission(participant_name: str, submission_path: str):
    """Evaluate a case study submission and return detailed report"""
    try:
        # Validate submission path
        submission = Path(submission_path)
        if not submission.exists():
            raise HTTPException(status_code=404, detail=f"Submission path not found: {submission_path}")
        if not submission.is_dir():
            raise HTTPException(status_code=400, detail=f"Submission path must be a directory: {submission_path}")

        # Run evaluation
        evaluator = SubmissionEvaluator()
        report = evaluator.evaluate(
            submission_path=str(submission.absolute()),
            participant_name=participant_name
        )

        return {
            "status": "success",
            "report": report.to_dict()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
