from langchain.agents import create_agent, AgentState
from langchain_openai import ChatOpenAI
from langchain_anthropic.chat_models import ChatAnthropic
from langgraph.runtime import Runtime
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage


from dotenv import load_dotenv

load_dotenv()

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

@tool
def calculate(expression: str) -> str:
    """Perform calculations."""
    return str(eval(expression))

def select_model(state: AgentState, runtime: Runtime) -> ChatOpenAI | ChatAnthropic:
    """Choose model based on conversation complexity."""
    messages = state["messages"]
    message_count = len(messages)

    if message_count > 10:
        return ChatOpenAI(model="gpt-4.1-mini")
    else:
        return ChatAnthropic(model_name="claude-3-5-sonnet-latest",temperature=0, timeout=None,  max_retries=2, stop=["\n\nHuman:"])
    
agent = create_agent(select_model, tools=[])

result = agent.invoke({
    "messages": [
        HumanMessage(content="what is your name")
    ]
})

print(result)