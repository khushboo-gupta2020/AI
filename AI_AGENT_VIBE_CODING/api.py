from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from tools.jira_fetcher import fetch_issues
from tools.llm_generator import generate_test_plan
from tools.docx_generator import populate_docx
import os
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TMP_DIR = os.path.join(os.path.dirname(__file__), ".tmp")

@app.get("/api/status")
def get_status():
    return {"status": "online"}

@app.post("/api/fetch-issues")
def api_fetch_issues(payload: dict):
    # E.g. {"jql": "order by updated DESC"}
    jql = payload.get("jql", "order by updated DESC")
    issue_data = fetch_issues(jql)
    if not issue_data:
        raise HTTPException(status_code=400, detail="Failed to fetch issues or no issues found.")
    return {"message": "Success", "data": issue_data}

@app.post("/api/generate-plan")
def api_generate_plan():
    # Trigger LLM script
    generate_test_plan()
    json_path = os.path.join(TMP_DIR, "generated_plan.json")
    if not os.path.exists(json_path):
        raise HTTPException(status_code=500, detail="LLM generation failed, no output found.")
    return {"message": "Plan generated successfully"}

@app.post("/api/synthesize-docx")
def api_synthesize_docx():
    populate_docx()
    out_path = os.path.join(TMP_DIR, "Generated_Test_Plan_Final.docx")
    if not os.path.exists(out_path):
        raise HTTPException(status_code=500, detail="Docx synthesis failed.")
    return {"message": "Document synthesized successfully", "file_path": out_path}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
