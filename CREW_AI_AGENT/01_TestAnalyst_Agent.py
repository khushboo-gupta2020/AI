#This is a senior QA with 15 years of experience.
#  Based on the feature, it will analyze the requirement
#  and suggest a 5-day test case, P0 test case. 
from crewai import LLM, Agent, Task, Crew
from dotenv import load_dotenv
import os

load_dotenv()


#step 0: brain
groq_LLM = LLM(
    model="groq/openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_KEY")
)

#step 1: define the agent identity
qa_agent = Agent(
    role="QA engineer",
    goal="Analyze the feature and requirements and create the test cases out of it",
    backstory="you are a senior QA engineer who has 15 years of experience in test analyzing, test requirement analyzing, and preparing the test. ",
    llm=groq_LLM,
    verbose=True
)
#step 2 : Give the task to agent
test_case_task = Task(
    description="create 5-20 test cases",
    expected_output="A numbered list of 5-10 test cases with brief description of app.vwo.com for login page with username and password with submit button and remember me password functionality",
    agent=qa_agent
)
#step 3: add them to crew
crew = Crew(
    agents=[qa_agent],
    tasks=[test_case_task],
    verbose=True
)

if __name__ == "__main__":
    result = crew.kickoff()
    print(result)