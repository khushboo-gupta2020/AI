from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from app.jira_service import JiraService
from app.test_case_generator import TestCaseGenerator

app = FastAPI(title="Jira Test Case Generator", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class JiraConfig(BaseModel):
    base_url: str
    email: str
    api_token: str


class TestConnectionRequest(BaseModel):
    config: JiraConfig


class GenerateRequest(BaseModel):
    config: JiraConfig
    issue_id: str


class TestCaseResponse(BaseModel):
    success: bool
    message: str
    story_data: Optional[dict] = None
    test_cases: Optional[list] = None


@app.get("/")
async def root():
    return {"message": "Jira Test Case Generator API", "version": "1.0.0"}


@app.post("/api/test-connection")
async def test_connection(request: TestConnectionRequest):
    service = JiraService(
        base_url=request.config.base_url,
        email=request.config.email,
        api_token=request.config.api_token
    )
    result = service.connect()
    if result["success"]:
        return {"success": True, "message": result["message"]}
    raise HTTPException(status_code=400, detail=result["message"])


@app.post("/api/generate", response_model=TestCaseResponse)
async def generate_test_cases(request: GenerateRequest):
    try:
        service = JiraService(
            base_url=request.config.base_url,
            email=request.config.email,
            api_token=request.config.api_token
        )

        story_data = service.get_issue(request.issue_id)
        if not story_data:
            raise HTTPException(status_code=404, detail="Failed to fetch Jira issue")

        generator = TestCaseGenerator()
        test_cases = generator.generate(story_data)

        return TestCaseResponse(
            success=True,
            message=f"Generated {len(test_cases)} test cases",
            story_data=story_data,
            test_cases=test_cases
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
