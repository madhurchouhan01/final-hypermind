from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from hypermindz.tools.custom_tool import calculate_channel_metrics
from crewai.memory import LongTermMemory
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from pydantic import BaseModel

class ParsedQuery(BaseModel):
    audience_size : int
    total_budget  : int
    flight        : int
    adult_pop     : int

@CrewBase
class InvestmentCrew():
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def basic_qna_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['basic_qna_agent'],            
            verbose=True
        )

    @agent
    def query_parser_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['query_parser_agent'],
            verbose=True,
        )
    
    # @agent
    # def calculation_agent(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['calculation_agent'],
    #         tools=[calculate_channel_metrics],
    #         verbose=True,
    #     )

    # @agent
    # def sensitivity_analysis_agent(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['sensitivity_analysis_agent'],
    #         tools=[calculate_channel_metrics],
    #         verbose=True,
    #     )

    @agent
    def task_router_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['task_router_agent'],
            verbose=True,
            allow_delegation=True,
        )


    @task
    def qna_parsing_task(self) -> Task:
        return Task(
            config=self.tasks_config['qna_parsing_task'],
            agent=self.basic_qna_agent(),
        )
    @task
    def parse_query(self) -> Task:
        return Task(
            config=self.tasks_config['parse_query'],
            agent=self.query_parser_agent(),
            output_json=ParsedQuery,
        )
    # @task
    # def calculation_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['analyze_sensitivity'],
    #         agent=self.calculation_agent(),
    #         context=[self.parse_query],
    # calculation_agent, sensitivity_analysis_agent, "
    #             "report_generator_agent, and goal_oriented_agent
    #     )


    @crew
    def crew(self) -> Crew:

        return Crew(
            agents=[self.basic_qna_agent(),self.query_parser_agent()],
            tasks=self.tasks,
            process=Process.hierarchical,
            verbose=True,
            memory=True,
            planning=True,
            manager_llm="gpt-4o",
            manager_agent=self.task_router_agent(),
        )