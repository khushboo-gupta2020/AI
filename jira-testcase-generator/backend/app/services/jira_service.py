import base64
import httpx
from app.models.schemas import JiraStory


class JiraService:
    def __init__(self, base_url: str, email: str, api_token: str):
        self.base_url = base_url.rstrip("/")
        self.auth_header = self._build_auth_header(email, api_token)

    @staticmethod
    def _build_auth_header(email: str, api_token: str) -> str:
        credentials = f"{email}:{api_token}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded}"

    async def test_connection(self) -> dict:
        url = f"{self.base_url}/rest/api/3/myself"
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(url, headers={"Authorization": self.auth_header})
            if response.status_code == 200:
                data = response.json()
                return {"success": True, "user": data.get("displayName", ""), "email": data.get("emailAddress", "")}
            elif response.status_code == 401:
                return {"success": False, "error": "Authentication failed. Check your email and API token."}
            elif response.status_code == 404:
                return {"success": False, "error": "Jira URL not found. Verify the base URL."}
            else:
                return {"success": False, "error": f"Connection failed with status {response.status_code}: {response.text}"}

    async def fetch_story(self, story_id: str) -> JiraStory:
        url = f"{self.base_url}/rest/api/3/issue/{story_id}"
        params = {"fields": "summary,description,issuetype,priority,labels,status,comment"}
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(url, headers={"Authorization": self.auth_header}, params=params)
            if response.status_code == 401:
                raise Exception("Authentication failed. Check your Jira credentials.")
            elif response.status_code == 404:
                raise Exception(f"Jira issue '{story_id}' not found.")
            elif response.status_code != 200:
                raise Exception(f"Failed to fetch Jira issue: {response.status_code} - {response.text}")

            data = response.json()
            fields = data.get("fields", {})

            description_raw = fields.get("description", {})
            description = self._parse_description(description_raw)

            acceptance_criteria = self._extract_acceptance_criteria(description, fields)

            priority = fields.get("priority", {})
            priority_name = priority.get("name") if priority else None

            labels = fields.get("labels", [])
            issue_type = fields.get("issuetype", {}).get("name", "")
            status = fields.get("status", {}).get("name", "")

            return JiraStory(
                key=data.get("key", story_id),
                summary=fields.get("summary", ""),
                description=description,
                acceptance_criteria=acceptance_criteria,
                priority=priority_name,
                labels=labels,
                issue_type=issue_type,
                status=status,
            )

    @staticmethod
    def _parse_description(description_raw) -> str:
        if isinstance(description_raw, str):
            return description_raw
        if isinstance(description_raw, dict):
            content = description_raw.get("content", [])
            return JiraService._parse_adf_content(content)
        return ""

    @staticmethod
    def _parse_adf_content(content: list) -> str:
        text_parts = []
        for node in content:
            node_type = node.get("type", "")
            if node_type == "paragraph":
                para_text = JiraService._extract_text_from_nodes(node.get("content", []))
                text_parts.append(para_text)
            elif node_type == "heading":
                heading_text = JiraService._extract_text_from_nodes(node.get("content", []))
                text_parts.append(f"\n## {heading_text}\n")
            elif node_type == "bulletList" or node_type == "orderedList":
                for item in node.get("content", []):
                    item_text = JiraService._extract_text_from_nodes(item.get("content", []))
                    text_parts.append(f"- {item_text}")
            elif node_type == "blockquote":
                bq_text = JiraService._extract_text_from_nodes(node.get("content", []))
                text_parts.append(f"> {bq_text}")
            else:
                fallback = JiraService._extract_text_from_nodes(node.get("content", []))
                if fallback:
                    text_parts.append(fallback)
        return "\n".join(text_parts)

    @staticmethod
    def _extract_text_from_nodes(nodes: list) -> str:
        parts = []
        for node in nodes:
            if node.get("type") == "text":
                parts.append(node.get("text", ""))
            elif node.get("type") == "hardBreak":
                parts.append("\n")
            elif node.get("content"):
                parts.append(JiraService._extract_text_from_nodes(node.get("content", [])))
        return "".join(parts)

    @staticmethod
    def _extract_acceptance_criteria(description: str, fields: dict) -> str:
        ac_text = ""
        for keyword in ["Acceptance Criteria", "Acceptance criteria", "AC:", "AC -", "Given/When/Then"]:
            idx = description.find(keyword)
            if idx != -1:
                ac_text = description[idx:].strip()
                break

        if not ac_text:
            comments = fields.get("comment", {}).get("comments", [])
            for comment in comments:
                body = comment.get("body", "")
                body_text = JiraService._parse_description(body) if isinstance(body, dict) else body
                for kw in ["Acceptance Criteria", "Acceptance criteria", "AC:"]:
                    if kw in body_text:
                        ac_text = body_text
                        break
                if ac_text:
                    break

        return ac_text
