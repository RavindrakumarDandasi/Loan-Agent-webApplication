import json
from typing import Any
from models import ApplicantProfileResult, LoanApplication


class ApplicantDBServer:
    def __init__(self):
        self.applicant_database = {
            "APP001": {
                "income_stability_years": 5,
                "employment_history": "5 years in current role",
                "previous_defaults": 0,
                "account_age_years": 10
            },
            "APP002": {
                "income_stability_years": 1,
                "employment_history": "1 year in current role",
                "previous_defaults": 1,
                "account_age_years": 2
            },
            "APP003": {
                "income_stability_years": 15,
                "employment_history": "15 years in current role",
                "previous_defaults": 0,
                "account_age_years": 20
            }
        }

    def get_applicant_profile(self, applicant_id: str, application: LoanApplication) -> ApplicantProfileResult:
        """Fetch applicant profile and compute metrics."""

        applicant_data = self.applicant_database.get(applicant_id, {})

        years_employed = applicant_data.get("income_stability_years", 0)
        if years_employed >= 3:
            income_stability = 0.85
        elif years_employed >= 1:
            income_stability = 0.60
        else:
            income_stability = 0.40

        employment_risk_map = {
            "SALARIED": "LOW",
            "SELF_EMPLOYED": "MEDIUM",
            "FREELANCE": "HIGH",
            "UNEMPLOYED": "CRITICAL"
        }

        employment_history = applicant_data.get("employment_history", "Unknown")
        previous_defaults = applicant_data.get("previous_defaults", 0)
        account_age = applicant_data.get("account_age_years", 0)

        completeness_flags = []
        if application.age < 21:
            completeness_flags.append("Applicant age below minimum threshold")
        if application.income < 20000:
            completeness_flags.append("Income below minimum threshold")
        if account_age < 1:
            completeness_flags.append("Insufficient credit history")

        return ApplicantProfileResult(
            income_stability_score=income_stability,
            employment_risk=employment_risk_map.get(application.employment_type, "UNKNOWN"),
            credit_history_summary=f"{employment_history}. Previous defaults: {previous_defaults}. Account age: {account_age} years",
            application_completeness_flags=completeness_flags
        )
