from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    jira_base_url: str = "https://khushboo-gupta.atlassian.net/"
    jira_email: str = ""
    jira_api_token: str = ""
    jira_project_key: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
