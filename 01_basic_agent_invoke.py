import os
from dotenv import load_dotenv

from langchain.agents import create_agent
from rich import print as rprint

load_dotenv()

def get_weather(city: str) -> str:
    """
    Get the weather for a given city.
    """
    return f"It's always Sunny in {city}!"

agent = create_agent(
    #model="openai:gpt-4o-mini", 
    model= os.getenv("MODEL_NAME") or "openai:gpt-4o-mini",
    tools=[get_weather],
    prompt="You are a helpful assistant",
)

#Run agent
response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)

rprint(response)
