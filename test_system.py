#!/usr/bin/env python3
import json
from datetime import datetime
from models import LoanApplication, EmploymentType, DecisionEnum
from orchestration.orchestrator import LoanEvaluationOrchestrator


def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def test_agent_workflow():
    """Test the complete agent workflow."""
    print_section("TEST 1: Complete Loan Evaluation Workflow")

    orchestrator = LoanEvaluationOrchestrator()

    test_cases = [
        {
            "name": "Good Applicant (Should Approve)",
            "applicant_id": "APP001",
            "age": 35,
            "income": 100000,
            "employment_type": EmploymentType.SALARIED,
            "credit_score": 780,
            "loan_amount": 100000,
            "tenure_months": 60,
            "existing_liabilities": 10000,
            "location": "New York",
            "expected_decision": DecisionEnum.APPROVED
        },
        {
            "name": "Risky Applicant (Should Reject)",
            "applicant_id": "APP002",
            "age": 25,
            "income": 30000,
            "employment_type": EmploymentType.FREELANCE,
            "credit_score": 480,
            "loan_amount": 150000,
            "tenure_months": 36,
            "existing_liabilities": 50000,
            "location": "Chicago",
            "expected_decision": DecisionEnum.REJECTED
        },
        {
            "name": "Borderline Applicant (Should Review)",
            "applicant_id": "APP003",
            "age": 45,
            "income": 60000,
            "employment_type": EmploymentType.SALARIED,
            "credit_score": 680,
            "loan_amount": 100000,
            "tenure_months": 72,
            "existing_liabilities": 15000,
            "location": "Los Angeles",
            "expected_decision": DecisionEnum.MANUAL_REVIEW
        }
    ]

    results = []

    for test_case in test_cases:
        print(f"\n📝 Test: {test_case['name']}")
        print("-" * 50)

        expected = test_case.pop("expected_decision")
        expected_name = test_case.pop("name")

        application = LoanApplication(**test_case)
        result = orchestrator.evaluate_loan(application)

        if result.error:
            print(f"❌ ERROR: {result.error}")
            results.append(("FAILED", expected_name, str(result.error)))
            continue

        decision = result.decision.classification
        dti = result.financial_risk.debt_to_income_ratio
        credit_risk = result.financial_risk.credit_score_risk_level

        print(f"✅ Evaluation Complete")
        print(f"   Decision: {decision.value}")
        print(f"   Expected: {expected.value}")
        print(f"   Risk Score: {result.decision.risk_score:.2f}")
        print(f"   Confidence: {result.decision.confidence_level:.1%}")
        print(f"   DTI Ratio: {dti:.2f}")
        print(f"   Credit Risk: {credit_risk}")
        print(f"   Case ID: {result.compliance.case_id}")

        match = decision == expected
        status = "✅ PASS" if match else "❌ FAIL"
        print(f"\n{status}: Decision matches expectation")

        results.append((
            "PASSED" if match else "FAILED",
            expected_name,
            f"Expected {expected.value}, got {decision.value}"
        ))

    print_section("Test Results Summary")
    passed = sum(1 for r in results if r[0] == "PASSED")
    total = len(results)

    for status, name, details in results:
        symbol = "✅" if status == "PASSED" else "❌"
        print(f"{symbol} {name}: {status}")
        print(f"   {details}")

    print(f"\n📊 Total: {passed}/{total} tests passed")
    return passed == total


def test_edge_cases():
    """Test edge cases and boundary conditions."""
    print_section("TEST 2: Edge Cases & Boundary Conditions")

    orchestrator = LoanEvaluationOrchestrator()

    edge_cases = [
        {
            "name": "Very High DTI (80%)",
            "applicant_id": "EDGE001",
            "age": 30,
            "income": 30000,
            "employment_type": EmploymentType.SALARIED,
            "credit_score": 600,
            "loan_amount": 200000,
            "tenure_months": 36,
            "existing_liabilities": 100000,
            "location": "Miami"
        },
        {
            "name": "Minimum Age & Income",
            "applicant_id": "EDGE002",
            "age": 21,
            "income": 20000,
            "employment_type": EmploymentType.SELF_EMPLOYED,
            "credit_score": 550,
            "loan_amount": 50000,
            "tenure_months": 120,
            "existing_liabilities": 5000,
            "location": "Denver"
        },
        {
            "name": "Perfect Profile",
            "applicant_id": "EDGE003",
            "age": 40,
            "income": 150000,
            "employment_type": EmploymentType.SALARIED,
            "credit_score": 850,
            "loan_amount": 200000,
            "tenure_months": 120,
            "existing_liabilities": 0,
            "location": "San Francisco"
        }
    ]

    for test_case in edge_cases:
        print(f"\n🔍 Edge Case: {test_case['name']}")
        print("-" * 50)

        test_case.pop("name")
        application = LoanApplication(**test_case)
        result = orchestrator.evaluate_loan(application)

        if result.error:
            print(f"❌ Error: {result.error}")
            continue

        print(f"✅ Decision: {result.decision.classification.value}")
        print(f"   Risk Score: {result.decision.risk_score:.2f}")
        print(f"   Factors: {', '.join(result.decision.key_decision_factors[:2])}")


