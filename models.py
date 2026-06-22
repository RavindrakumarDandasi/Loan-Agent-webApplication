from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class DecisionEnum(str, Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    MANUAL_REVIEW = "MANUAL_REVIEW"


class EmploymentType(str, Enum):
    SALARIED = "SALARIED"
    SELF_EMPLOYED = "SELF_EMPLOYED"
    FREELANCE = "FREELANCE"
    UNEMPLOYED = "UNEMPLOYED"


class LoanType(str, Enum):
    PERSONAL = "Personal Loan"
    HOME = "Home Loan"
    CAR = "Car Loan"
    EDUCATION = "Education Loan"
    BUSINESS = "Business Loan"


class CreditScoreCategory(str, Enum):
    POOR = "Poor"
    AVERAGE = "Average"
    GOOD = "Good"
    EXCELLENT = "Excellent"


class RiskLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class LoanApplication(BaseModel):
    applicant_id: str
    applicant_name: Optional[str] = None
    age: int
    income: float
    monthly_income: Optional[float] = None
    employment_type: EmploymentType
    credit_score: int
    loan_amount: float
    tenure_months: int
    existing_liabilities: float
    location: str
    city: Optional[str] = None
    loan_type: Optional[str] = None
    application_timestamp: Optional[datetime] = None


class ApplicantProfileResult(BaseModel):
    income_stability_score: float
    employment_risk: str
    credit_history_summary: str
    application_completeness_flags: list[str]


class FinancialRiskResult(BaseModel):
    debt_to_income_ratio: float
    credit_score_risk_level: str
    loan_amount_risk: str
    anomaly_detected: bool
    reasoning: str


class LoanDecisionResult(BaseModel):
    classification: DecisionEnum
    risk_score: float
    confidence_level: float
    key_decision_factors: list[str]
    explanation: str


class ComplianceResult(BaseModel):
    action_taken: str
    notification_sent: bool
    case_id: str
    timestamp: datetime
    summary: str


class LoanEvaluationState(BaseModel):
    application: LoanApplication
    applicant_profile: Optional[ApplicantProfileResult] = None
    financial_risk: Optional[FinancialRiskResult] = None
    decision: Optional[LoanDecisionResult] = None
    compliance: Optional[ComplianceResult] = None
    error: Optional[str] = None
