import uuid
from datetime import datetime
from models import ComplianceResult, LoanDecisionResult, LoanApplication


class NotificationSystemServer:
    def __init__(self):
        self.notification_log = []

    def handle_compliance_and_notification(
        self,
        application: LoanApplication,
        decision: LoanDecisionResult
    ) -> ComplianceResult:
        """Generate compliance records and notifications."""

        case_id = f"CASE-{uuid.uuid4().hex[:8].upper()}"
        timestamp = datetime.now()

        action_taken = f"Loan application {decision.classification.value}"
        notification_text = f"Application {application.applicant_id}: {action_taken}"

        summary = f"Applicant ID: {application.applicant_id}, Decision: {decision.classification.value}, Risk Score: {decision.risk_score:.2f}, Confidence: {decision.confidence_level:.2%}"

        record = {
            "case_id": case_id,
            "applicant_id": application.applicant_id,
            "decision": decision.classification.value,
            "timestamp": timestamp.isoformat(),
            "notification": notification_text,
            "summary": summary
        }

        self.notification_log.append(record)

        result = ComplianceResult(
            action_taken=action_taken,
            notification_sent=True,
            case_id=case_id,
            timestamp=timestamp,
            summary=summary
        )

        return result
