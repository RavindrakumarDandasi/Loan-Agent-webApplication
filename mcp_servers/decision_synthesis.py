from datetime import datetime
from models import (
    LoanDecisionResult,
    DecisionEnum,
    LoanApplication,
    ApplicantProfileResult,
    FinancialRiskResult
)


class DecisionSynthesisServer:
    def __init__(self):
        self.decision_rules = {
            "auto_approve_dti": 0.40,
            "auto_reject_dti": 0.70,
            "auto_approve_credit": 700,
            "auto_reject_credit": 500,
        }

    def synthesize_decision(
        self,
        application: LoanApplication,
        applicant_profile: ApplicantProfileResult,
        financial_risk: FinancialRiskResult
    ) -> LoanDecisionResult:
        """Synthesize loan decision based on all risk factors."""

        decision = DecisionEnum.MANUAL_REVIEW
        confidence = 0.5
        risk_score = 0.5
        decision_factors = []

        dti = financial_risk.debt_to_income_ratio
        credit_score = application.credit_score
        employment_risk = applicant_profile.employment_risk

        if dti <= self.decision_rules["auto_approve_dti"] and credit_score >= self.decision_rules["auto_approve_credit"]:
            decision = DecisionEnum.APPROVED
            confidence = 0.90
            risk_score = 0.25
            decision_factors = ["Low DTI", "Good credit score", "Meets approval criteria"]

        elif dti >= self.decision_rules["auto_reject_dti"] or credit_score <= self.decision_rules["auto_reject_credit"]:
            decision = DecisionEnum.REJECTED
            confidence = 0.90
            risk_score = 0.85
            decision_factors = ["High DTI" if dti >= self.decision_rules["auto_reject_dti"] else "",
                               "Poor credit score" if credit_score <= self.decision_rules["auto_reject_credit"] else ""]
            decision_factors = [f for f in decision_factors if f]

        else:
            decision = DecisionEnum.MANUAL_REVIEW
            confidence = 0.75
            risk_score = 0.50
            decision_factors = ["Borderline financial metrics", "Requires manual assessment"]

        if financial_risk.anomaly_detected:
            decision_factors.append(f"Risk anomalies detected: {financial_risk.reasoning}")
            risk_score = min(1.0, risk_score + 0.2)
            confidence = max(0.3, confidence - 0.15)

        if len(applicant_profile.application_completeness_flags) > 0:
            decision_factors.extend(applicant_profile.application_completeness_flags)

        explanation = f"Decision: {decision.value}. Risk Score: {risk_score:.2f}. Factors: {', '.join(decision_factors)}"

        return LoanDecisionResult(
            classification=decision,
            risk_score=risk_score,
            confidence_level=confidence,
            key_decision_factors=decision_factors,
            explanation=explanation
        )
