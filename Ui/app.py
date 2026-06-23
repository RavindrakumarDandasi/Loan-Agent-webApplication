"""
Agentic AI Intelligent Loan Approval System - Streamlit Web Interface
Professional Loan Application & Evaluation Platform with Beautiful Dashboard
"""

import streamlit as st
import requests
import json
from datetime import datetime
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="Agentic AI Loan Approval System",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = "http://localhost:8000"

# Indian Cities Database
INDIAN_CITIES = [
    "Chennai",
    "Bengaluru",
    "Hyderabad",
    "Mumbai",
    "Pune",
    "Delhi",
    "Kolkata",
    "Ahmedabad",
    "Coimbatore",
    "Kochi",
    "Jaipur",
    "Noida"
]

EMPLOYMENT_TYPES = [
    "SALARIED",
    "SELF_EMPLOYED",
    "FREELANCE",
    "BUSINESS_OWNER",
    "UNEMPLOYED"
]

# Beautiful Professional CSS Styling
st.markdown("""
    <style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    .main {
        padding: 0;
        background: linear-gradient(135deg, #1e1e2e 0%, #16213e 100%);
    }

    .stApp {
        background: linear-gradient(135deg, #1e1e2e 0%, #16213e 100%);
    }

    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 0;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }

    .header-container h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        font-weight: 800;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }

    .header-container p {
        font-size: 1.1rem;
        opacity: 0.95;
        font-weight: 500;
    }

    .form-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 2.5rem;
        border-radius: 15px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .form-section-title {
        color: #667eea;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
    }

    .result-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 2.5rem;
        border-radius: 15px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }

    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 32px rgba(102, 126, 234, 0.4);
    }

    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0.5rem 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .metric-subtext {
        font-size: 0.85rem;
        opacity: 0.85;
        margin-top: 0.5rem;
    }

    .status-approved {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        border-left: 8px solid #38ef7d;
    }

    .status-rejected {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        border-left: 8px solid #f45c43;
    }

    .status-review {
        background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
        border-left: 8px solid #fda085;
    }

    .decision-banner {
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    }

    .decision-banner h2 {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }

    .decision-banner p {
        font-size: 1.1rem;
        opacity: 0.95;
        font-weight: 500;
    }

    .info-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-left: 5px solid #667eea;
        border-radius: 8px;
        margin: 0.75rem 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }

    .info-card-text {
        color: #2c3e50;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    .section-header {
        color: #667eea;
        font-size: 1.8rem;
        font-weight: 700;
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.75rem;
        margin: 2rem 0 1.5rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .summary-table {
        width: 100%;
        border-collapse: collapse;
        background: white;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }

    .summary-table th {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.2rem;
        text-align: left;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.9rem;
        letter-spacing: 1px;
    }

    .summary-table td {
        padding: 1rem 1.2rem;
        border-bottom: 1px solid #e9ecef;
        color: #2c3e50;
    }

    .summary-table tr:hover {
        background: #f8f9fa;
    }

    .summary-table tr:last-child td {
        border-bottom: none;
    }

    .progress-bar-container {
        background: #e9ecef;
        border-radius: 10px;
        height: 12px;
        overflow: hidden;
        margin: 0.5rem 0;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        transition: width 0.4s ease;
        border-radius: 10px;
    }

    .risk-low {
        background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
    }

    .risk-medium {
        background: linear-gradient(90deg, #f6d365 0%, #fda085 100%);
    }

    .risk-high {
        background: linear-gradient(90deg, #eb3349 0%, #f45c43 100%);
    }

    .factor-list {
        list-style: none;
        padding: 0;
    }

    .factor-list li {
        background: #f8f9fa;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        border-radius: 4px;
        color: #2c3e50;
        font-weight: 500;
    }

    .factor-list li:before {
        content: "✓ ";
        color: #38ef7d;
        font-weight: bold;
        margin-right: 0.5rem;
    }

    .badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .badge-approved {
        background: #d4edda;
        color: #155724;
    }

    .badge-rejected {
        background: #f8d7da;
        color: #721c24;
    }

    .badge-review {
        background: #fff3cd;
        color: #856404;
    }

    .compliance-box {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        border: 2px solid #667eea;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }

    .compliance-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 0;
        border-bottom: 1px solid #e9ecef;
    }

    .compliance-row:last-child {
        border-bottom: none;
    }

    .compliance-label {
        color: #667eea;
        font-weight: 600;
    }

    .compliance-value {
        color: #2c3e50;
        font-weight: 500;
    }

    .risk-indicator {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .risk-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }

    .risk-dot.low {
        background: #38ef7d;
    }

    .risk-dot.medium {
        background: #fda085;
    }

    .risk-dot.high {
        background: #f45c43;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    .sidebar-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)


def create_header():
    """Create beautiful header"""
    st.markdown("""
    <div class="header-container">
        <h1>💰 Agentic AI Loan Approval System</h1>
        <p>Intelligent Multi-Agent Loan Evaluation Platform</p>
    </div>
    """, unsafe_allow_html=True)


def create_loan_application_form():
    """Create professional loan application form"""
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="form-section-title">📋 Loan Application Form</h2>', unsafe_allow_html=True)

    # Applicant ID and Name Row
    col1, col2 = st.columns(2)
    with col1:
        applicant_id = st.text_input(
            "Applicant ID *",
            placeholder="e.g., APP-2024-001",
            help="Unique identifier for this application"
        )

    with col2:
        applicant_name = st.text_input(
            "Applicant Name *",
            placeholder="Enter full name",
            help="Full legal name of the applicant"
        )

    # Age and City Row
    col3, col4 = st.columns(2)
    with col3:
        age = st.number_input(
            "Age *",
            min_value=18,
            max_value=80,
            value=35,
            help="Applicant age (18-80 years)"
        )

    with col4:
        city = st.selectbox(
            "Indian City / Location *",
            INDIAN_CITIES,
            help="Select applicant's location"
        )

    # Employment and Income Row
    col5, col6 = st.columns(2)
    with col5:
        employment_type = st.selectbox(
            "Employment Type *",
            EMPLOYMENT_TYPES,
            help="Type of employment"
        )

    with col6:
        monthly_income = st.number_input(
            "Monthly Income (₹) *",
            min_value=0.0,
            value=50000.0,
            step=1000.0,
            help="Monthly income in Indian Rupees"
        )

    # Credit Score and Existing Liabilities Row
    col7, col8 = st.columns(2)
    with col7:
        credit_score = st.number_input(
            "Credit Score *",
            min_value=300,
            max_value=900,
            value=700,
            help="Credit score (300-900)"
        )

    with col8:
        existing_liabilities = st.number_input(
            "Existing Liabilities (₹)",
            min_value=0.0,
            value=0.0,
            step=10000.0,
            help="Total existing loans/debts in Indian Rupees"
        )

    # Loan Amount and Tenure Row
    col9, col10 = st.columns(2)
    with col9:
        loan_amount = st.number_input(
            "Loan Amount Required (₹) *",
            min_value=10000.0,
            value=500000.0,
            step=50000.0,
            help="Amount of loan required in Indian Rupees"
        )

    with col10:
        loan_tenure = st.number_input(
            "Loan Tenure (Months) *",
            min_value=6,
            max_value=360,
            value=60,
            step=6,
            help="Loan repayment period in months"
        )

    st.markdown('</div>', unsafe_allow_html=True)

    return {
        "applicant_id": applicant_id,
        "applicant_name": applicant_name,
        "age": age,
        "city": city,
        "employment_type": employment_type,
        "monthly_income": monthly_income,
        "credit_score": credit_score,
        "existing_liabilities": existing_liabilities,
        "loan_amount": loan_amount,
        "loan_tenure": loan_tenure
    }


def get_risk_level_color(risk_level):
    """Get color class based on risk level"""
    risk_level = str(risk_level).upper()
    if "LOW" in risk_level:
        return "risk-low"
    elif "MEDIUM" in risk_level:
        return "risk-medium"
    else:
        return "risk-high"


def get_risk_dot_class(risk_level):
    """Get dot class based on risk level"""
    risk_level = str(risk_level).upper()
    if "LOW" in risk_level:
        return "low"
    elif "MEDIUM" in risk_level:
        return "medium"
    else:
        return "high"


def display_applicant_profile_summary(report_data):
    """Display Applicant Profile Summary section"""
    st.markdown('<h3 class="section-header">👤 Applicant Profile Summary</h3>', unsafe_allow_html=True)

    applicant_profile = report_data.get("applicant_profile", {})
    applicant_info = report_data.get("applicant_info", {})

    # Profile Summary Cards
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.write(f"**📛 Applicant Name:** {applicant_info.get('name', 'N/A')}")
        st.write(f"**🆔 Applicant ID:** `{applicant_info.get('id', 'N/A')}`")
        st.write(f"**📅 Age:** {applicant_info.get('age', 'N/A')} years")
        st.write(f"**📍 City:** {applicant_info.get('city', 'N/A')}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.write(f"**💼 Employment Type:** {applicant_info.get('employment_type', 'N/A')}")
        st.write(f"**💰 Monthly Income:** ₹{applicant_info.get('monthly_income', 0):,.2f}")
        st.write(f"**📊 Credit Score:** {applicant_info.get('credit_score', 'N/A')}")
        st.write(f"**📈 Existing Liabilities:** ₹{applicant_info.get('existing_liabilities', 0):,.2f}")
        st.markdown('</div>', unsafe_allow_html=True)

    # Application Completeness Status
    st.markdown("**✓ Application Completeness Status:**")
    completeness_flags = applicant_profile.get("application_completeness_flags", [])

    if completeness_flags:
        cols = st.columns(len(completeness_flags) if len(completeness_flags) <= 3 else 3)
        for i, flag in enumerate(completeness_flags):
            with cols[i % 3]:
                if "✓" in flag or "complete" in flag.lower():
                    st.success(f"✅ {flag.replace('✓', '').strip()}")
                else:
                    st.warning(f"⚠️ {flag}")
    else:
        st.success("✓ Application is complete")

    # Income Stability and Employment Risk - Beautiful Cards
    col3, col4 = st.columns(2)

    with col3:
        income_stability = applicant_profile.get("income_stability_score", 0)
        stability_pct = (income_stability / 10) * 100
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">💼 Income Stability Score</div>
            <div class="metric-value">{income_stability:.1f}</div>
            <div class="metric-subtext">Out of 10</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<div class="progress-bar-container"><div class="progress-bar" style="width: {stability_pct}%;"></div></div>', unsafe_allow_html=True)

    with col4:
        employment_risk = applicant_profile.get("employment_risk", "N/A")
        risk_color = get_risk_level_color(employment_risk)
        risk_dot = get_risk_dot_class(employment_risk)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">⚠️ Employment Risk Level</div>
            <div class="metric-value" style="font-size: 1.8rem;">{employment_risk}</div>
            <div class="risk-indicator" style="justify-content: center; color: white; margin-top: 0.5rem;">
                <div class="risk-dot {risk_dot}"></div>
                <span>{employment_risk}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Credit History Summary
    st.markdown("---")
    st.markdown("**📋 Credit History Summary:**")
    credit_summary = applicant_profile.get("credit_history_summary", "No information available")
    st.markdown(f'<div class="info-card"><div class="info-card-text">{credit_summary}</div></div>', unsafe_allow_html=True)


def display_financial_risk_analysis(report_data):
    """Display Financial Risk Analysis section"""
    st.markdown('<h3 class="section-header">📊 Financial Risk Analysis</h3>', unsafe_allow_html=True)

    financial_risk = report_data.get("financial_risk", {})

    # Financial Metrics - Beautiful Dashboard Grid
    col1, col2, col3 = st.columns(3)

    with col1:
        dti_ratio = financial_risk.get("debt_to_income_ratio", 0)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">💳 Debt-to-Income Ratio</div>
            <div class="metric-value">{dti_ratio:.1%}</div>
            <div class="metric-subtext">Monthly debt / Monthly income</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        credit_risk = financial_risk.get("credit_score_risk_level", "N/A")
        risk_color = get_risk_level_color(credit_risk)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📈 Credit Score Risk</div>
            <div class="metric-value" style="font-size: 1.8rem;">{credit_risk}</div>
            <div class="metric-subtext">Risk assessment</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        loan_risk = financial_risk.get("loan_amount_risk", "N/A")
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🏦 Loan Amount Risk</div>
            <div class="metric-value" style="font-size: 1.8rem;">{loan_risk}</div>
            <div class="metric-subtext">Loan vs. income ratio</div>
        </div>
        """, unsafe_allow_html=True)

    # Anomaly Detection
    st.markdown("---")
    anomaly_detected = financial_risk.get("anomaly_detected", False)
    if anomaly_detected:
        st.markdown("""
        <div class="info-card" style="border-left: 5px solid #f45c43; background: linear-gradient(135deg, #f4554315 0%, #eb334915 100%);">
            <div class="info-card-text">⚠️ <strong>Anomaly Detected:</strong> Unusual financial patterns detected in the application</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-card" style="border-left: 5px solid #38ef7d; background: linear-gradient(135deg, #38ef7d15 0%, #11998e15 100%);">
            <div class="info-card-text">✓ <strong>No Anomalies Detected:</strong> Financial profile appears normal</div>
        </div>
        """, unsafe_allow_html=True)

    # Risk Reasoning
    st.markdown("---")
    st.markdown("**🔍 Financial Risk Analysis Reasoning:**")
    reasoning = financial_risk.get("reasoning", "No detailed reasoning available")
    st.markdown(f'<div class="info-card"><div class="info-card-text">{reasoning}</div></div>', unsafe_allow_html=True)


