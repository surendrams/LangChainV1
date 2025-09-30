from langchain.agents import create_agent, AgentState
import os
from dotenv import load_dotenv
from rich import print as rprint

from langchain.agents import create_agent

load_dotenv()

def check_weather(location: str) -> str:
    '''Return the weather forecast for the specified location.'''
    return f"It's always sunny in {location}"

agent = create_agent(
    model= os.getenv("MODEL_NAME") or "openai:gpt-4o-mini",
    tools=[check_weather],
    prompt="You are a helpful assistant",
)
inputs = {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
for chunk in agent.stream(inputs, stream_mode="updates"):
    rprint(chunk)