def test_compliance_tracking():
    """Test compliance record generation."""
    print_section("TEST 3: Compliance Tracking")

    orchestrator = LoanEvaluationOrchestrator()

    application = LoanApplication(
        applicant_id="COMPLIANCE001",
        age=35,
        income=70000,
        employment_type=EmploymentType.SALARIED,
        credit_score=700,
        loan_amount=100000,
        tenure_months=60,
        existing_liabilities=10000,
        location="Boston"
    )

    result = orchestrator.evaluate_loan(application)

    if result.compliance:
        print("✅ Compliance Record Generated")
        print(f"   Case ID: {result.compliance.case_id}")
        print(f"   Action: {result.compliance.action_taken}")
        print(f"   Notification Sent: {result.compliance.notification_sent}")
        print(f"   Summary: {result.compliance.summary}")
        print(f"   Timestamp: {result.compliance.timestamp}")
    else:
        print("❌ No compliance record generated")


def test_data_models():
    """Test data model validation."""
    print_section("TEST 4: Data Model Validation")

    valid_app = LoanApplication(
        applicant_id="MODEL001",
        age=30,
        income=50000,
        employment_type=EmploymentType.SALARIED,
        credit_score=700,
        loan_amount=100000,
        tenure_months=60,
        existing_liabilities=5000,
        location="Seattle"
    )

    print("✅ Valid Application Created")
    print(f"   ID: {valid_app.applicant_id}")
    print(f"   Income: ${valid_app.income:,.0f}")
    print(f"   Loan: ${valid_app.loan_amount:,.0f}")

    try:
        invalid_app = LoanApplication(
            applicant_id="INVALID",
            age=15,
            income=-1000,
            employment_type="INVALID_TYPE",
            credit_score=900,
            loan_amount=100000,
            tenure_months=60,
            existing_liabilities=5000,
            location="Test"
        )
        print("❌ Invalid application should have failed validation")
    except Exception as e:
        print(f"✅ Invalid application correctly rejected: {type(e).__name__}")


def test_decision_consistency():
    """Test decision consistency across multiple runs."""
    print_section("TEST 5: Decision Consistency")

    orchestrator = LoanEvaluationOrchestrator()

    application = LoanApplication(
        applicant_id="CONSISTENCY001",
        age=35,
        income=60000,
        employment_type=EmploymentType.SALARIED,
        credit_score=700,
        loan_amount=100000,
        tenure_months=60,
        existing_liabilities=15000,
        location="Atlanta"
    )

    decisions = []
    for i in range(3):
        result = orchestrator.evaluate_loan(application)
        decisions.append(result.decision.classification)

    all_same = all(d == decisions[0] for d in decisions)
    print(f"✅ Multiple runs produce consistent decision: {all_same}")
    print(f"   Run 1: {decisions[0].value}")
    print(f"   Run 2: {decisions[1].value}")
    print(f"   Run 3: {decisions[2].value}")


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("  LOAN APPLICATION EVALUATION SYSTEM - TEST SUITE")
    print("="*60)

    test_results = []

    try:
        test_results.append(("Agent Workflow", test_agent_workflow()))
    except Exception as e:
        print(f"❌ Test failed: {e}")
        test_results.append(("Agent Workflow", False))

    try:
        test_edge_cases()
        test_results.append(("Edge Cases", True))
    except Exception as e:
        print(f"❌ Test failed: {e}")
        test_results.append(("Edge Cases", False))

    try:
        test_compliance_tracking()
        test_results.append(("Compliance Tracking", True))
    except Exception as e:
        print(f"❌ Test failed: {e}")
        test_results.append(("Compliance Tracking", False))

    try:
        test_data_models()
        test_results.append(("Data Models", True))
    except Exception as e:
        print(f"❌ Test failed: {e}")
        test_results.append(("Data Models", False))

    try:
        test_decision_consistency()
        test_results.append(("Decision Consistency", True))
    except Exception as e:
        print(f"❌ Test failed: {e}")
        test_results.append(("Decision Consistency", False))

    print_section("Final Test Summary")
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)

    for test_name, result in test_results:
        symbol = "✅" if result else "❌"
        print(f"{symbol} {test_name}")

    print(f"\n📊 Total Tests Passed: {passed}/{total}")
    print("="*60 + "\n")

    return passed == total


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
