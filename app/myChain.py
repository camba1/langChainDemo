from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Model constants
MODEL_NAME = "gpt-3.5-turbo"
MODEL_TEMPERATURE = 0

model = ChatOpenAI(temperature=0.8, model=MODEL_NAME)

prompt_text = """Your are a helpful assistant.
Tell me in which movies this fictional character appears {input}. Be concise."""

prompt = ChatPromptTemplate.from_template(prompt_text)


chain = prompt | model | StrOutputParser()


