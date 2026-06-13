# Define Your QA Team
# # Our task of BugTriageCrew is to prioritize, analyze, find RCA (root cause analysis) for these applications. 
# In short -> Why bug occurs? 

# # Sample bug report
# bug_report = """
# Bug Title: Shopping cart total shows $0.00 after applying discount code
# Bug ID: BUG-4521
# Reporter: manual_tester_jane
# Environment: Production, Chrome 120, Windows 11
# Severity (Reporter): High

# Steps to Reproduce:
# 1. Add 3+ items to shopping cart (total > $50)
# 2. Apply discount code "SAVE20" (20% off)
# 3. Observe the cart total

# Actual Result: Cart total shows $0.00 instead of discounted price
# Expected Result: Cart total should show original price minus 20%

# Additional Info:
# - Happens only when cart has 3+ items
# - Works fine with 1-2 items
# - Started after last Friday's deployment (v2.4.1)
# - No errors in browser console
# - API response shows correct discounted amount
# """

from crewai import LLM, Agent, Task, Crew, Process
from dotenv import load_dotenv
import os
import requests

load_dotenv()

# Patch: Groq doesn't support cache_breakpoint. Make mark_cache_breakpoint a no-op.
import crewai.llms.cache as _cache
_cache.mark_cache_breakpoint = lambda msg: msg


#step 0: brain
groq_LLM = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_KEY")
)
#- Agent1: Bug Tries Analyst
#- Agent2: Root Cause Investigator
# Agent3: Task Recommendation Agent
#- Task1: Classify the bug
#- Task2: Investigate root cause (Uses tries output as context)
#- Task3: Recommend test (Uses both previous output)

def fetch_jira_ticket(bugid):    
    url=f"https://khushboo-gupta.atlassian.net/rest/api/3/issue/{bugid}"
    r=requests.get(url,auth=(os.getenv("JIRA_EMAIL"),os.getenv("JIRA_API_TOKEN")))
    data= r.json()
    f=data["fields"]
    desc=f["description"]["content"][0]["content"][0]["text"]
    return f"""Bug title:{f['summary']}
    Bug ID:{data['key']}
    reporter:{f['reporter']['displayName']}
    {desc}"""


print(fetch_jira_ticket("AIS-8"))
bug_report =fetch_jira_ticket("AIS-8")
print(bug_report)

buganalyst_agent = Agent(
    role="Senior Bug Triage Analyst",
    goal="Accurately classify incoming bugs by severity, category, and priority. ",
    backstory="""You are a veteran QA engineer with 15 years of experience. You follow strict severity classification.
    P0:Blocker  System Down Data Loss Security Breach
    p1 : Critical Major feature Broken No workaround
    P2 : Major Feature Impaired Workaround exists
    P3 : Minor Cosmetic IssueMinor Inconvenience 
   P4 : Trivial Enhancement RequestTypo"
Never inflate severity. You always justify your classification.""",
    llm=groq_LLM,
    verbose=True,
    ALLOW_DELEGATION=False
) 

rootcause_agent = Agent(
    role="Root cause analysis specialist",
    goal="Identify the likely root cause and affected system components ",
    backstory="""You are debugging/exporting things in system layers. 
    You analyze work by tracing through UI, API, service, database.
      You identify whether the issue is in Front-End, Back-End, Infrastructure, or Third-Party Integration. 
      You suggest which log files or monitoring dashboards to check first. """,
    llm=groq_LLM,
    verbose=True,
    ALLOW_DELEGATION=False
)
test_recommender_agent = Agent(
    role="Test Strategy Advisor ",
    goal="recommends specific tests to validate the fix and prevent regression",
    backstory="""You are an estate who designs test strategies. For every bug you recommend:
- an immediate smog test to verify the fix
- regression test cases to prevent recurrence
- edge cases should be added to the test suit
You specify tests in 3-5 minutes each time when applicable. """,
    llm=groq_LLM,
    verbose=True,
    ALLOW_DELEGATION=False
)
triage_task =Task(
    description="""Analyze and classify this bug report.
{bug_report}
  
 Provide :
1. severity :(P0-P4) justification.
2. Category: UI, functional performance, and metadata.
3. Affected component/module.
4. Business impact assessment.
5. Recommended priority for sprint planning.""",
    expected_output="""A Structured Triage Report with:
Severity, Capability,Continent,Business Impact,Sprint Priority""",
agent=buganalyst_agent
)


root_cause_task =Task(
    description="""Based on the trial analysis, investigate the likely root cause of this bug.
     {bug_report}
       Provide:
1. 1 most likely root cause
2. 2 system, near-affected UI/API service
3. 3 related component that might have impacted
4. 4 suggested investigation steps
5. 5 which logs or dashboards to check first""",
    expected_output="""Total cause analysis improved with the probable cause, affected near component, and in the station stress. """,
agent=rootcause_agent,
context=[triage_task]
)

test_task =Task(
    description="""Based on the triage and root cause analysis, recommend test cases for this bug.
    {bug_report}
    1. Verification test to confirm the fix
    2. 3 to 5 regression test cases
    3. Edge cases to add to the test suite
    4. Suggested test automation approach, playwright with Typescript
    5. Any load or performance tests if applicable""",
    expected_output="""A Test Recommendation Report with Verification Tests, Regulation Cases, Edge Cases, and Automation Approach """,
agent=test_recommender_agent,
 context=[triage_task,root_cause_task]
 )
crew = Crew(
    agents=[buganalyst_agent,rootcause_agent,test_recommender_agent],
    tasks=[triage_task,root_cause_task,test_task],
    process=Process.sequential,
    verbose=True
)

print(" QA Bug triage crew sctarted anlaysis")
print("=" *60)
result = crew.kickoff();
print("\n" + "=" *60);
print("Final triage report");
print("=" *60)
print(result)
