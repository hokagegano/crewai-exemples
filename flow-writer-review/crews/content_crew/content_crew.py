from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import os

os.environ["OTEL_SDK_DISABLED"] = "true"

@CrewBase
class ContentCrew():
    """Content writing crew"""

    @agent
    def content_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['content_writer'],
            verbose=True
        )

    @agent
    def content_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['content_reviewer'],
            verbose=True
        )

    @task
    def write_section_task(self) -> Task:
        return Task(
            config=self.tasks_config['write_section_task']
        )

    @task
    def review_section_task(self) -> Task:
        return Task(
            config=self.tasks_config['review_section_task'],
            context=[self.write_section_task()]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the content writing crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

    