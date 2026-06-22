from mcp_servers.notification_system import NotificationSystemServer
from models import LoanApplication, LoanDecisionResult, ComplianceResult


class ComplianceOrchestratorAgent:
    def __init__(self):
        self.db = NotificationSystemServer()

    def handle_compliance(
        self,
        application: LoanApplication,
        decision: LoanDecisionResult
    ) -> ComplianceResult:
        """Generate compliance records and handle notifications."""
        return self.db.handle_compliance_and_notification(application, decision)
