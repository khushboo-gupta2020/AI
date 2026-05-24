# Project Constitution (gemini.md)

## 1. Project Goal
Create a deterministic, self-healing automation Test Planner Agent that fetches details from Jira using project keys/sprint info and generates a structured test plan based on a `.docx` template, using configurable LLM connections (Ollama, Groq).

## 2. Data Schemas (Input/Output shapes)

### UI State & Connections Schema
```json
{
  "setup": {
    "jiraConnection": {
      "name": "string",
      "url": "string",
      "email": "string",
      "apiToken": "string",
      "status": "pending | connected | failed"
    },
    "llmConnection": {
      "provider": "ollama | groq",
      "apiKey": "string",
      "modelUrl": "string",
      "modelName": "string",
      "status": "pending | connected | failed"
    }
  },
  "fetchCriteria": {
    "productName": "string",
    "projectKey": "string",
    "sprintVersion": "string",
    "additionalContext": "string"
  },
  "review": {
    "refinedContext": "string",
    "fetchedIssues": [
      {
        "id": "JIRA-123",
        "summary": "string",
        "description": "string"
      }
    ]
  }
}
```

### Final Payload Shape (Test Plan Output)
```json
{
  "status": "success | error",
  "testPlanId": "string",
  "generatedContent": {
    "scope": "string",
    "testItems": ["string"],
    "featuresToTest": ["string"],
    "featuresNotToTest": ["string"],
    "testStrategy": "string",
    "entryCriteria": ["string"],
    "exitCriteria": ["string"],
    "testEnvironment": "object",
    "deliverables": ["string"],
    "roles": ["string"]
  },
  "downloadUrl": "string (URL to generated .docx)"
}
```

## 3. Behavioral Rules
- Prioritize reliability over speed.
- Never guess at business logic.
- Follow B.L.A.S.T. and A.N.T architectures strictly.
- Always provide a "Test Connection" button for new configurations.
- Require successful connection handshakes before proceeding to subsequent steps.

## 4. Architectural Invariants
- 4-Step UI Flow: Setup -> Fetch Issues -> Review -> Test Plan.
- Use `.tmp` for intermediate test plan generation files.
- Separation of Concerns: LLM routing (Navigation/Logic) is strictly deterministic. Generation is probabilistic, but its output mapping to the Test Plan Template is constrained.
