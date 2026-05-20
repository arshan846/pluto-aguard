from langchain.agents import AgentExecutor, initialize_agent
from langchain.tools import Tool

agent = initialize_agent(tools=tools, llm=llm, verbose=True, allow_dangerous_requests=True)
