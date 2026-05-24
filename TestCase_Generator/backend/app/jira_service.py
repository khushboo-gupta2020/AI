from jira import JIRA
from jira.exceptions import JIRAError
from app.config import settings


class JiraService:
    def __init__(self, base_url=None, email=None, api_token=None):
        self.base_url = base_url or settings.JIRA_BASE_URL
        self.email = email or settings.JIRA_EMAIL
        self.api_token = api_token or settings.JIRA_API_TOKEN
        self.client = None

    def connect(self):
        try:
            self.client = JIRA(
                server=self.base_url,
                basic_auth=(self.email, self.api_token)
            )
            self.client.myself()
            return {"success": True, "message": "Connection successful"}
        except JIRAError as e:
            return {"success": False, "message": f"Jira Error: {e.text or str(e)}"}
        except Exception as e:
            return {"success": False, "message": f"Connection failed: {str(e)}"}

    def get_issue(self, issue_id):
        try:
            if not self.client:
                self.connect()
                if not self.client:
                    return None
            issue = self.client.issue(issue_id)
            return {
                "id": issue.id,
                "key": issue.key,
                "summary": issue.fields.summary,
                "description": issue.fields.description or "",
                "status": str(issue.fields.status),
                "priority": str(issue.fields.priority) if issue.fields.priority else "None",
                "labels": issue.fields.labels or [],
                "issuetype": str(issue.fields.issuetype),
                "acceptance_criteria": self._extract_acceptance_criteria(issue)
            }
        except JIRAError as e:
            raise Exception(f"Jira Error: {e.text or str(e)}")
        except Exception as e:
            raise Exception(f"Failed to fetch issue: {str(e)}")

    def _extract_acceptance_criteria(self, issue):
        description = issue.fields.description or ""
        ac_keywords = ["acceptance criteria", "given", "when", "then", "scenario"]
        lines = description.split("\n")
        ac_section = []
        in_ac = False

        for line in lines:
            lower_line = line.lower().strip()
            if any(kw in lower_line for kw in ac_keywords):
                in_ac = True
            if in_ac:
                ac_section.append(line)

        return "\n".join(ac_section) if ac_section else description
