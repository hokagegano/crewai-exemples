from crewai import Agent, Crew, Process, Task
from crewai import LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
    DirectorySearchTool,
    FileReadTool,
    # SerperDevTool,
    # WebsiteSearchTool,
	# FirecrawlCrawlWebsiteTool,
	# ScrapeWebsiteTool
)
import os
os.environ["OTEL_SDK_DISABLED"] = "true"
from crewai.memory import ShortTermMemory
from crewai.memory.storage.rag_storage import RAGStorage

# from devteam.tools.custom_tool import MyCustomTool 
# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators
i=0

@CrewBase
class Devteam():
	"""Devteam crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def senior_engineer_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['senior_engineer_agent'],
			allow_delegation=False,
			verbose=True
		)
	@agent
	def senior_design_engineer_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['senior_design_engineer_agent'],
			allow_delegation=False,
			verbose=True
		)
    
	# @agent
	# def qa_engineer_agent(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['qa_engineer_agent'],
	# 		allow_delegation=True,
	# 		verbose=True
	# 	)
	
	# @agent
	# def manager(self) -> Agent:
	# 	return Manager(
	# 		config=self.agents_config['manager'],
	# 		allow_delegation=True,
	# 		verbose=True
	# 	)
	
	# @agent
	# def chief_qa_engineer_agent(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['chief_qa_engineer_agent'],
	# 		allow_delegation=True,
	# 		verbose=True
	# 	)

	# @agent
	# def chief_qa_engineer_agent(self) -> Agent:
	# 	return Agent(
	# 		role="Project Manager",
	# 		goal="Efficiently manage the crew and ensure high-quality task completion",
	# 		backstory="You're an experienced project manager, skilled in overseeing complex projects and guiding teams to success.",
	# 		allow_delegation=True,
	# 	)


	@task
	def code_task(self) -> Task:
		return Task(
			i=i+1,
			config=self.tasks_config['code_task'],
			agent=self.senior_engineer_agent(),
			# concatentate the output file name with the task number
			output_file=f'reportCodeTask_Deepseekr1{i}.md'
						# output_file='reportCodeTask.md'
			# output_file='reportCodeTask_{i}.md'			
		)

	@task
	def design_task(self) -> Task:
		return Task(
			i=i+1,
			config=self.tasks_config['design_task'],
			agent=self.senior_design_engineer_agent(),
			output_file=f'reportDesign_Deepseekr1{i}.md'
		)

	# @task
	# def review_task(self) -> Task:
	# 	return Task(
	# 		i=i+1,
	# 		config=self.tasks_config['review_task'],
	# 		agent=self.qa_engineer_agent(),
	# 		output_file=f'reportReview_{i}.md'
	# 		#### output_json=ResearchRoleRequirements
	# 	)

	# @task
	# def evaluate_task(self) -> Task:
	# 	return Task(
	# 		i=i+1,
	# 		config=self.tasks_config['evaluate_task'],
	# 		agent=self.chief_qa_engineer_agent(),
	# 		output_file=f'reportFinal_{i}.md'
	# 	)

	@crew
	def crew(self) -> Crew:
		"""Creates the Devteam crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge
		manager = Agent(
			role="Project Manager",
			goal="Efficiently manage the crew and ensure high-quality task completion",
			backstory="You're an experienced project manager, skilled in overseeing complex projects and guiding teams to success. Your role is to coordinate the efforts of the crew members, ensuring that each task is completed on time and to the highest standard. If any issue or missing features are identified, you must reiterate the task to the appropriate team member, until all taks are done.",
			allow_delegation=True,
			output_file=f'reportManager_Deepseekr1{i}.md'
			# expected_output="The full code backend and frontend, in markdown format.",
		)
		return Crew(
			agents=self.agents,
			# agents=[self.senior_engineer_agent,self.senior_design_engineer_agent,self.qa_engineer_agent], # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			# process=Process.sequential,
			verbose=True,
			# agents=[self.senior_engineer_agent, self.qa_engineer_agent],
			# manager_agent=self.chief_qa_engineer_agent.agent,  # Use your custom manager agent
			process=Process.hierarchical,
			respect_context_window=True,
			# memory = True,
			planning=True,
			planning_llm = LLM(model="ollama/deepseek-r1:14b", base_url="http://localhost:11434"),
			# manager_llm = LLM(model="ollama/llama3.2", base_url="http://localhost:11434"),
			manager_llm = LLM(model="ollama/deepseek-r1:14b", base_url="http://localhost:11434"),
			manager_agent=manager,
			short_term_memory = ShortTermMemory(
        		storage = RAGStorage(
                embedder_config={
                    "provider": "ollama",
                    "config": {
                        "model": 'mxbai-embed-large'
                    }
                },
                type="short_term",
                path="./memory/"
            )
        	)
		)
