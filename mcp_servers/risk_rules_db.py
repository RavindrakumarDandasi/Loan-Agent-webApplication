from models import FinancialRiskResult, LoanApplication, ApplicantProfileResult


class RiskRulesDBServer:
    def __init__(self):
        self.risk_thresholds = {
            "dti_high": 0.50,
            "dti_medium": 0.35,
            "credit_score_excellent": 750,
            "credit_score_good": 650,
            "credit_score_fair": 550,
            "loan_amount_high_ratio": 5.0,
            "loan_amount_medium_ratio": 3.0
        }

    def analyze_financial_risk(
        self,
        application: LoanApplication,
        applicant_profile: ApplicantProfileResult
    ) -> FinancialRiskResult:
        """Analyze financial risk based on application and profile data."""

        monthly_income = application.income / 12
        monthly_loan_payment = (application.loan_amount / application.tenure_months)
        total_monthly_liabilities = (application.existing_liabilities / 12) + monthly_loan_payment

        dti_ratio = total_monthly_liabilities / monthly_income if monthly_income > 0 else 1.0

        if application.credit_score >= self.risk_thresholds["credit_score_excellent"]:
            credit_risk = "LOW"
        elif application.credit_score >= self.risk_thresholds["credit_score_good"]:
            credit_risk = "MEDIUM"
        elif application.credit_score >= self.risk_thresholds["credit_score_fair"]:
            credit_risk = "HIGH"
        else:
            credit_risk = "CRITICAL"

        loan_to_income_ratio = application.loan_amount / application.income
        if loan_to_income_ratio > self.risk_thresholds["loan_amount_high_ratio"]:
            loan_risk = "HIGH"
        elif loan_to_income_ratio > self.risk_thresholds["loan_amount_medium_ratio"]:
            loan_risk = "MEDIUM"
        else:
            loan_risk = "LOW"

        anomaly_detected = False
        anomaly_reasons = []

        if dti_ratio > self.risk_thresholds["dti_high"]:
            anomaly_detected = True
            anomaly_reasons.append("DTI ratio exceeds high threshold")

        if credit_risk == "CRITICAL":
            anomaly_detected = True
            anomaly_reasons.append("Critical credit score")

        if applicant_profile.employment_risk == "HIGH":
            anomaly_detected = True
            anomaly_reasons.append("High employment risk")

        if len(applicant_profile.application_completeness_flags) > 0:
            anomaly_detected = True
            anomaly_reasons.append("Application completeness issues")

        reasoning = f"DTI Ratio: {dti_ratio:.2f}. Credit Risk: {credit_risk}. Loan Risk: {loan_risk}. "
        if anomaly_reasons:
            reasoning += "Anomalies: " + ", ".join(anomaly_reasons)

        return FinancialRiskResult(
            debt_to_income_ratio=dti_ratio,
            credit_score_risk_level=credit_risk,
            loan_amount_risk=loan_risk,
            anomaly_detected=anomaly_detected,
            reasoning=reasoning
        )
