# System Architecture Diagram

## High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         PRESENTATION LAYER                          │
│                      (Streamlit Web UI)                             │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  • Loan Application Form                                     │   │
│  │  • Real-time Decision Display                               │   │
│  │  • Risk Assessment Visualization                            │   │
│  │  • JSON Export Functionality                                │   │
│  │  • Interactive Metrics Dashboard                            │   │
│  └──────────────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────────────┘
                         │ HTTP Request
                         │ (port 8501)
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       MICROSERVICE LAYER                            │
│                      (FastAPI REST API)                             │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  • POST /evaluate-loan          (Main endpoint)              │   │
│  │  • GET /health                  (Health check)               │   │
│  │  • GET /docs                    (Swagger UI)                 │   │
│  │  • GET /redoc                   (ReDoc)                      │   │
│  │  • Request Validation (Pydantic)                            │   │
│  │  • Error Handling & Response Formatting                     │   │
│  └──────────────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────────────┘
                         │ Application Data
                         │ (JSON)
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION LAYER                              │
│                   (LangGraph State Machine)                          │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Workflow Stages:                                            │   │
│  │  [1] Evaluate Applicant Profile                             │   │
│  │       ↓                                                       │   │
│  │  [2] Analyze Financial Risk                                 │   │
│  │       ↓                                                       │   │
│  │  [3] Make Decision                                          │   │
│  │       ↓                                                       │   │
│  │  [4] Handle Compliance & Notifications                      │   │
│  │                                                              │   │
│  │  State Management & Error Recovery                          │   │
│  └──────────────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
    Agent 1          Agent 2        Agent 3 ... Agent 4
         
┌─────────────────────────────────────────────────────────────────────┐
│                        AGENT LAYER                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────────┐  ┌──────────────────────┐               │
│  │  Applicant Profile   │  │  Financial Risk      │               │
│  │  Agent               │  │  Agent               │               │
│  │                      │  │                      │               │
│  │ • Income Stability   │  │ • DTI Ratio Calc     │               │
│  │ • Employment Risk    │  │ • Credit Risk Assess │               │
│  │ • Credit History     │  │ • Loan Amount Risk   │               │
│  │ • Completeness Check │  │ • Anomaly Detection  │               │
│  │ • Verification       │  │ • Risk Scoring       │               │
│  └──────────────────────┘  └──────────────────────┘               │
│                                                                     │
│  ┌──────────────────────┐  ┌──────────────────────┐               │
│  │  Loan Decision       │  │  Compliance &        │               │
│  │  Agent               │  │  Action Orchestrator │               │
│  │                      │  │                      │               │
│  │ • Decision Synthesis │  │ • Case ID Generation │               │
│  │ • Risk Calculation   │  │ • Audit Trail        │               │
│  │ • Confidence Level   │  │ • Notifications      │               │
│  │ • Reasoning Logic    │  │ • Record Keeping     │               │
│  │ • Classification     │  │ • Compliance Logging │               │
│  └──────────────────────┘  └──────────────────────┘               │
│                                                                     │
└────────────────────────┬────────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
    MCP Server 1   MCP Server 2   MCP Server 3 ... MCP Server 4

┌─────────────────────────────────────────────────────────────────────┐
│                    DATA ACCESS LAYER (MCP Servers)                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────────┐  ┌──────────────────────┐               │
│  │  ApplicantDB         │  │  RiskRulesDB         │               │
│  │  (Data Access)       │  │  (Rules Engine)      │               │
│  │                      │  │                      │               │
│  │ • Applicant Profile  │  │ • DTI Thresholds     │               │
│  │ • Employment History │  │ • Credit Thresholds  │               │
│  │ • Credit Records     │  │ • Risk Calculations  │               │
│  │ • Account Age        │  │ • Anomaly Rules      │               │
│  │ • Previous Defaults  │  │ • Risk Matrices      │               │
│  └──────────────────────┘  └──────────────────────┘               │
│                                                                     │
│  ┌──────────────────────┐  ┌──────────────────────┐               │
│  │  DecisionSynthesis   │  │  NotificationSystem  │               │
│  │  (Decision Engine)   │  │  (Compliance)        │               │
│  │                      │  │                      │               │
│  │ • Decision Rules     │  │ • Case ID Generator  │               │
│  │ • Classification     │  │ • Audit Logging      │               │
│  │ • Risk Scoring       │  │ • Notifications      │               │
│  │ • Confidence Calc    │  │ • Compliance Record  │               │
│  │ • Factor Weighting   │  │ • Trail Maintenance  │               │
│  └──────────────────────┘  └──────────────────────┘               │
│                                                                     │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │   External Systems (Future)    │
        │  • PostgreSQL Database         │
        │  • Email Service               │
        │  • Logging Service             │
        │  • Monitoring Service          │
        └────────────────────────────────┘
