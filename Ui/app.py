"""
GEN-AI Case Study Evaluator - Streamlit Web Interface
Evaluates Agentic AI Intelligent Loan Approval System case study submissions
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
    page_title="GEN-AI Case Study Evaluator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = "http://localhost:8000"

# Custom CSS
st.markdown("""
    <style>
    .main { padding: 2rem; }
    .stTabs [data-baseweb="tab-list"] button { font-size: 16px; }
    .stProgress { margin: 20px 0; }
    .metric-box {
        padding: 20px;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    .score-excellent { color: #27ae60; font-weight: bold; font-size: 24px; }
    .score-good { color: #3498db; font-weight: bold; font-size: 24px; }
    .score-average { color: #f39c12; font-weight: bold; font-size: 24px; }
    .score-needs-improvement { color: #e74c3c; font-weight: bold; font-size: 24px; }
    .dimension-score {
        padding: 15px;
        margin: 10px 0;
        border-left: 5px solid #3498db;
        background: #ecf0f1;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)


def get_score_color(score):
    """Return color class based on score"""
    if score >= 9:
        return "score-excellent"
    elif score >= 7:
        return "score-good"
    elif score >= 5:
        return "score-average"
    else:
        return "score-needs-improvement"


def evaluate_submission(participant_name: str, submission_path: str):
    """Send submission to API for evaluation"""
    try:
        response = requests.post(
            f"{API_URL}/evaluate-submission",
            params={
                "participant_name": participant_name,
                "submission_path": submission_path
            },
            timeout=60
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to API server. Ensure it's running on localhost:8000"}
    except requests.exceptions.Timeout:
        return {"error": "API request timed out. The evaluation might still be processing."}
    except requests.exceptions.RequestException as e:
        return {"error": f"API Error: {str(e)}"}


def display_completion_check(completion_data):
    """Display submission completeness check results"""
    st.subheader("📋 Submission Completeness Check")

    is_complete = completion_data["is_complete"]
    status_color = "🟢" if is_complete else "🔴"
    status_text = "✓ COMPLETE" if is_complete else "✗ INCOMPLETE"

    col1, col2 = st.columns([1, 3])
    with col1:
        st.metric("Status", status_text, delta="All components present" if is_complete else "Missing components")
    with col2:
        st.info(f"**{status_color} {status_text}** - {len(completion_data['found_components'])}/10 components found")

    # Show found components
    if completion_data["found_components"]:
        st.markdown("**✓ Found Components:**")
        cols = st.columns(2)
        for i, component in enumerate(completion_data["found_components"]):
            with cols[i % 2]:
                st.checkbox(component, value=True, disabled=True, key=f"found_{i}")

    # Show missing components
    if completion_data["missing_components"]:
        st.warning("**✗ Missing Components:**")
        for component in completion_data["missing_components"]:
            st.write(f"• {component}")


def display_dimension_scores(dimension_scores):
    """Display individual dimension scores"""
    st.subheader("📊 Detailed Dimension Scores")

    dimensions_col1, dimensions_col2 = st.columns([1, 2])

    with dimensions_col1:
        st.markdown("**Scores Summary:**")
        scores_dict = {}
        for score in dimension_scores:
            scores_dict[score["name"]] = score["score"]

        for name, score in scores_dict.items():
            color = "🟢" if score >= 7 else "🟡" if score >= 5 else "🔴"
            st.write(f"{color} {name}: **{score}/10**")

    with dimensions_col2:
        st.markdown("**Detailed Remarks:**")
        for score in dimension_scores:
            with st.expander(f"📝 {score['name']} ({score['score']}/10)"):
                st.write(score["remarks"])


def display_evaluation_summary(report_data):
    """Display evaluation summary table"""
    st.subheader("📈 Evaluation Summary Table")

    summary_data = {
        "Dimension": [],
        "Score": [],
        "Grade": []
    }

    for score in report_data["dimension_scores"]:
        summary_data["Dimension"].append(score["name"])
        summary_data["Score"].append(f"{score['score']}/10")
        if score["score"] >= 7:
            summary_data["Grade"].append("✓ Good")
        elif score["score"] >= 5:
            summary_data["Grade"].append("⚠ Average")
        else:
            summary_data["Grade"].append("✗ Needs Work")

    st.table(summary_data)


def display_recommendations(report_data):
    """Display final recommendations"""
    st.subheader("💡 Final Recommendations")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.expander("✨ Strengths to Highlight", expanded=False):
            for i, strength in enumerate(report_data["strengths"], 1):
                st.write(f"{i}. {strength}")

    with col2:
        with st.expander("🎯 Areas for Improvement", expanded=False):
            for i, improvement in enumerate(report_data["improvements"], 1):
                st.write(f"{i}. {improvement}")

    with col3:
        with st.expander("📚 Learning Outcomes", expanded=False):
            for i, outcome in enumerate(report_data["learning_outcomes"], 1):
                st.write(f"{i}. {outcome}")

    # Final Verdict
    st.markdown("---")
    st.info(f"**Final Verdict:** {report_data['final_verdict']}")


def main():
    # Header
    st.title("🎓 GEN-AI Case Study Evaluator")
    st.markdown(
        """
        Comprehensive evaluation system for **Agentic AI Intelligent Loan Approval System**
        case study submissions. Evaluates submissions across 7 dimensions with detailed scoring
        and recommendations.
        """
    )
    st.markdown("---")

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📝 Evaluate Submission", "📚 Guide", "ℹ️ About"])

    # Tab 1: Evaluate Submission
    with tab1:
        st.header("Evaluate Case Study Submission")

        col1, col2 = st.columns(2)

        with col1:
            participant_name = st.text_input(
                "Participant Name",
                placeholder="Enter participant's full name",
                help="Name of the person/team submitting the case study"
            )

        with col2:
            submission_path = st.text_input(
                "Submission Path",
                placeholder="/path/to/submission",
                value=".",
                help="Full path to the submission directory (e.g., . for current, ./submission, /home/user/work)"
            )

        st.markdown("---")

        # Evaluation button
        if st.button("🚀 Run Evaluation", use_container_width=True, type="primary"):
            if not participant_name.strip():
                st.error("❌ Please enter participant name")
                return

            if not submission_path.strip():
                st.error("❌ Please enter submission path")
                return

            # Validate path exists
            path_obj = Path(submission_path)
            if not path_obj.exists():
                st.error(f"❌ Path does not exist: {submission_path}")
                return

            if not path_obj.is_dir():
                st.error(f"❌ Path is not a directory: {submission_path}")
                return

            with st.spinner("🔄 Evaluating submission... This may take a moment."):
                result = evaluate_submission(participant_name, submission_path)

            if "error" in result:
                st.error(f"❌ Error: {result['error']}")
                return

            # Successfully evaluated
            report = result.get("report", {})

            # Summary metrics
            st.markdown("---")
            st.markdown("## 📊 Evaluation Results")

            col_score, col_grade, col_status = st.columns(3)

            with col_score:
                score_class = get_score_color(report["overall_score"])
                st.markdown(
                    f'<div style="text-align: center; padding: 20px; background: #f0f0f0; border-radius: 10px;"> '
                    f'<div style="font-size: 14px; color: #666;">Overall Score</div> '
                    f'<div class="{score_class}">{report["overall_score"]}/10</div> '
                    f'</div>',
                    unsafe_allow_html=True
                )

            with col_grade:
                grade_colors = {
                    "Excellent": "#27ae60",
                    "Good": "#3498db",
                    "Average": "#f39c12",
                    "Needs Improvement": "#e74c3c"
                }
                grade_color = grade_colors.get(report["grade"], "#95a5a6")
                st.markdown(
                    f'<div style="text-align: center; padding: 20px; background: #f0f0f0; border-radius: 10px;"> '
                    f'<div style="font-size: 14px; color: #666;">Grade</div> '
                    f'<div style="font-size: 24px; font-weight: bold; color: {grade_color};">{report["grade"]}</div> '
                    f'</div>',
                    unsafe_allow_html=True
                )

            with col_status:
                status_emoji = "✅" if report["status"] == "Pass" else "⚠️"
                st.markdown(
                    f'<div style="text-align: center; padding: 20px; background: #f0f0f0; border-radius: 10px;"> '
                    f'<div style="font-size: 14px; color: #666;">Status</div> '
                    f'<div style="font-size: 24px; font-weight: bold;">{status_emoji} {report["status"]}</div> '
                    f'</div>',
                    unsafe_allow_html=True
                )

            st.markdown("---")

            # Display sections
            display_completion_check(report["completion_check"])
            st.markdown("---")

            display_dimension_scores(report["dimension_scores"])
            st.markdown("---")

            display_evaluation_summary(report)
            st.markdown("---")

            display_recommendations(report)

            # Download report
            st.markdown("---")
            st.subheader("📥 Download Report")

            markdown_report = result.get("markdown", "")
            json_report = json.dumps(report, indent=2)

            col_md, col_json = st.columns(2)

            with col_md:
                st.download_button(
                    label="📄 Download as Markdown",
                    data=markdown_report,
                    file_name=f"evaluation_{participant_name.lower().replace(' ', '_')}.md",
                    mime="text/markdown"
                )

            with col_json:
                st.download_button(
                    label="📋 Download as JSON",
                    data=json_report,
                    file_name=f"evaluation_{participant_name.lower().replace(' ', '_')}.json",
                    mime="application/json"
                )

    # Tab 2: Guide
    with tab2:
        st.header("📚 Evaluator Guide")

        st.markdown("""
        ### How to Use the Evaluator

        1. **Enter Participant Name**: Full name of the person/team submitting
        2. **Enter Submission Path**: Path to the submission directory
        3. **Run Evaluation**: Click the evaluation button
        4. **Review Results**: See detailed scores and recommendations
        5. **Download Report**: Export as Markdown or JSON

        ### What Gets Evaluated

        The evaluator checks for 10 required components:
        - Business understanding of loan approval problem
        - Multi-agent / Agentic AI architecture
        - Streamlit-based UI or equivalent
        - FastAPI-based API layer or equivalent
        - LangGraph orchestration or equivalent
        - MCP-based agent communication or equivalent
        - Applicant Profile Agent
        - Financial Risk Analysis Agent
        - Loan Decision Agent
        - Compliance & Action Orchestrator Agent

        ### Scoring Dimensions

        1. **Business Understanding** (0-10)
        2. **Architecture Quality** (0-10)
        3. **Agent Design Quality** (0-10)
        4. **Workflow Clarity** (0-10)
        5. **Explainability & Auditability** (0-10)
        6. **Implementation Readiness** (0-10)
        7. **Technology Stack** (0-10)

        ### Score Ranges

        - **9-10 (Excellent)**: Strong alignment, clear design, correct orchestration
        - **7-8 (Good)**: Mostly complete, minor gaps
        - **5-6 (Average)**: Partial understanding, some gaps
        - **0-4 (Needs Improvement)**: Major gaps, incomplete design

        ### Example Usage

        ```
        Participant Name: John Doe
        Submission Path: /home/user/submissions/john_doe
        ```

        For detailed information, see EVALUATOR_GUIDE.md
        """)

    # Tab 3: About
    with tab3:
        st.header("ℹ️ About This System")

        st.markdown("""
        ### GEN-AI Case Study Evaluator v2.0

        A comprehensive evaluation system for the **Agentic AI Intelligent Loan Approval System**
        case study submissions.

        #### Features
        - ✅ Automated completeness checking
        - ✅ Multi-dimensional scoring
        - ✅ Detailed recommendations
        - ✅ Markdown and JSON export
        - ✅ Evidence-based evaluation

        #### Technologies
        - **Framework**: Streamlit (UI), FastAPI (API)
        - **Evaluation Engine**: Python with AST analysis
        - **Report Generation**: Markdown & JSON

        #### System Architecture
        - FastAPI server running on port 8000
        - Streamlit UI on port 8501
        - Standalone evaluator module

        #### Documentation
        - See `EVALUATOR_GUIDE.md` for detailed evaluation criteria
        - See `IMPLEMENTATION_NOTES.md` for technical details
        - See `/docs` for API documentation

        #### Contact
        For issues or questions about the evaluator system, refer to the
        comprehensive EVALUATOR_GUIDE.md file.
        """)

        # System Status
        st.markdown("---")
        st.subheader("🔧 System Status")

        try:
            health_response = requests.get(f"{API_URL}/health", timeout=5)
            if health_response.status_code == 200:
                st.success("✅ API Server: Connected")
            else:
                st.error("❌ API Server: Unreachable")
        except:
            st.error("❌ API Server: Not running")

        st.info("For more information, visit: http://localhost:8000/docs")


if __name__ == "__main__":
    main()
