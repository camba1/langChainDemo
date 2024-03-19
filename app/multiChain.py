from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
# ChatPromptTemplate allow the creation of prompt with multiple personas (sys, user, etc..)
from langchain_core.prompts import ChatPromptTemplate
# PromptTemplate allow the creation of prompt from a simple string
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import RunnableSerializable
from langchain.pydantic_v1 import BaseModel

# Model constants
MODEL_NAME = "gpt-3.5-turbo"
INVENTIVE_MODEL_TEMPERATURE = 0.8
PRIMARY_MODEL_NAME = "gpt-fake"

STAR_TREK_MODEL_NAME = "gpt-3.5-turbo"
STAR_WARS_MODEL_NAME = "gpt-4"
MODEL_TEMPERATURE = 0


def chain_with_fallback():
    """
    Performs a chat conversation using a fallback mechanism.
    The function creates a `chain` by calling the `with_fallbacks` method on the primary chain and passing
    the secondary chain as a fallback. This ensures that if the primary chain fails, the secondary chain will be
    invoked automatically.
    """

    model = ChatOpenAI(temperature=INVENTIVE_MODEL_TEMPERATURE, model=MODEL_NAME)
    chat_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You're a nice assistant who always includes a compliment in your response",
            ),
            ("human", "Why did the {animal} cross the road"),
        ]
    )

    chat_model = ChatOpenAI(model_name=PRIMARY_MODEL_NAME)
    bad_chain = chat_prompt | chat_model | StrOutputParser()

    # This line fails because there is no gpt-fake model
    # bad_chain.invoke({"animal": "chicken"})

    good_chain = chat_prompt | model | StrOutputParser()

    # This succeeds because it calls the bad model first and sice tha fails, it automatically
    # calls the good model.
    chain = bad_chain.with_fallbacks([good_chain])

    return chain


# result = chain_with_fallback().invoke({"animal": "chicken"})
# print(result)


def create_chain(prompt_text: str, model_temperature, model_name) -> RunnableSerializable:
    """
    Create a new chain object
    :param prompt_text: Text that will e used as part of the prompt sent to llm
    :param model_temperature: Zero to 1 where zero is factual and 1 imaginative
    :param model_name: Name of the model to use
    :return: New chain object
    """
    model = ChatOpenAI(temperature=model_temperature, model=model_name)
    classify_prompt = PromptTemplate.from_template(prompt_text)
    classification_chain = classify_prompt | model | StrOutputParser()
    return classification_chain


# Class used to indicate the expected input format since the Agent runnable does not expose by default
class QuestionInput(BaseModel):
    question: str


def routable_chain():
    # Initial chain
    classify_prompt_text = """You are an expert in science fiction movies. In particular you are well verse in the
    movies from 'Star Trek' and 'Star Wars'. Classify if the user question below refers to 'Star Trek', 'Star Wars' 
    or 'other'.
     Keep you answer to a maximum of two words.

     <question>
     {question}
     </question>

     Classification:"""
    classification_chain = create_chain(classify_prompt_text, MODEL_TEMPERATURE, MODEL_NAME)

    # chain 1
    startrek_prompt_text = """You are an expert in Star Trek movies.
        Answer all the questions starting with " Spock once mentioned that"
        
        Question:{question} 
        Answer:"""
    startrek_chain = create_chain(startrek_prompt_text, MODEL_TEMPERATURE, STAR_TREK_MODEL_NAME)

    # Chain 2
    starwars_prompt_text = """You are an expert in Star Wars movies.
        Answer all the questions starting with "As Leia always says"
        
        Question:{question} 
        Answer:"""
    starwars_chain = create_chain(starwars_prompt_text, MODEL_TEMPERATURE, STAR_WARS_MODEL_NAME)

    # chain 3
    general_prompt_text = """You are helpful assistant.
        Answer all the questions starting with "I do believe"

        Question:{question} 
        Answer:"""
    general_chain = create_chain(general_prompt_text, MODEL_TEMPERATURE, MODEL_NAME)

    # Final Chain (Composite of all other chains)
    route = lambda x: startrek_chain if "star trek" in x["topic"].lower() \
                    else (starwars_chain if "star wars" in x["topic"].lower()
                    else general_chain)

    final_chain = {"topic": classification_chain, "question": lambda x: x["question"]} | RunnableLambda(route)

    return final_chain.with_types(input_type=QuestionInput)

# result = routable_chain().invoke({"question": "Who is Hans Solo?"})
# print(result)
# result = routable_chain().invoke({"question": "Who is captain Kirk?"})
# print(result)
# result = routable_chain().invoke({"question": "Who is Madonna?"})
# print(result)
