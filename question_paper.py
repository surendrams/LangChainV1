import os
from pydantic import BaseModel, Field
from typing import Dict, List, Any
from langchain.agents import create_agent
from rich import print as rprint
from pydantic import create_model
import re

MCQResponse = create_model("MCQResponse", **{
    "question": (str, ...),
    "options": (List[Dict[str, str]], ...),
    "correct_option": (str, ...),
    "justification": (str, ...)
})


def extract_code_and_text(raw: str) -> tuple[str, list[Any]]:
    code_pattern = re.compile(pattern=r"```(?:\w+)?\n(.*?)```", flags=re.DOTALL)
    code_snippets = code_pattern.findall(string=raw)

    text_without_code = code_pattern.sub(repl="", string=raw).strip()
    return text_without_code, code_snippets

def handle_agent_response(resp: MCQResponse): # type: ignore
    # Extract text + code from question
    q_text, code_blocks = extract_code_and_text(raw=resp.question)

    # Normalize options
    options = {list(opt.keys())[0]: list(opt.values())[0] for opt in resp.options}

    return {
        "question_text": q_text,
        "code_snippets": code_blocks,
        "options": options,
        "correct_option": resp.correct_option,
        "justification": resp.justification
    }

from dotenv import load_dotenv

load_dotenv()

# class MCQResponse(BaseModel):
#     question: str = Field(..., description="The generated multiple-choice question")
#     options: List[Dict[str, str]] = Field(
#         ...,
#         description="List of 4 options as objects with keys A, B, C, D and their values"
#     )
#     correct_option: str = Field(..., description="The correct option letter: A, B, C, or D")
#     justification: str = Field(..., description="Detailed explanation of the correct answer")


agent = create_agent(
    model= os.getenv("MODEL_NAME") or "openai:gpt-4o-mini",
    tools=[],
    response_format=MCQResponse,
    prompt="""
    You are a helpful Tutor Agent.
    Generate one multiple-choice question for the given subject.
    
    Output format (schema):
    - question: The question text
    - options: List of exactly 4 dicts, e.g.
      [{"A": "option text"}, {"B": "option text"}, {"C": "option text"}, {"D": "option text"}]
    - correct_option: One of A, B, C, D
    - justification: Detailed explanation (step by step manner, make sure these steps are properly aligned into new section) of why the correct option is right and others are wrong.
    """
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Generate a question for the subject: Algebra slope for 8th Grade"}]
})

rprint(handle_agent_response(result['structured_response']))

