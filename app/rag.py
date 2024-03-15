import os

# Chat imports
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser

# RAG imports
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain import hub
from langchain.schema.runnable import RunnablePassthrough
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Model constants
MODEL_NAME = "gpt-3.5-turbo"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
MODEL_TEMPERATURE = 0

# Document embedding constants
CHUNK_SIZE = 26
CHUNK_OVERLAP = 5

#  Prompt name to the used to pull from the langChain Hub
HUB_RAG_PROMPT = "rlm/rag-prompt"

# This is necessary to avoid an issue with running the Hugging face embedding model
os.environ["TOKENIZERS_PARALLELISM"] = "false"

model = ChatOpenAI(temperature=MODEL_TEMPERATURE, model_name=MODEL_NAME)
output_parser = StrOutputParser()
prompt = hub.pull(HUB_RAG_PROMPT)
# print(f"RAG prompt: {prompt}")


def import_data(path):
    """
    Import file from path and split it into chucks
    :param path: Path to the file
    :return: documents containing the different chunks
    """
    loader = TextLoader(path)
    markdown_document = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    docs = splitter.split_documents(markdown_document)
    return docs


def populate_db():
    """
    Load document chunks into the DB as vector embeddings
    :return: Retriever object that can be used in chains to do similarity searches
    """
    filepath = os.path.dirname(os.path.realpath(__file__))
    docs = import_data(f'{filepath}/data/cwit2020.md')
    # print(docs[0])

    vector_store = Qdrant.from_documents(documents=docs,
                                         embedding=HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME),
                                         location=":memory:",
                                         collection_name="rag_collection"
                                         )

    retriever = vector_store.as_retriever()
    return retriever


retriever = populate_db()


def build_chain():
    """
    Define the chain that will be used to answer the user's question. This can be called from client.
    :return: Chain object
    """

    prompt_mapper = {"context": retriever, "question": RunnablePassthrough()}

    rag_chain = prompt_mapper | prompt | model | output_parser

    return rag_chain

# result = build_chain().invoke("What year was the CWIT conference")
# print(result)
