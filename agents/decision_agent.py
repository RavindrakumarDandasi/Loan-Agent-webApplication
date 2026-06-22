from mcp_servers.decision_synthesis import DecisionSynthesisServer
from models import (
    LoanApplication,
    ApplicantProfileResult,
    FinancialRiskResult,
    LoanDecisionResult
)


class LoanDecisionAgent:
    def __init__(self):
        self.db = DecisionSynthesisServer()

    def make_decision(
        self,
        application: LoanApplication,
        applicant_profile: ApplicantProfileResult,
        financial_risk: FinancialRiskResult
    ) -> LoanDecisionResult:
        """Synthesize loan decision based on all risk factors."""
        return self.db.synthesize_decision(application, applicant_profile, financial_risk)
