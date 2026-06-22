from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableConfig
from models import LoanEvaluationState, LoanApplication
from agents.applicant_agent import ApplicantProfileAgent
from agents.financial_risk_agent import FinancialRiskAgent
from agents.decision_agent import LoanDecisionAgent
from agents.compliance_agent import ComplianceOrchestratorAgent


class LoanEvaluationOrchestrator:
    def __init__(self):
        self.applicant_agent = ApplicantProfileAgent()
        self.risk_agent = FinancialRiskAgent()
        self.decision_agent = LoanDecisionAgent()
        self.compliance_agent = ComplianceOrchestratorAgent()
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        """Build the LangGraph workflow."""
        workflow = StateGraph(LoanEvaluationState)

        workflow.add_node("evaluate_applicant", self._evaluate_applicant)
        workflow.add_node("analyze_risk", self._analyze_risk)
        workflow.add_node("make_decision", self._make_decision)
        workflow.add_node("handle_compliance", self._handle_compliance)

        workflow.set_entry_point("evaluate_applicant")
        workflow.add_edge("evaluate_applicant", "analyze_risk")
        workflow.add_edge("analyze_risk", "make_decision")
        workflow.add_edge("make_decision", "handle_compliance")

        return workflow.compile()

    def _evaluate_applicant(self, state: LoanEvaluationState):
        """Step 1: Evaluate applicant profile."""
        try:
            profile = self.applicant_agent.evaluate_applicant_profile(state.application)
            state.applicant_profile = profile
        except Exception as e:
            state.error = f"Applicant evaluation failed: {str(e)}"
        return state

    def _analyze_risk(self, state: LoanEvaluationState):
        """Step 2: Analyze financial risk."""
        try:
            if state.applicant_profile is None:
                state.error = "Applicant profile not available"
                return state

            risk = self.risk_agent.analyze_financial_risk(
                state.application,
                state.applicant_profile
            )
            state.financial_risk = risk
        except Exception as e:
            state.error = f"Risk analysis failed: {str(e)}"
        return state

    def _make_decision(self, state: LoanEvaluationState):
        """Step 3: Make loan decision."""
        try:
            if state.financial_risk is None or state.applicant_profile is None:
                state.error = "Required data for decision not available"
                return state

            decision = self.decision_agent.make_decision(
                state.application,
                state.applicant_profile,
                state.financial_risk
            )
            state.decision = decision
        except Exception as e:
            state.error = f"Decision making failed: {str(e)}"
        return state

    def _handle_compliance(self, state: LoanEvaluationState):
        """Step 4: Handle compliance and notifications."""
        try:
            if state.decision is None:
                state.error = "Decision not available for compliance"
                return state

            compliance = self.compliance_agent.handle_compliance(
                state.application,
                state.decision
            )
            state.compliance = compliance
        except Exception as e:
            state.error = f"Compliance handling failed: {str(e)}"
        return state

    def evaluate_loan(self, application: LoanApplication) -> LoanEvaluationState:
        """Execute the complete evaluation workflow."""
        initial_state = LoanEvaluationState(application=application)
        result_dict = self.workflow.invoke(initial_state)
        return LoanEvaluationState(**result_dict)
