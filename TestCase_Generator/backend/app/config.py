from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    JIRA_BASE_URL: str = ""
    JIRA_EMAIL: str = ""
    JIRA_API_TOKEN: str = ""
    JIRA_PROJECT_KEY: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
