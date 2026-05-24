from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import jira, testcases

app = FastAPI(title="Jira Test Case Generator", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jira.router)
app.include_router(testcases.router)


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "Jira Test Case Generator"}
