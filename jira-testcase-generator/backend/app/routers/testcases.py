from fastapi import APIRouter, HTTPException
from app.models.schemas import JiraStoryRequest, TestCaseResponse, JiraStory, TestCase
from app.services.jira_service import JiraService
from app.services.testcase_generator import TestCaseGenerator

router = APIRouter(prefix="/api/testcases", tags=["testcases"])


@router.post("/generate")
async def generate_testcases(request: JiraStoryRequest):
    service = JiraService(request.jira_base_url, request.jira_email, request.jira_api_token)
    try:
        story = await service.fetch_story(request.story_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    generator = TestCaseGenerator(story)
    test_cases = generator.generate()

    return {
        "story": story.dict(),
        "test_cases": [tc.dict() for tc in test_cases],
    }
