# Jira Test Case Generator

A full-stack application that automatically generates QA test cases from Jira User Stories.

## Tech Stack

- **Frontend:** React.js with Tailwind CSS
- **Backend:** Python FastAPI
- **Integration:** Jira REST API

## Features

- Configure and test Jira connection
- Fetch Jira story details by ID
- Auto-generate 5+ QA test cases (positive, negative, boundary)
- Export to Markdown, CSV, or copy to clipboard
- Modern responsive dashboard UI
- Local storage for connection settings

## Project Structure

```
TestCase_Generator/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Settings management
│   │   ├── jira_service.py      # Jira API integration
│   │   └── test_case_generator.py  # Test case generation engine
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── public/
    ├── src/
    │   ├── components/
    │   │   ├── App.js
    │   │   ├── JiraSettings.js
    │   │   ├── TestCaseForm.js
    │   │   ├── TestCaseTable.js
    │   │   └── Notification.js
    │   ├── services/
    │   │   └── api.js
    │   ├── index.js
    │   └── index.css
    ├── package.json
    ├── tailwind.config.js
    └── postcss.config.js
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd TestCase_Generator/backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   source venv/bin/activate  # Mac/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file from example:
   ```bash
   copy .env.example .env   # Windows
   cp .env.example .env     # Mac/Linux
   ```

5. Edit `.env` with your Jira credentials (optional, can also configure via UI):
   ```
   JIRA_BASE_URL=https://your-domain.atlassian.net
   JIRA_EMAIL=your-email@example.com
   JIRA_API_TOKEN=your-api-token
   ```

6. Start the backend server:
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   Backend will be available at: `http://localhost:8000`
   API docs at: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd TestCase_Generator/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. (Optional) Set API URL in `.env`:
   ```
   REACT_APP_API_URL=http://localhost:8000
   ```

4. Start the development server:
   ```bash
   npm start
   ```

   Frontend will be available at: `http://localhost:3000`

## Usage

1. Open the application in your browser (`http://localhost:3000`)
2. In the left sidebar, enter your Jira connection settings:
   - Jira Base URL (e.g., `https://your-domain.atlassian.net`)
   - Email address
   - API Token (generate at https://id.atlassian.com/manage-profile/security/api-tokens)
3. Click **Test Connection** to validate
4. Click **Save Config** to persist settings locally
5. In the main panel, enter a Jira Story ID (e.g., `PROJ-123`)
6. Click **Generate Test Cases**
7. View generated test cases in the table
8. Use export buttons to:
   - **Copy** - Copy formatted test cases to clipboard
   - **Markdown** - Download as `.md` file
   - **CSV** - Download as `.csv` file (Excel compatible)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API health check |
| POST | `/api/test-connection` | Test Jira connection |
| POST | `/api/generate` | Generate test cases from Jira story |

### Request Body for `/api/generate`

```json
{
  "config": {
    "base_url": "https://your-domain.atlassian.net",
    "email": "your-email@example.com",
    "api_token": "your-api-token"
  },
  "issue_id": "PROJ-123"
}
```

## Generating Jira API Token

1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click **Create API token**
3. Give it a label (e.g., "Test Case Generator")
4. Copy the token (you won't see it again)
5. Use this token in the application settings

## Troubleshooting

- **Connection failed:** Verify your Jira URL, email, and API token
- **Issue not found:** Check the issue ID format (e.g., `PROJ-123`)
- **CORS errors:** Ensure backend is running and CORS is configured
- **Port conflicts:** Change ports in backend (`--port`) or frontend (`PORT=3001 npm start`)