```

## Request Flow Diagram

```
┌──────────┐
│  User    │
│(Streamlit)
└────┬─────┘
     │ 1. Submit Application
     │    {applicant_id, age, income, ...}
     ▼
┌─────────────────────┐
│  FastAPI Endpoint   │
│ POST /evaluate-loan │ 2. Validate & Parse
└────┬────────────────┘
     │
     │ 3. Pass to Orchestrator
     ▼
┌─────────────────────────────────────┐
│  LangGraph Orchestrator             │
│  (State Management)                 │
└────┬────────────────────────────────┘
     │
     ├─ 4a. Node: evaluate_applicant
     │      ├─ Call ApplicantProfileAgent
     │      ├─ Query ApplicantDB
     │      └─ Return: ApplicantProfileResult
     │         {income_stability_score: 0.85,
     │          employment_risk: "LOW",
     │          credit_history_summary: "...",
     │          flags: [...]}
     │
     ├─ 4b. Node: analyze_risk
     │      ├─ Call FinancialRiskAgent
     │      ├─ Query RiskRulesDB
     │      └─ Return: FinancialRiskResult
     │         {debt_to_income_ratio: 0.30,
     │          credit_score_risk_level: "LOW",
     │          loan_amount_risk: "LOW",
     │          anomaly_detected: false}
     │
     ├─ 4c. Node: make_decision
     │      ├─ Call LoanDecisionAgent
     │      ├─ Query DecisionSynthesis
     │      └─ Return: LoanDecisionResult
     │         {classification: "APPROVED",
     │          risk_score: 0.25,
     │          confidence_level: 0.90,
     │          explanation: "..."}
     │
     └─ 4d. Node: handle_compliance
            ├─ Call ComplianceAgent
            ├─ Query NotificationSystem
            └─ Return: ComplianceResult
               {action_taken: "Loan application APPROVED",
                case_id: "CASE-ABC123XY",
                notification_sent: true}
     │
     ▼
┌─────────────────────────────────┐
│  Response Object                │
│  (LoanEvaluationState)          │
│  with all results               │
└────┬────────────────────────────┘
     │
     │ 5. Format Response
     ▼
┌─────────────────────────────────┐
│  JSON Response                  │
│  {status, decision, risk_score, │
│   confidence, case_id, ...}     │
└────┬────────────────────────────┘
     │
     │ 6. Send to User
     ▼
┌──────────────────────┐
│  Streamlit UI        │
│  Display Results     │
└──────────────────────┘
```

## Data Model Relationships

```
LoanApplication (INPUT)
├── applicant_id: str
├── age: int
├── income: float
├── employment_type: enum
├── credit_score: int
├── loan_amount: float
├── tenure_months: int
├── existing_liabilities: float
├── location: str
└── application_timestamp: datetime

                    ↓ (Processed by Agents)

LoanEvaluationState (COMPLETE STATE)
├── application: LoanApplication
├── applicant_profile: ApplicantProfileResult
│   ├── income_stability_score: float
│   ├── employment_risk: str
│   ├── credit_history_summary: str
│   └── application_completeness_flags: list[str]
├── financial_risk: FinancialRiskResult
│   ├── debt_to_income_ratio: float
│   ├── credit_score_risk_level: str
│   ├── loan_amount_risk: str
│   ├── anomaly_detected: bool
│   └── reasoning: str
├── decision: LoanDecisionResult
│   ├── classification: enum (APPROVED|REJECTED|MANUAL_REVIEW)
│   ├── risk_score: float (0-1)
│   ├── confidence_level: float (0-1)
│   ├── key_decision_factors: list[str]
│   └── explanation: str
├── compliance: ComplianceResult
│   ├── action_taken: str
│   ├── notification_sent: bool
│   ├── case_id: str (unique identifier)
│   ├── timestamp: datetime
│   └── summary: str
└── error: str (if any)

                    ↓ (Returned to User)

EvaluationResponse (OUTPUT)
├── status: str
├── applicant_id: str
├── decision: str
├── risk_score: float
├── confidence_level: float
├── case_id: str
├── explanation: str
└── error: str (optional)
```

## Decision Engine Logic Flow

```
Input: LoanApplication + ApplicantProfileResult + FinancialRiskResult

                         ↓

        ┌─ Check DTI Ratio ──────────┐
        │                            │
        ▼                            ▼
    ≤ 0.40?                      ≥ 0.70?
        │                            │
        YES                          YES
        │                            │
        ▼                            ▼
    Check Credit Score          → REJECTED
        │                        (High Risk)
        ▼
    ≥ 700?
        │
        YES                         NO
        │                           │
        ▼                           ▼
    Check Employment         Borderline
        │                    Metrics
        ▼
    Risk = LOW
        │
        ▼
    → APPROVED (90% confidence)
    
    
