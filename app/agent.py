from langchain_core.tools import tool
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableSerializable

from langchain.pydantic_v1 import BaseModel


# Model constants
MODEL_NAME = "gpt-3.5-turbo"
MODEL_TEMPERATURE = 0

#  Prompt name to the used to pull from the langChain Hub
HUB_RAG_PROMPT = "hwchase17/openai-tools-agent"


model = ChatOpenAI(temperature=MODEL_TEMPERATURE, model_name=MODEL_NAME)


# Class used to indicate the expected input format since the Agent runnable does not expose by default
class AgentInput(BaseModel):
    input: str

# Define the tools we are going to use the decorator makes it easier to declare them
@tool
def multiply(first_int: int, second_int: int) -> int:
    """Multiply two integers together."""
    return first_int * second_int


@tool
def add(first_int: int, second_int: int) -> int:
    """Add two integers."""
    return first_int + second_int


@tool
def exponentiate(base: int, exponent: int) -> int:
    """Update the base to the exponent power."""
    return base**exponent


def build_agent() -> RunnableSerializable:
    """
    Build the agent executor that will be responsible to answer the user's question
    :return: The agent executor object
    """

    prompt = hub.pull(HUB_RAG_PROMPT)
    # prompt.pretty_print()

    tools = [multiply, add, exponentiate]

    # Construct the Tools agent
    agent = create_openai_tools_agent(model, tools, prompt)

    # Create an agent executor by passing in the agent and tools
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False).with_types(input_type=AgentInput) | (lambda x: x["output"])

    return agent_executor

# result = build_agent().invoke(
#     {
#         "input": "Take 3 to the fifth power and multiply that by the sum of twelve and three, then square the whole result"
#     }
# )
#
# print(result)
