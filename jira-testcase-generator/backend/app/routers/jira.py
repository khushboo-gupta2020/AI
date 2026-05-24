from fastapi import APIRouter, HTTPException
from app.models.schemas import JiraConnectionConfig, JiraStoryRequest
from app.services.jira_service import JiraService

router = APIRouter(prefix="/api/jira", tags=["jira"])


@router.post("/test-connection")
async def test_connection(config: JiraConnectionConfig):
    service = JiraService(config.jira_base_url, config.jira_email, config.jira_api_token)
    result = await service.test_connection()
    if result["success"]:
        return result
    raise HTTPException(status_code=400, detail=result.get("error", "Connection failed"))


@router.post("/fetch-story")
async def fetch_story(request: JiraStoryRequest):
    service = JiraService(request.jira_base_url, request.jira_email, request.jira_api_token)
    try:
        story = await service.fetch_story(request.story_id)
        return story.dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