Anomalies & Flags Detected?
        │
        YES
        ▼
    • Increase risk_score by 0.2
    • Reduce confidence by 15%
    • Add to decision_factors
    • May override to MANUAL_REVIEW


Final Output:
┌─ Decision: APPROVED|REJECTED|MANUAL_REVIEW
├─ Risk Score: 0.0 - 1.0
├─ Confidence Level: 30% - 95%
├─ Decision Factors: [list of reasons]
└─ Explanation: Detailed reasoning
```

## Component Interactions

```
User Request
    ↓
FastAPI (Request Validation)
    ↓
LangGraph Orchestrator
    ↓
┌───────────────────────────────────────────┐
│ Step 1: Applicant Evaluation              │
├─────────────────────────────────────────────
│ ApplicantProfileAgent                     │
│    ├─→ ApplicantDB Server                 │
│    └─→ Returns: ApplicantProfileResult    │
└───────────────────────────────────────────┘
    ↓
┌───────────────────────────────────────────┐
│ Step 2: Risk Analysis                     │
├─────────────────────────────────────────────
│ FinancialRiskAgent                        │
│    ├─→ RiskRulesDB Server                 │
│    └─→ Returns: FinancialRiskResult       │
└───────────────────────────────────────────┘
    ↓
┌───────────────────────────────────────────┐
│ Step 3: Decision Making                   │
├─────────────────────────────────────────────
│ LoanDecisionAgent                         │
│    ├─→ DecisionSynthesis Server           │
│    └─→ Returns: LoanDecisionResult        │
└───────────────────────────────────────────┘
    ↓
┌───────────────────────────────────────────┐
│ Step 4: Compliance & Notification         │
├─────────────────────────────────────────────
│ ComplianceOrchestratorAgent                │
│    ├─→ NotificationSystem Server          │
│    ├─→ Generates Case ID                  │
│    ├─→ Creates Audit Trail               │
│    └─→ Returns: ComplianceResult         │
└───────────────────────────────────────────┘
    ↓
FastAPI (Format Response)
    ↓
Streamlit UI (Display Results)
    ↓
User (Decision + Case Record)
```

## Deployment Architecture

```
┌──────────────────────────────────────────────────┐
│         LOAD BALANCER / INGRESS                  │
└─────────────────┬────────────────────────────────┘
                  │
        ┌─────────┼─────────┐
        │         │         │
        ▼         ▼         ▼
    ┌─────────┬─────────┬─────────┐
    │ API Pod │ API Pod │ API Pod │ (Kubernetes)
    │ :8000   │ :8000   │ :8000   │
    └────┬────┴────┬────┴────┬────┘
         │         │         │
         └─────────┼─────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  PostgreSQL Database │
        │  (Compliance Logs)   │
        └──────────────────────┘
        
        ┌──────────────────────┐
        │  Redis Cache         │
        │  (Session Storage)   │
        └──────────────────────┘
        
        ┌──────────────────────┐
        │  Monitoring Stack    │
        │  (Prometheus/Grafana)│
        └──────────────────────┘
```

## Technology Stack Diagram

```
┌─────────────────────────────────────────────────────┐
│                   LAYER STACK                       │
├─────────────────────────────────────────────────────┤
│ Frontend        │ Streamlit (Web UI)                │
├─────────────────┼──────────────────────────────────┤
│ API             │ FastAPI + Uvicorn                │
├─────────────────┼──────────────────────────────────┤
│ Orchestration   │ LangGraph + LangChain             │
├─────────────────┼──────────────────────────────────┤
│ Agents          │ Python Classes (Domain Logic)    │
├─────────────────┼──────────────────────────────────┤
│ MCP/Services    │ MCP Servers (Data Access)        │
├─────────────────┼──────────────────────────────────┤
│ Models          │ Pydantic (Data Validation)       │
├─────────────────┼──────────────────────────────────┤
│ LLM             │ Anthropic Claude API             │
├─────────────────┼──────────────────────────────────┤
│ Database        │ PostgreSQL (Future)              │
└─────────────────┴──────────────────────────────────┘
```

---

**Key Takeaway**: This is a well-designed, layered architecture that separates concerns, scales horizontally, and maintains flexibility for future enhancements while keeping the codebase maintainable and testable.
