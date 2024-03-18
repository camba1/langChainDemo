import langsmith
from langchain import chat_models, prompts, smith
# from langchain.schema import output_parser

# -------------Model definition for model we want to evaluate --------------
from os import getenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


OPENROUTER_BASE = "https://openrouter.ai"
OPENROUTER_API_BASE = f"{OPENROUTER_BASE}/api/v1"
MODEL_NAME = "nousresearch/nous-hermes-2-mixtral-8x7b-dpo"


MODEL_TEMPERATURE = 0.8
openrouter_api_key=getenv("OPENROUTER_API_KEY")


model = ChatOpenAI(temperature=MODEL_TEMPERATURE,
                   model=MODEL_NAME,
                   openai_api_key=openrouter_api_key,
                   openai_api_base=OPENROUTER_API_BASE,
                   )

prompt_text = """Your are a helpful assistant.
Tell me in which movies this fictional character appears {input}. Be concise."""

prompt = ChatPromptTemplate.from_template(prompt_text)

chain = prompt | model | StrOutputParser()

# -------------Evaluators definition  --------------

# Define the evaluators to apply
eval_config = smith.RunEvalConfig(
    evaluators=[
        "cot_qa",
        smith.RunEvalConfig.LabeledCriteria("relevance"),
        smith.RunEvalConfig.LabeledCriteria("insensitivity")
    ],
    custom_evaluators=[],
    eval_llm=ChatOpenAI(model="gpt-4", temperature=0)
)

client = langsmith.Client()
chain_results = client.run_on_dataset(
    dataset_name="Movie Characters",
    llm_or_chain_factory=chain,
    evaluation=eval_config,
    project_name="Fourth-Run",
    concurrency_level=5,
    verbose=True,
)