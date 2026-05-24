# Jira Test Case Generator

A full-stack application that automatically generates QA test cases from Jira User Stories.

## Tech Stack

- **Frontend:** React.js + Vite + Tailwind CSS
- **Backend:** Python + FastAPI
- **Integration:** Jira REST API v3

## Features

- Jira connection configuration and validation
- Automatic fetching of Jira User Story details
- Generation of 10+ QA test cases per story (positive, negative, boundary, acceptance criteria)
- Export to Markdown (.md) and CSV (.csv)
- Copy to clipboard
- Modern responsive dashboard UI
- Local storage for Jira credentials

## Project Structure

```
jira-testcase-generator/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application entry
│   │   ├── config.py            # Settings & env config
│   │   ├── models/
│   │   │   └── schemas.py       # Pydantic models
│   │   ├── routers/
│   │   │   ├── jira.py          # Jira connection endpoints
│   │   │   └── testcases.py     # Test case generation endpoint
│   │   └── services/
│   │       ├── jira_service.py          # Jira API integration
│   │       └── testcase_generator.py    # Test case generation engine
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Main React component
│   │   ├── main.jsx             # React entry point
│   │   ├── index.css            # Tailwind CSS
│   │   └── services/
│   │       └── api.js           # Axios API service
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── index.html
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.10+
- Node.js 18+
- Jira account with API token

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file from example:
   ```bash
   cp .env.example .env
   ```

5. Edit `.env` with your Jira credentials:
   ```
   JIRA_BASE_URL=https://your-domain.atlassian.net
   JIRA_EMAIL=your-email@example.com
   JIRA_API_TOKEN=your-api-token
   ```

6. Start the backend server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

   The API will be available at `http://localhost:8000`
   API docs at `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:3000`

### Generating Jira API Token

1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Give it a name and copy the token
4. Use this token in the `.env` file or the UI

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/jira/test-connection` | Test Jira connection |
| POST | `/api/jira/fetch-story` | Fetch a Jira story by ID |
| POST | `/api/testcases/generate` | Generate test cases from a Jira story |
| GET | `/api/health` | Health check |

## Usage

1. Open the dashboard at `http://localhost:3000`
2. Configure Jira connection in the left sidebar
3. Click "Test Connection" to validate
4. Enter a Jira Story ID (e.g., `PROJ-123`)
5. Click "Generate Test Cases"
6. Review, copy, or export the generated test cases

## Export Formats

- **Copy to Clipboard:** Formatted text ready for pasting
- **Markdown:** Properly formatted `.md` file with tables
- **CSV:** Excel-compatible `.csv` file with UTF-8 BOM

## Docker (Optional)

### Backend Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile

```dockerfile
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## License

MIT
