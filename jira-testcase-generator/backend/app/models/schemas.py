from pydantic import BaseModel
from typing import Optional


class JiraConnectionConfig(BaseModel):
    jira_base_url: str
    jira_email: str
    jira_api_token: str
    jira_project_key: Optional[str] = ""


class JiraStoryRequest(BaseModel):
    story_id: str
    jira_base_url: str
    jira_email: str
    jira_api_token: str


class JiraStory(BaseModel):
    key: str
    summary: str
    description: str
    acceptance_criteria: str = ""
    priority: Optional[str] = None
    labels: list[str] = []
    issue_type: str = ""
    status: str = ""


class TestCase(BaseModel):
    test_case_id: str
    test_scenario: str
    preconditions: str
    test_steps: str
    expected_result: str
    priority: str


class TestCaseResponse(BaseModel):
    story: JiraStory
    test_cases: list[TestCase]
