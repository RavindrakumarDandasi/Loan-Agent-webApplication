# Deployment Guide

## Development Environment

### Local Setup
```bash
# Clone/navigate to project
cd /home/ubuntu/Desktop/Loan_Agent

# Create/activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python3 test_system.py

# Start services
./run_api.sh      # Terminal 1: API on :8000
./run_ui.sh       # Terminal 2: UI on :8501
```

## Production Deployment

### Docker Setup

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000 8501

CMD ["sh", "-c", "python -m uvicorn Api.main:app --host 0.0.0.0 --port 8000"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - LOG_LEVEL=INFO
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  ui:
    build: .
    ports:
      - "8501:8501"
    depends_on:
      - api
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    restart: unless-stopped
    command: ["streamlit", "run", "Ui/app.py", "--server.port=8501"]

  postgres:
    image: postgres:15
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=loan_agent
      - POSTGRES_USER=loanadmin
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

### Environment Variables (.env for production)

```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# LLM Configuration
ANTHROPIC_API_KEY=sk-ant-...
BEDROCK_REGION=us-east-1
BEDROCK_MODEL_ID=global.anthropic.claude-sonnet-4-6

# Database Configuration (Optional)
DATABASE_URL=postgresql://loanadmin:password@postgres:5432/loan_agent
DB_ECHO=false

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/loan-agent/api.log

# Security
ALLOWED_ORIGINS=https://yourdomain.com
CORS_CREDENTIALS=true

# Feature Flags
ENABLE_COMPLIANCE_LOGGING=true
ENABLE_AUDIT_TRAIL=true
ENABLE_FRAUD_DETECTION=false
```

## Database Persistence

### Setup PostgreSQL Schema

```sql
CREATE TABLE loan_applications (
    id SERIAL PRIMARY KEY,
    case_id VARCHAR(50) UNIQUE NOT NULL,
    applicant_id VARCHAR(100) NOT NULL,
    application_data JSONB NOT NULL,
    decision VARCHAR(50) NOT NULL,
    risk_score FLOAT NOT NULL,
    confidence FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE compliance_records (
    id SERIAL PRIMARY KEY,
    case_id VARCHAR(50) UNIQUE NOT NULL REFERENCES loan_applications(case_id),
    action_taken VARCHAR(200),
    notification_sent BOOLEAN,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    case_id VARCHAR(50) NOT NULL REFERENCES loan_applications(case_id),
    agent_name VARCHAR(100),
    action VARCHAR(200),
    details JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_applicant_id ON loan_applications(applicant_id);
CREATE INDEX idx_case_id ON loan_applications(case_id);
CREATE INDEX idx_decision ON loan_applications(decision);
```

## Kubernetes Deployment

### deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: loan-agent-api
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: loan-agent-api
  template:
    metadata:
      labels:
        app: loan-agent-api
    spec:
      containers:
      - name: api
        image: loan-agent:latest
        ports:
        - containerPort: 8000
        env:
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: anthropic-secrets
              key: api-key
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secrets
              key: url
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10

---
apiVersion: v1
kind: Service
metadata:
  name: loan-agent-api
spec:
  selector:
    app: loan-agent-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

## CI/CD Pipeline

### GitHub Actions (.github/workflows/deploy.yml)

```yaml
name: Deploy Loan Agent

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python3 test_system.py
      - run: python3 -m pytest tests/ --cov

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v2
      - uses: docker/setup-buildx-action@v1
      - uses: docker/login-action@v1
        with:
          registry: gcr.io
          username: _json_key
          password: ${{ secrets.GCP_SA_KEY }}
      - uses: docker/build-push-action@v2
        with:
          context: .
          push: true
          tags: gcr.io/${{ secrets.GCP_PROJECT }}/loan-agent:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/loan-agent-api \
            api=gcr.io/${{ secrets.GCP_PROJECT }}/loan-agent:latest
```

## Monitoring & Logging

### Application Metrics

```python
# In Api/main.py
from prometheus_client import Counter, Histogram, generate_latest

evaluation_counter = Counter('loan_evaluations_total', 'Total evaluations', ['decision'])
evaluation_duration = Histogram('loan_evaluation_duration_seconds', 'Evaluation duration')
risk_score_histogram = Histogram('loan_risk_score', 'Risk score distribution')

@app.post("/evaluate-loan")
async def evaluate_loan(application: LoanApplication):
    with evaluation_duration.time():
        result = orchestrator.evaluate_loan(application)
        evaluation_counter.labels(decision=result.decision.classification.value).inc()
        risk_score_histogram.observe(result.decision.risk_score)
```

### Log Aggregation

```yaml
# docker-compose with ELK stack
elasticsearch:
  image: docker.elastic.co/elasticsearch/elasticsearch:8.0.0
  environment:
    discovery.type: single-node

kibana:
  image: docker.elastic.co/kibana/kibana:8.0.0
  ports:
    - "5601:5601"
```

## Performance Optimization

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_applicant_profile_cached(applicant_id: str):
    return applicant_agent.evaluate_applicant_profile(applicant_id)
```

### Async Processing

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=10)

@app.post("/evaluate-loan-async")
async def evaluate_loan_async(application: LoanApplication):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        executor,
        orchestrator.evaluate_loan,
        application
    )
    return result
```

## Security Considerations

1. **API Authentication**
   - Use API keys for external access
   - Implement JWT tokens
   - Rate limiting per client

2. **Data Encryption**
   - Encrypt sensitive fields (credit scores, income)
   - Use TLS/SSL for all communications
   - Encrypt database at rest

3. **Audit Logging**
   - Log all decisions and reasons
   - Track user access
   - Maintain compliance records

4. **Input Validation**
   - Validate all application data
   - Sanitize inputs
   - Check data types and ranges

## Scaling Strategy

### Horizontal Scaling
- Run multiple API instances behind load balancer
- Use message queue (RabbitMQ/Redis) for async tasks
- Implement connection pooling

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Cache frequently accessed data

### Database Scaling
- Use read replicas for analytics
- Implement sharding by applicant_id
- Archive old records

## Maintenance

### Backup Strategy
```bash
# Daily backup
pg_dump loan_agent | gzip > backup_$(date +%Y%m%d).sql.gz
```

### Update Process
1. Run tests in staging
2. Blue-green deployment
3. Gradual rollout (canary)
4. Monitor error rates

## Rollback Procedure

```bash
# Revert to previous version
docker service update --image loan-agent:previous loan-agent-api
kubectl rollout undo deployment/loan-agent-api
```
