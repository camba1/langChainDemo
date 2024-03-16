from os import getenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


OPENROUTER_BASE = "https://openrouter.ai"
OPENROUTER_API_BASE = f"{OPENROUTER_BASE}/api/v1"
MODEL_NAME = "nousresearch/nous-hermes-2-mixtral-8x7b-dpo"


# Model constants
# MODEL_NAME = "openrouter/auto"
MODEL_TEMPERATURE = 0.8
openrouter_api_key=getenv("OPENROUTER_API_KEY")
print(openrouter_api_key)

model = ChatOpenAI(temperature=MODEL_TEMPERATURE,
                   model=MODEL_NAME,
                   openai_api_key=openrouter_api_key,
                   openai_api_base=OPENROUTER_API_BASE,
                   )

prompt_text = """Your are a helpful assistant.
Tell me in which movies this fictional character appears {input}. Be concise."""

prompt = ChatPromptTemplate.from_template(prompt_text)


chain = prompt | model | StrOutputParser()