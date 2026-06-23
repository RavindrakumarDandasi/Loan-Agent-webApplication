"""
Evaluator module for GEN-AI Case Study submissions.
Implements the 5-step evaluation framework from the evaluator prompt.
"""

import os
import re
import ast
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class GradeLevel(Enum):
    EXCELLENT = "Excellent"
    GOOD = "Good"
    AVERAGE = "Average"
    NEEDS_IMPROVEMENT = "Needs Improvement"


class EvaluationStatus(Enum):
    PASS = "Pass"
    NEEDS_REWORK = "Needs Rework"


@dataclass
class CompletionCheckResult:
    """Result of submission completeness check"""
    is_complete: bool
    missing_components: List[str]
    found_components: List[str]


@dataclass
class DimensionScore:
    """Score for a single evaluation dimension"""
    name: str
    score: float
    remarks: str


@dataclass
class EvaluationReport:
    """Structured evaluation report"""
    participant_name: str
    case_study: str
    date: str
    overall_score: float
    grade: str
    status: str
    completion_check: CompletionCheckResult
    dimension_scores: List[DimensionScore]
    strengths: List[str]
    improvements: List[str]
    learning_outcomes: List[str]
    final_verdict: str

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            "participant_name": self.participant_name,
            "case_study": self.case_study,
            "date": self.date,
            "overall_score": self.overall_score,
            "grade": self.grade,
            "status": self.status,
            "completion_check": {
                "is_complete": self.completion_check.is_complete,
                "missing_components": self.completion_check.missing_components,
                "found_components": self.completion_check.found_components,
            },
            "dimension_scores": [asdict(score) for score in self.dimension_scores],
            "strengths": self.strengths,
            "improvements": self.improvements,
            "learning_outcomes": self.learning_outcomes,
            "final_verdict": self.final_verdict,
        }

    def to_markdown(self) -> str:
        """Generate markdown-formatted report"""
        lines = []

        # Header
        lines.append("# GEN-AI Case Study – Executive Summary Report")
        lines.append("")

        # Details of Submission
        lines.append("## Details of Submission")
        lines.append(f"**Participant:** {self.participant_name}")
        lines.append(f"**Case Study:** {self.case_study}")
        lines.append(f"**Date:** {self.date}")
        lines.append(f"**Overall Score:** {self.overall_score}/10")
        lines.append(f"**Grade:** {self.grade}")
        lines.append(f"**Status:** {self.status}")
        lines.append("")

        # Completion Check
        lines.append("## Submission Completeness")
        lines.append(f"**Complete:** {'Yes' if self.completion_check.is_complete else 'No'}")
        if self.completion_check.found_components:
            lines.append(f"**Found Components ({len(self.completion_check.found_components)}):**")
            for component in self.completion_check.found_components:
                lines.append(f"  - ✓ {component}")
        if self.completion_check.missing_components:
            lines.append(f"**Missing Components ({len(self.completion_check.missing_components)}):**")
            for component in self.completion_check.missing_components:
                lines.append(f"  - ✗ {component}")
        lines.append("")

        # Evaluation Summary Table
        lines.append("## Evaluation Summary Table")
        lines.append("")
        lines.append("|Submission Complete|Business Understanding|Architecture Quality|Agent Design Quality|Workflow Clarity|Explainability & Auditability|Implementation Readiness|Score|Key Remarks|")
        lines.append("|---|---|---|---|---|---|---|---|---|")

        complete_status = "Yes" if self.completion_check.is_complete else "No"
        remarks = "Submission " + ("complete and evaluated" if self.completion_check.is_complete else "incomplete - evaluation limited")

        bu_score = next((s.score for s in self.dimension_scores if s.name == "Business Understanding"), 0)
        arch_score = next((s.score for s in self.dimension_scores if s.name == "Architecture Quality"), 0)
        agent_score = next((s.score for s in self.dimension_scores if s.name == "Agent Design Quality"), 0)
        workflow_score = next((s.score for s in self.dimension_scores if s.name == "Workflow Clarity"), 0)
        explain_score = next((s.score for s in self.dimension_scores if s.name == "Explainability & Auditability"), 0)
        impl_score = next((s.score for s in self.dimension_scores if s.name == "Implementation Readiness"), 0)

        lines.append(f"|{complete_status}|{bu_score}|{arch_score}|{agent_score}|{workflow_score}|{explain_score}|{impl_score}|{self.overall_score}|{remarks}|")
        lines.append("")

        # Dimension Scores
        lines.append("## Detailed Dimension Scores")
        for score in self.dimension_scores:
            lines.append(f"### {score.name}: {score.score}/10")
            lines.append(f"{score.remarks}")
            lines.append("")

        # Final Recommendations
        lines.append("## Final Recommendations for Participant")
        lines.append("")

        lines.append("### Strengths to Highlight")
        for strength in self.strengths:
            lines.append(f"- {strength}")
        lines.append("")

        lines.append("### Areas for Improvement")
        for improvement in self.improvements:
            lines.append(f"- {improvement}")
        lines.append("")

        lines.append("### Learning Outcomes Demonstrated")
        for outcome in self.learning_outcomes:
            lines.append(f"- {outcome}")
        lines.append("")

        lines.append("### Final Verdict on Solution Quality")
        lines.append(self.final_verdict)
        lines.append("")

        return "\n".join(lines)


