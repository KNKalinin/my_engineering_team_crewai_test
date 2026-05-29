from crewai import Agent, Crew, Process, Task,LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import os



from dotenv import load_dotenv


load_dotenv(override=True)
API_KEY = os.getenv("OPENROUTER_API_KEY")


#engineering_lead =LLM(model="ollama/qwen3:14b",base_url="http://localhost:11434",api_key="ollama",) #num_ctx=7000
#backend_engineer = LLM(model="ollama/qwen2.5-coder:14b",base_url="http://localhost:11434",api_key="ollama",num_ctx=7000)
#frontend_engineer = LLM(model="ollama/qwen2.5-coder:14b",base_url="http://localhost:11434",api_key="ollama",num_ctx=7000)
#test_engineer = LLM(model="ollama/qwen2.5-coder:14b",base_url="http://localhost:11434",api_key="ollama",num_ctx=7000)

#engineering_lead =LLM(model="openrouter/google/gemini-2.5-flash-lite-preview-06-17",base_url="https://openrouter.ai/api/v1",api_key=API_KEY)
engineering_lead =LLM(model="openrouter/google/gemini-2.5-pro",base_url="https://openrouter.ai/api/v1",api_key=API_KEY)
#backend_engineer = LLM(model="openrouter/moonshotai/kimi-k2:free",base_url="https://openrouter.ai/api/v1",api_key=API_KEY)
#frontend_engineer = LLM(model="openrouter/moonshotai/kimi-k2:free",base_url="https://openrouter.ai/api/v1",api_key=API_KEY)
backend_engineer = LLM(model="openrouter/anthropic/claude-sonnet-4",base_url="https://openrouter.ai/api/v1",api_key=API_KEY)
frontend_engineer = LLM(model="openrouter/anthropic/claude-sonnet-4",base_url="https://openrouter.ai/api/v1",api_key=API_KEY)
#test_engineer= LLM(model="openrouter/moonshotai/kimi-k2:free",base_url="https://openrouter.ai/api/v1",api_key=API_KEY)



@CrewBase
class MyEngineeringTeam():
    """MyEngineeringTeam crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    @agent
    def engineering_lead(self) -> Agent:
        return Agent(
            config=self.agents_config['engineering_lead'],
            verbose=True,
            llm=engineering_lead
        )
    
    @agent
    def backend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_engineer'],
            verbose=True,
            llm=backend_engineer,
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety
            max_execution_time=500, 
            max_retry_limit=3
        )
    
    @agent
    def frontend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_engineer'],
            verbose=True,
            llm=frontend_engineer
        )
    """ 
    @agent
    def test_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['test_engineer'],
            verbose=True,
            llm=test_engineer,
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety
            max_execution_time=500, 
            max_retry_limit=3 
        )
    """
    @task
    def design_task(self) -> Task:
        return Task(
            config=self.tasks_config['design_task']
        )

    @task
    def code_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_task'],
        )

    @task
    def frontend_task(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_task'],
        )
    """ 
    @task
    def test_task(self) -> Task:
        return Task(
            config=self.tasks_config['test_task'],
        )   
    """
    @crew
    def crew(self) -> Crew:
        """Creates the engeenering crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )