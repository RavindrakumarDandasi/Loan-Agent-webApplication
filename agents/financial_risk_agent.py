from mcp_servers.risk_rules_db import RiskRulesDBServer
from models import LoanApplication, ApplicantProfileResult, FinancialRiskResult


class FinancialRiskAgent:
    def __init__(self):
        self.db = RiskRulesDBServer()

    def analyze_financial_risk(
        self,
        application: LoanApplication,
        applicant_profile: ApplicantProfileResult
    ) -> FinancialRiskResult:
        """Analyze financial risk based on application and profile data."""
        return self.db.analyze_financial_risk(application, applicant_profile)
