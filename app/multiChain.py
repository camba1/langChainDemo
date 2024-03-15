from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
# ChatPromptTemplate allow the creation of prompt with multiple personas (sys, user, etc..)
from langchain_core.prompts import ChatPromptTemplate
# PromptTemplate allow the creation of prompt from a simple string
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda


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


def routable_chain():

    model = ChatOpenAI(temperature=MODEL_TEMPERATURE, model=MODEL_NAME)

    classify_prompt_text = """You are an expert in science fiction movies. In particular you are well verse in the
    movies from 'Star Trek' and 'Star Wars'. Classify if the user question below refers to 'Star Trek', 'Star Wars' 
    or 'other'.
     Keep you answer to a maximum of two words.
     
     <question>
     {question}
     </question>
     
     Classification:"""

    classify_prompt = PromptTemplate.from_template(classify_prompt_text)

    classification_chain = classify_prompt | model | StrOutputParser()

    startrek_model = ChatOpenAI(temperature=MODEL_TEMPERATURE, model=STAR_TREK_MODEL_NAME)

    startrek_prompt_text = """You are an expert in Star Trek movies.
        Answer all the questions with " Spock once mentioned that"
        
        Question:{question} 
        Answer:"""

    startrek_prompt = PromptTemplate.from_template(startrek_prompt_text)

    startrek_chain = startrek_prompt | startrek_model | StrOutputParser()

    starwars_model = ChatOpenAI(temperature=MODEL_TEMPERATURE, model=STAR_WARS_MODEL_NAME)

    starwars_prompt_text = """You are an expert in Star Wars movies.
        Answer all the questions with "As Leia always says"
        
        Question:{question} 
        Answer:"""

    starwars_prompt = PromptTemplate.from_template(starwars_prompt_text)

    starwars_chain = starwars_prompt | starwars_model | StrOutputParser()

    general_prompt_text = """You are an expert in Star Wars movies.
        Answer all the questions with "As Leia always says"

        Question:{question} 
        Answer:"""

    general_prompt = PromptTemplate.from_template(general_prompt_text)

    general_chain = general_prompt | model | StrOutputParser()

    route = lambda x : startrek_chain if "star trek" in x["topic"].lower() \
        else (starwars_chain if "star wars" in x["topic"].lower() else general_chain)

    complete_chain = {"topic": classification_chain, "question": lambda x : x["question"]} | RunnableLambda(route)

    return complete_chain


result = routable_chain().invoke({"question": "Who is Hans Solo?"})
print(result)