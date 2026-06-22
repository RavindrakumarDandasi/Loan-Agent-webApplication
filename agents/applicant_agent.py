from mcp_servers.applicant_db import ApplicantDBServer
from models import LoanApplication, ApplicantProfileResult


class ApplicantProfileAgent:
    def __init__(self):
        self.db = ApplicantDBServer()

    def evaluate_applicant_profile(self, application: LoanApplication) -> ApplicantProfileResult:
        """Evaluate applicant profile and return risk metrics."""
        return self.db.get_applicant_profile(application.applicant_id, application)
