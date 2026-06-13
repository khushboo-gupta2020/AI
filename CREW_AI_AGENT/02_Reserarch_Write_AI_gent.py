#This is a senior QA with 15 years of experience.
#  Based on the feature, it will analyze the requirement
#  and suggest a 5-day test case, P0 test case. 
from crewai import LLM, Agent, Task, Crew
from dotenv import load_dotenv
import os

load_dotenv()

# Patch: Groq doesn't support cache_breakpoint. Make mark_cache_breakpoint a no-op.
import crewai.llms.cache as _cache
_cache.mark_cache_breakpoint = lambda msg: msg


#step 0: brain
groq_LLM = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_KEY")
)

#step 1: define the agent identity
writer_agent = Agent(
    role="QA Documentation Writer",
    goal=" Create clear actionable bug prevention guidelines",
    backstory="You are a technical writer specializing in QA documentation. Utilize complex bug detection to create a simple actionable checklist that developers can follow. ",
    llm=groq_LLM,
    verbose=True
) 

researcher_agent = Agent(
    role="QA Research Analyst",
    goal="Find the common bugs in the application",
    backstory="You are a QA researcher who has analyzed thousands of bug reports across web applications. You specialized in identifying patterns and trends in software defects."
    " and preparing the test. ",
    llm=groq_LLM,
    verbose=True
) 
Researcher_task =Task(
    description="research and list the top 5 most common bug categories in the modern web applications.For each catgory, provide:name, frequency(percentage) ,example,impact level",
    expected_output="A ranked list of 5 bug categories, name, frequency, example, and impact for each ",
    agent=researcher_agent
)

#step 2 : Give the task to agent
writing_task = Task(
    description="Based on the research provided, create a bug prevention checklist that developers can use before submitting a pull request. Make it practical and actionable.",
    expected_output="A format called checklist with 5 to 10 items that developers can quickly review before code submission.",
    agent=writer_agent
)
#step 3: add them to crew
crew = Crew(
    agents=[researcher_agent,writer_agent],
    tasks=[Researcher_task ,writing_task ],
    verbose=True
)

if __name__ == "__main__":
    result = crew.kickoff()
    print(result)