def display_loan_decision(report_data):
    """Display Loan Decision section"""
    st.markdown('<h3 class="section-header">💼 Loan Decision</h3>', unsafe_allow_html=True)

    decision = report_data.get("decision", {})
    classification = decision.get("classification", "UNKNOWN")

    # Decision Display with Beautiful Styling
    if classification == "APPROVED":
        st.markdown("""
        <div class="decision-banner status-approved">
            <h2>✅ APPLICATION APPROVED</h2>
            <p>Congratulations! Your loan application has been approved.</p>
        </div>
        """, unsafe_allow_html=True)
    elif classification == "REJECTED":
        st.markdown("""
        <div class="decision-banner status-rejected">
            <h2>❌ APPLICATION REJECTED</h2>
            <p>Unfortunately, your loan application has been rejected.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="decision-banner status-review">
            <h2>⚠️ REQUIRES MANUAL REVIEW</h2>
            <p>Your application requires further evaluation by our team.</p>
        </div>
        """, unsafe_allow_html=True)

    # Decision Metrics - Dashboard Grid
    col1, col2, col3 = st.columns(3)

    with col1:
        risk_score = decision.get("risk_score", 0)
        risk_pct = (risk_score / 100) * 100
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📊 Risk Score</div>
            <div class="metric-value">{risk_score:.1f}</div>
            <div class="metric-subtext">Out of 100</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<div class="progress-bar-container"><div class="progress-bar {get_risk_level_color("HIGH" if risk_score > 70 else "MEDIUM" if risk_score > 40 else "LOW")}" style="width: {risk_pct}%;"></div></div>', unsafe_allow_html=True)

    with col2:
        confidence = decision.get("confidence_level", 0) * 100
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🎯 Confidence Level</div>
            <div class="metric-value">{confidence:.0f}%</div>
            <div class="metric-subtext">Decision confidence</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<div class="progress-bar-container"><div class="progress-bar" style="width: {confidence}%;"></div></div>', unsafe_allow_html=True)

    with col3:
        status = "Active" if classification != "REJECTED" else "On Hold"
        status_badge = "badge-approved" if classification == "APPROVED" else "badge-rejected" if classification == "REJECTED" else "badge-review"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📌 Application Status</div>
            <div class="metric-value" style="font-size: 1.5rem;">{status}</div>
            <div class="metric-subtext" style="margin-top: 0.75rem;">
                <span class="badge {status_badge}">{classification}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Decision Explanation
    st.markdown("---")
    st.markdown("**📝 Decision Explanation:**")
    explanation = decision.get("explanation", "No explanation provided")
    st.markdown(f'<div class="info-card"><div class="info-card-text">{explanation}</div></div>', unsafe_allow_html=True)

    # Key Decision Factors
    st.markdown("---")
    st.markdown("**🔑 Key Decision Factors:**")
    factors = decision.get("key_decision_factors", [])
    if factors:
        st.markdown('<ul class="factor-list">', unsafe_allow_html=True)
        for factor in factors:
            st.markdown(f'<li>{factor}</li>', unsafe_allow_html=True)
        st.markdown('</ul>', unsafe_allow_html=True)
    else:
        st.write("No specific factors identified")


