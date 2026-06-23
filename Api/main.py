from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.evaluator import SubmissionEvaluator

app = FastAPI(
    title="GEN-AI Case Study Evaluator",
    description="Comprehensive evaluator for Agentic AI Intelligent Loan Approval System case study submissions",
    version="2.0.0"
)

# Setup static files and templates
base_dir = Path(__file__).parent.parent
static_dir = base_dir / "static"
templates_dir = base_dir / "templates"

if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
if templates_dir.exists():
    templates = Jinja2Templates(directory=str(templates_dir))


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "GEN-AI Case Study Evaluator",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/", response_class=HTMLResponse)
async def home():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>GEN-AI Case Study Evaluator</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; }
            .info { background: #e8f4f8; padding: 15px; border-left: 4px solid #3498db; margin: 20px 0; }
            .endpoints { background: #f9f9f9; padding: 20px; border-radius: 4px; }
            .endpoint { margin: 10px 0; padding: 10px; background: white; border-left: 3px solid #27ae60; }
            code { background: #f0f0f0; padding: 2px 6px; border-radius: 3px; font-family: monospace; }
            a { color: #3498db; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎓 GEN-AI Case Study Evaluator</h1>
            <p>Comprehensive evaluation system for <strong>Agentic AI Intelligent Loan Approval System</strong> case study submissions.</p>

            <div class="info">
                <strong>Version 2.0</strong> - Optimized for case study evaluation<br>
                Evaluates submissions across 7 dimensions with detailed scoring and recommendations.
            </div>

            <h2>API Endpoints</h2>
            <div class="endpoints">
                <div class="endpoint">
                    <strong>Health Check</strong><br>
                    <code>GET /health</code>
                </div>
                <div class="endpoint">
                    <strong>Evaluate Submission</strong><br>
                    <code>POST /evaluate-submission</code><br>
                    <em>Query: ?participant_name=Name&submission_path=/path</em>
                </div>
                <div class="endpoint">
                    <strong>API Documentation</strong><br>
                    <code>GET /docs</code> (Swagger UI)<br>
                    <code>GET /redoc</code> (ReDoc)
                </div>
            </div>

            <h2>Quick Links</h2>
            <ul>
                <li><a href="/docs">📖 API Documentation (Swagger)</a></li>
                <li><a href="http://localhost:8501">🎨 Web Interface (Streamlit)</a></li>
                <li><a href="/evaluator-guide">📚 Evaluator Guide</a></li>
            </ul>
        </div>
    </body>
    </html>
    """
    return html


@app.get("/evaluator-guide")
async def evaluator_guide():
    guide_path = base_dir / "EVALUATOR_GUIDE.md"
    if guide_path.exists():
        with open(guide_path, 'r') as f:
            content = f.read()
        return HTMLResponse(f"<pre>{content}</pre>")
    return {"message": "Evaluator guide not found"}


@app.post("/evaluate-submission")
async def evaluate_submission(participant_name: str, submission_path: str):
    """
    Evaluate a GEN-AI case study submission.

    **Query Parameters:**
    - `participant_name`: Name of the participant (required)
    - `submission_path`: Path to the submission directory (required)

    **Returns:** Comprehensive evaluation report with:
    - Submission completeness check
    - 7-dimension scoring
    - Detailed recommendations
    - Overall grade and status
    """
    try:
        # Validate submission path
        submission = Path(submission_path)
        if not submission.exists():
            raise HTTPException(status_code=404, detail=f"Submission path not found: {submission_path}")
        if not submission.is_dir():
            raise HTTPException(status_code=400, detail=f"Submission path must be a directory: {submission_path}")

        # Run evaluation
        evaluator = SubmissionEvaluator()
        report = evaluator.evaluate(
            submission_path=str(submission.absolute()),
            participant_name=participant_name
        )

        return {
            "status": "success",
            "report": report.to_dict(),
            "markdown": report.to_markdown()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