class SubmissionAnalyzer:
    """Analyzes submission files to identify components"""

    def __init__(self, submission_path: str):
        self.submission_path = Path(submission_path)
        self.py_files = list(self.submission_path.rglob("*.py"))
        self.md_files = list(self.submission_path.rglob("*.md"))
        self.txt_files = list(self.submission_path.rglob("*.txt"))

    def find_python_classes(self, filename: str) -> List[str]:
        """Extract class names from a Python file"""
        try:
            file_path = self._find_file(filename)
            if not file_path:
                return []
            with open(file_path, 'r') as f:
                tree = ast.parse(f.read())
            return [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        except:
            return []

    def find_python_functions(self, filename: str) -> List[str]:
        """Extract function names from a Python file"""
        try:
            file_path = self._find_file(filename)
            if not file_path:
                return []
            with open(file_path, 'r') as f:
                tree = ast.parse(f.read())
            return [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        except:
            return []

    def _find_file(self, filename: str) -> Optional[Path]:
        """Find a file in submission directory"""
        for py_file in self.py_files:
            if filename.lower() in py_file.name.lower():
                return py_file
        return None

    def file_contains_text(self, text: str, exclude_files: List[str] = None) -> bool:
        """Check if any file contains the given text"""
        exclude_files = exclude_files or []
        search_files = self.py_files + self.md_files + self.txt_files

        for file in search_files:
            if any(exclude in file.name for exclude in exclude_files):
                continue
            try:
                with open(file, 'r', errors='ignore') as f:
                    content = f.read()
                    if text.lower() in content.lower():
                        return True
            except:
                pass
        return False

    def has_file_pattern(self, pattern: str) -> bool:
        """Check if any file matches the pattern"""
        search_files = self.py_files + self.md_files + self.txt_files
        regex = re.compile(pattern, re.IGNORECASE)
        return any(regex.search(file.name) for file in search_files)


class SubmissionEvaluator:
    """Main evaluator for GEN-AI case study submissions"""

    REQUIRED_COMPONENTS = [
        "Business understanding of the loan approval problem",
        "Multi-agent / Agentic AI architecture",
        "Streamlit-based chatbot UI or equivalent user interaction layer",
        "FastAPI-based microservice layer or equivalent API handling layer",
        "LangGraph-based orchestration or equivalent workflow/state management",
        "MCP-based agent communication or equivalent standardized agent communication",
        "Applicant Profile Agent",
        "Financial Risk Analysis Agent",
        "Loan Decision Agent",
        "Compliance & Action Orchestrator Agent",
    ]

    def __init__(self):
        self.analyzer = None

    def evaluate(self, submission_path: str, participant_name: str = None) -> EvaluationReport:
        """Run complete evaluation of a submission"""

        if not participant_name:
            participant_name = "Not Provided"

        self.analyzer = SubmissionAnalyzer(submission_path)

        # Step 1: Completeness Check
        completion_result = self._check_completeness()

        if not completion_result.is_complete:
            # Return incomplete submission with 0 score
            return self._create_incomplete_report(participant_name, completion_result)

        # Step 2: Evaluate dimensions
        dimension_scores = self._evaluate_dimensions()

        # Calculate overall score
        overall_score = sum(score.score for score in dimension_scores) / len(dimension_scores)
        overall_score = round(overall_score)

        # Determine grade and status
        grade = self._get_grade(overall_score)
        status = "Pass" if overall_score >= 7 else "Needs Rework"

        # Generate recommendations
        strengths, improvements, learning_outcomes, verdict = self._generate_recommendations(
            dimension_scores, overall_score
        )

        return EvaluationReport(
            participant_name=participant_name,
            case_study="Agentic AI Intelligent Loan Approval System",
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            overall_score=overall_score,
            grade=grade,
            status=status,
            completion_check=completion_result,
            dimension_scores=dimension_scores,
            strengths=strengths,
            improvements=improvements,
            learning_outcomes=learning_outcomes,
            final_verdict=verdict,
        )

    def _check_completeness(self) -> CompletionCheckResult:
        """Check if submission includes all required components"""
        found = []
        missing = []

        for component in self.REQUIRED_COMPONENTS:
            if self._has_component(component):
                found.append(component)
            else:
                missing.append(component)

        is_complete = len(missing) == 0

        return CompletionCheckResult(
            is_complete=is_complete,
            missing_components=missing,
            found_components=found,
        )

    def _has_component(self, component: str) -> bool:
        """Check if submission has a specific component"""
        component_lower = component.lower()

        # Business understanding
        if "business understanding" in component_lower:
            return self.analyzer.file_contains_text("loan approval") or \
                   self.analyzer.file_contains_text("loan application") or \
                   self.analyzer.file_contains_text("README")

        # Multi-agent / Agentic AI architecture
        if "multi-agent" in component_lower or "agentic" in component_lower:
            return self.analyzer.file_contains_text("agent") and \
                   (self.analyzer.file_contains_text("orchestrat") or \
                    self.analyzer.file_contains_text("workflow"))

        # Streamlit UI
        if "streamlit" in component_lower or "chatbot ui" in component_lower:
            return self.analyzer.file_contains_text("streamlit") or \
                   self.analyzer.has_file_pattern(r"app\.py|ui\.py") or \
                   self.analyzer.file_contains_text("st.")

        # FastAPI API
        if "fastapi" in component_lower or "api handling" in component_lower:
            return self.analyzer.file_contains_text("fastapi") or \
                   self.analyzer.file_contains_text("@app") or \
                   self.analyzer.file_contains_text("uvicorn")

        # LangGraph orchestration
        if "langgraph" in component_lower or "orchestration" in component_lower:
            return self.analyzer.file_contains_text("langgraph") or \
                   self.analyzer.file_contains_text("StateGraph") or \
                   self.analyzer.file_contains_text("orchestrat")

        # MCP communication
        if "mcp" in component_lower or "agent communication" in component_lower:
            return self.analyzer.file_contains_text("mcp") or \
                   self.analyzer.file_contains_text("message") or \
                   self.analyzer.file_contains_text("tool")

        # Specific agents
        if "applicant" in component_lower and "agent" in component_lower:
            return self.analyzer.file_contains_text("applicant") and \
                   (self.analyzer.file_contains_text("agent") or \
                    self.analyzer.file_contains_text("profile"))

        if "financial" in component_lower and "risk" in component_lower:
            return self.analyzer.file_contains_text("financial") and \
                   (self.analyzer.file_contains_text("risk") or \
                    self.analyzer.file_contains_text("dti") or \
                    self.analyzer.file_contains_text("credit"))

        if "decision" in component_lower and "agent" in component_lower:
            return self.analyzer.file_contains_text("decision") and \
                   (self.analyzer.file_contains_text("approve") or \
                    self.analyzer.file_contains_text("reject") or \
                    self.analyzer.file_contains_text("review"))

        if "compliance" in component_lower:
            return self.analyzer.file_contains_text("compliance") or \
                   self.analyzer.file_contains_text("notification") or \
                   self.analyzer.file_contains_text("audit")

        return False

    def _evaluate_dimensions(self) -> List[DimensionScore]:
        """Evaluate submission across all dimensions"""
        scores = []

        # Business Understanding
        bu_score = self._evaluate_business_understanding()
        scores.append(DimensionScore(
            name="Business Understanding",
            score=bu_score,
            remarks=f"Solution demonstrates understanding of loan approval automation, decision speed/consistency, and explainability requirements." if bu_score >= 7 else "Limited business context or problem understanding."
        ))

        # Architecture Quality
        arch_score = self._evaluate_architecture()
        scores.append(DimensionScore(
            name="Architecture Quality",
            score=arch_score,
            remarks=f"Architecture shows proper multi-agent decomposition with clear separation of concerns." if arch_score >= 7 else "Architecture lacks clarity in agent decomposition or separation of concerns."
        ))

        # Agent Design Quality
        agent_score = self._evaluate_agent_design()
        scores.append(DimensionScore(
            name="Agent Design Quality",
            score=agent_score,
            remarks=f"All four required agents properly designed with clear responsibilities." if agent_score >= 7 else "Agent design missing clarity or incomplete agent implementations."
        ))

        # Workflow Clarity
        workflow_score = self._evaluate_workflow_clarity()
        scores.append(DimensionScore(
            name="Workflow Clarity",
            score=workflow_score,
            remarks=f"Workflow path from input to decision is clear and well-documented." if workflow_score >= 7 else "Workflow coordination or orchestration logic unclear."
        ))

        # Explainability & Auditability
        explain_score = self._evaluate_explainability()
        scores.append(DimensionScore(
            name="Explainability & Auditability",
            score=explain_score,
            remarks=f"Solution provides clear decision explanations and audit trails." if explain_score >= 7 else "Limited explainability or audit trail capabilities."
        ))

        # Implementation Readiness
        impl_score = self._evaluate_implementation_readiness()
        scores.append(DimensionScore(
            name="Implementation Readiness",
            score=impl_score,
            remarks=f"Implementation appears feasible and technically sound." if impl_score >= 7 else "Implementation details unclear or architectural feasibility questionable."
        ))

        # Technology Stack
        tech_score = self._evaluate_tech_stack()
        scores.append(DimensionScore(
            name="Technology Stack",
            score=tech_score,
            remarks=f"Appropriate tools meaningfully applied to solution." if tech_score >= 7 else "Technology choices unclear or superficially applied."
        ))

        return scores

    def _evaluate_business_understanding(self) -> float:
        """Evaluate business understanding dimension"""
        score = 5.0

        if self.analyzer.file_contains_text("loan"):
            score += 1.0
        if self.analyzer.file_contains_text("approve") or self.analyzer.file_contains_text("reject"):
            score += 1.0
        if self.analyzer.file_contains_text("risk") or self.analyzer.file_contains_text("credit"):
            score += 0.5
        if self.analyzer.file_contains_text("automat"):
            score += 0.5
        if self.analyzer.file_contains_text("decision") and self.analyzer.file_contains_text("explainable"):
            score += 1.0

        return min(10, score)

    def _evaluate_architecture(self) -> float:
        """Evaluate architecture quality dimension"""
        score = 5.0

        if self.analyzer.file_contains_text("agent"):
            score += 1.0
        if self.analyzer.file_contains_text("orchestrat"):
            score += 1.0
        if self.analyzer.file_contains_text("microservice") or self.analyzer.file_contains_text("api"):
            score += 1.0
        if self.analyzer.file_contains_text("ui") or self.analyzer.file_contains_text("interface"):
            score += 0.5
        if self.analyzer.file_contains_text("separation") or self.analyzer.file_contains_text("loose"):
            score += 0.5

        return min(10, score)

    def _evaluate_agent_design(self) -> float:
        """Evaluate agent design quality dimension"""
        score = 5.0

        agents_found = 0
        required_agents = [
            ("applicant", "agent"),
            ("financial", "risk"),
            ("decision", "agent"),
            ("compliance", "orchestrat"),
        ]

        for term1, term2 in required_agents:
            if self.analyzer.file_contains_text(term1) and self.analyzer.file_contains_text(term2):
                agents_found += 1

        score += agents_found * 1.25

        if self.analyzer.file_contains_text("responsibility"):
            score += 0.5

        return min(10, score)

    def _evaluate_workflow_clarity(self) -> float:
        """Evaluate workflow clarity dimension"""
        score = 5.0

        if self.analyzer.file_contains_text("orchestrat"):
            score += 1.5
        if self.analyzer.file_contains_text("state"):
            score += 1.0
        if self.analyzer.file_contains_text("flow") or self.analyzer.file_contains_text("routing"):
            score += 1.0
        if self.analyzer.file_contains_text("error") or self.analyzer.file_contains_text("fallback"):
            score += 0.5

        return min(10, score)

    def _evaluate_explainability(self) -> float:
        """Evaluate explainability & auditability dimension"""
        score = 5.0

        if self.analyzer.file_contains_text("explain"):
            score += 1.5
        if self.analyzer.file_contains_text("audit") or self.analyzer.file_contains_text("trace"):
            score += 1.5
        if self.analyzer.file_contains_text("reason"):
            score += 1.0
        if self.analyzer.file_contains_text("confidence") or self.analyzer.file_contains_text("score"):
            score += 0.5

        return min(10, score)

    def _evaluate_implementation_readiness(self) -> float:
        """Evaluate implementation readiness dimension"""
        score = 5.0

        if self.analyzer.py_files:
            score += 1.0
        if len(self.analyzer.py_files) > 5:
            score += 1.0
        if self.analyzer.file_contains_text("def "):
            score += 1.0
        if self.analyzer.file_contains_text("class"):
            score += 0.5
        if self.analyzer.file_contains_text("import") or self.analyzer.file_contains_text("from"):
            score += 0.5

        return min(10, score)

    def _evaluate_tech_stack(self) -> float:
        """Evaluate technology stack dimension"""
        score = 5.0

        tech_keywords = ["fastapi", "streamlit", "langgraph", "langchain", "python", "anthropic", "claude"]
        tech_found = sum(1 for keyword in tech_keywords if self.analyzer.file_contains_text(keyword))

        score += min(tech_found * 0.75, 3.0)

        if self.analyzer.file_contains_text("pydantic"):
            score += 0.5
        if self.analyzer.file_contains_text("model"):
            score += 0.5

        return min(10, score)

    def _get_grade(self, score: float) -> str:
        """Get letter grade from numeric score"""
        if score >= 9:
            return GradeLevel.EXCELLENT.value
        elif score >= 7:
            return GradeLevel.GOOD.value
        elif score >= 5:
            return GradeLevel.AVERAGE.value
        else:
            return GradeLevel.NEEDS_IMPROVEMENT.value

    def _create_incomplete_report(self, participant_name: str, completion: CompletionCheckResult) -> EvaluationReport:
        """Create report for incomplete submission"""
        return EvaluationReport(
            participant_name=participant_name,
            case_study="Agentic AI Intelligent Loan Approval System",
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            overall_score=0,
            grade=GradeLevel.NEEDS_IMPROVEMENT.value,
            status=EvaluationStatus.NEEDS_REWORK.value,
            completion_check=completion,
            dimension_scores=[],
            strengths=[],
            improvements=[f"Missing: {comp}" for comp in completion.missing_components],
            learning_outcomes=[],
            final_verdict="Submission is incomplete and cannot be fully evaluated. Please provide all required components and resubmit.",
        )

    def _generate_recommendations(self, scores: List[DimensionScore], overall_score: float) -> Tuple[List[str], List[str], List[str], str]:
        """Generate recommendations based on evaluation results"""
        strengths = []
        improvements = []
        learning_outcomes = []

        # Identify strengths
        for score in scores:
            if score.score >= 8:
                strengths.append(f"Strong {score.name}: {score.score}/10")
            elif score.score >= 7:
                strengths.append(f"Good {score.name}: {score.score}/10")

        # Identify improvements
        for score in scores:
            if score.score < 7:
                improvements.append(f"Enhance {score.name} (current: {score.score}/10)")

        # Learning outcomes
        if overall_score >= 7:
            learning_outcomes = [
                "Demonstrates understanding of multi-agent system design patterns",
                "Shows competency in orchestration and state management",
                "Exhibits awareness of explainability and auditability requirements",
                "Able to design scalable, loosely-coupled microservices architecture",
            ]
        else:
            learning_outcomes = [
                "Foundational understanding of agentic AI concepts",
                "Exposure to multi-agent workflow design",
                "Awareness of case study requirements",
            ]

        # Final verdict
        if overall_score >= 9:
            verdict = "Excellent submission demonstrating comprehensive understanding of agentic AI patterns, multi-agent orchestration, and enterprise-ready design principles. Ready for production discussion."
        elif overall_score >= 7:
            verdict = "Good submission with solid understanding of multi-agent architecture and loan approval domain. Minor refinements needed for implementation readiness."
        elif overall_score >= 5:
            verdict = "Partial understanding demonstrated. Significant areas require clarification and enhancement before implementation."
        else:
            verdict = "Submission requires substantial rework. Core concepts need reinforcement. Please address missing components and resubmit."

        return strengths, improvements, learning_outcomes, verdict