def display_compliance_summary(report_data):
    """Display Compliance and Audit Summary section"""
    st.markdown('<h3 class="section-header">✅ Compliance & Audit Summary</h3>', unsafe_allow_html=True)

    compliance = report_data.get("compliance", {})

    # Compliance Details - Beautiful Box
    st.markdown('<div class="compliance-box">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="compliance-row">
            <span class="compliance-label">🆔 Case ID:</span>
            <span class="compliance-value"><code>{compliance.get('case_id', 'N/A')}</code></span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="compliance-row">
            <span class="compliance-label">⏰ Timestamp:</span>
            <span class="compliance-value">{compliance.get('timestamp', 'N/A')}</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="compliance-row">
            <span class="compliance-label">✉️ Notification Status:</span>
            <span class="compliance-value">{'Sent ✓' if compliance.get('notification_sent', False) else 'Pending'}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="compliance-row">
            <span class="compliance-label">🎯 Action Taken:</span>
            <span class="compliance-value">{compliance.get('action_taken', 'N/A')}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Audit Summary
    st.markdown("---")
    st.markdown("**📋 Audit Summary:**")
    summary = compliance.get("summary", "No audit summary available")
    st.markdown(f'<div class="info-card"><div class="info-card-text">{summary}</div></div>', unsafe_allow_html=True)


def main():
    """Main application"""
    create_header()

    # Sidebar with System Information
    with st.sidebar:
        st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
        st.markdown("### 🤖 Multi-Agent System")
        st.markdown("""
        **Active Agents:**
        - 👤 Applicant Profile Agent
        - 📊 Financial Risk Agent
        - 💼 Loan Decision Agent
        - ✅ Compliance Agent

        **System Status:** ✅ Online
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    # Create form
    form_data = create_loan_application_form()

    # Submit Button with Beautiful Styling
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        submit_button = st.button(
            "🚀 Submit Application for AI Evaluation",
            use_container_width=True,
            type="primary",
            key="submit_btn"
        )

    if submit_button:
        # Validation
        errors = []
        if not form_data["applicant_id"].strip():
            errors.append("❌ Applicant ID is required")
        if not form_data["applicant_name"].strip():
            errors.append("❌ Applicant Name is required")
        if form_data["monthly_income"] <= 0:
            errors.append("❌ Monthly Income must be greater than 0")
        if form_data["loan_amount"] <= 0:
            errors.append("❌ Loan Amount must be greater than 0")

        if errors:
            for error in errors:
                st.error(error)
        else:
            # Process application
            with st.spinner("🔄 Processing through multi-agent system... Evaluating application..."):
                try:
                    # Prepare payload
                    payload = {
                        "applicant_id": form_data["applicant_id"],
                        "applicant_name": form_data["applicant_name"],
                        "age": form_data["age"],
                        "income": form_data["monthly_income"] * 12,  # Convert to annual
                        "monthly_income": form_data["monthly_income"],
                        "employment_type": form_data["employment_type"],
                        "credit_score": form_data["credit_score"],
                        "loan_amount": form_data["loan_amount"],
                        "tenure_months": form_data["loan_tenure"],
                        "existing_liabilities": form_data["existing_liabilities"],
                        "location": form_data["city"],
                        "city": form_data["city"],
                        "loan_type": "Personal Loan"
                    }

                    response = requests.post(
                        f"{API_URL}/evaluate-loan",
                        json=payload,
                        timeout=60
                    )

                    if response.status_code == 200:
                        result = response.json()
                        report = result.get("report", {})

                        # Add applicant info to report
                        report["applicant_info"] = {
                            "id": form_data["applicant_id"],
                            "name": form_data["applicant_name"],
                            "age": form_data["age"],
                            "city": form_data["city"],
                            "employment_type": form_data["employment_type"],
                            "monthly_income": form_data["monthly_income"],
                            "credit_score": form_data["credit_score"],
                            "existing_liabilities": form_data["existing_liabilities"]
                        }

                        st.markdown("---")
                        st.success("✅ Application evaluated successfully!")
                        st.markdown("---")

                        # Display Results Header
                        st.markdown("""
                        <div class="result-container">
                        <div style="text-align: center;">
                            <h2 style="color: #667eea; font-size: 2rem; margin-bottom: 0.5rem;">📊 LOAN EVALUATION REPORT</h2>
                            <p style="color: #667eea; font-size: 0.95rem;">AI-Powered Multi-Agent Analysis</p>
                        </div>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown('<div class="result-container">', unsafe_allow_html=True)

                        # Display all sections
                        display_applicant_profile_summary(report)
                        st.markdown("---")

                        display_financial_risk_analysis(report)
                        st.markdown("---")

                        display_loan_decision(report)
                        st.markdown("---")

                        display_compliance_summary(report)

                        st.markdown('</div>', unsafe_allow_html=True)

                        # Download Report
                        st.markdown("---")
                        st.markdown('<h3 class="section-header">📥 Download Report</h3>', unsafe_allow_html=True)

                        json_report = json.dumps(report, indent=2, default=str)

                        col_download1, col_download2, col_download3 = st.columns([1, 2, 1])
                        with col_download2:
                            st.download_button(
                                label="📋 Download Full Report (JSON)",
                                data=json_report,
                                file_name=f"loan_report_{form_data['applicant_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                                mime="application/json",
                                use_container_width=True
                            )

                    else:
                        st.error(f"❌ Error processing application: Status code {response.status_code}")
                        st.error(f"Response: {response.text}")

                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to API server. Ensure it's running on localhost:8000")
                except requests.exceptions.Timeout:
                    st.error("❌ Request timed out. Please try again.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
