import streamlit as st
import requests
import json
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import EmploymentType

st.set_page_config(
    page_title="Loan Application Portal",
    page_icon="💰",
    layout="wide"
)

API_URL = "http://localhost:8000"


def evaluate_application(form_data):
    """Send loan application to API for evaluation."""
    try:
        response = requests.post(
            f"{API_URL}/evaluate-loan",
            json=form_data,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to API server. Ensure it's running on localhost:8000"}
    except requests.exceptions.RequestException as e:
        return {"error": f"API Error: {str(e)}"}


def main():
    st.title("💰 Loan Application Evaluation System")
    st.markdown("---")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("Application Form")

        with st.form("loan_application"):
            col_left, col_right = st.columns(2)

            with col_left:
                applicant_id = st.text_input(
                    "Applicant ID",
                    value="APP001",
                    help="Unique identifier for the applicant"
                )

                age = st.number_input(
                    "Age",
                    min_value=18,
                    max_value=100,
                    value=35,
                    step=1
                )

                income = st.number_input(
                    "Annual Income ($)",
                    min_value=15000,
                    max_value=500000,
                    value=60000,
                    step=1000
                )

                employment_type = st.selectbox(
                    "Employment Type",
                    [e.value for e in EmploymentType]
                )

            with col_right:
                credit_score = st.number_input(
                    "Credit Score",
                    min_value=300,
                    max_value=850,
                    value=720,
                    step=10
                )

                loan_amount = st.number_input(
                    "Loan Amount ($)",
                    min_value=5000,
                    max_value=500000,
                    value=100000,
                    step=5000
                )

                tenure_months = st.number_input(
                    "Tenure (months)",
                    min_value=6,
                    max_value=360,
                    value=60,
                    step=6
                )

                existing_liabilities = st.number_input(
                    "Existing Liabilities ($)",
                    min_value=0,
                    max_value=500000,
                    value=20000,
                    step=1000
                )

            location = st.text_input(
                "Location",
                value="New York",
                help="Applicant's location/state"
            )

            submit_button = st.form_submit_button(
                "🚀 Evaluate Application",
                use_container_width=True
            )

    with col2:
        st.markdown("### Quick Stats")
        st.metric("DTI Ratio (Est.)", f"{((existing_liabilities/12 + loan_amount/tenure_months) / (income/12)):.2f}")
        st.metric("Loan to Income", f"{(loan_amount/income):.2f}x")
        st.metric("Monthly Installment", f"${loan_amount/tenure_months:,.0f}")

    st.markdown("---")

    if submit_button:
        with st.spinner("⏳ Evaluating application..."):
            form_data = {
                "applicant_id": applicant_id,
                "age": age,
                "income": income,
                "employment_type": employment_type,
                "credit_score": credit_score,
                "loan_amount": loan_amount,
                "tenure_months": tenure_months,
                "existing_liabilities": existing_liabilities,
                "location": location
            }

            result = evaluate_application(form_data)

            if "error" in result:
                st.error(f"❌ {result['error']}")
            else:
                st.success("✅ Evaluation Complete!")

                col1, col2, col3 = st.columns(3)

                with col1:
                    decision = result.get("decision", "UNKNOWN")
                    if decision == "APPROVED":
                        st.success(f"### Decision: {decision}")
                    elif decision == "REJECTED":
                        st.error(f"### Decision: {decision}")
                    else:
                        st.warning(f"### Decision: {decision}")

                with col2:
                    st.info(f"**Risk Score:** {result.get('risk_score', 0):.2f}")

                with col3:
                    st.info(f"**Confidence:** {result.get('confidence_level', 0):.1%}")

                st.markdown("---")

                st.subheader("📋 Detailed Results")

                result_cols = st.columns(2)

                with result_cols[0]:
                    st.markdown(f"**Case ID:** `{result.get('case_id', 'N/A')}`")
                    st.markdown(f"**Applicant ID:** `{result.get('applicant_id', 'N/A')}`")
                    st.markdown(f"**Status:** {result.get('status', 'N/A')}")

                with result_cols[1]:
                    st.markdown(f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

                st.markdown("---")
                st.subheader("💡 Explanation")
                st.info(result.get("explanation", "No explanation available"))

                st.markdown("---")

                if st.button("📥 Download Results (JSON)"):
                    json_str = json.dumps(result, indent=2)
                    st.download_button(
                        label="Download JSON",
                        data=json_str,
                        file_name=f"loan_evaluation_{result.get('applicant_id', 'unknown')}.json",
                        mime="application/json"
                    )


if __name__ == "__main__":
    main()
