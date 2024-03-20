# LangChainDemo

This repository shows a number of AI powered LangChain examples. The repo was used to present a talk at AICamp. It uses:

- **LangServe** to create and serve the application inference endpoints
- **Langchain** to interact with the LLM models and build the application logic.
- The examples use OpenAI GPT 3.5 Turbo, GPT 4 as well as Nous Hermes 2 Mixtral 8x7B MoE (via [OpenRouter](https://openrouter.ai/docs#quick-start))
- **LangSmith** integration for observability metrics and evaluation. See the section on Langsmith for details 
on how to enable sending data to Langsmith

The sister repository [LangChain Demo Client](https://github.com/camba1/langchainDemoClient ) includes simple client examples that can be used to call 
this application using [Gradio](https://www.gradio.app), [Streamlit](https://streamlit.io), 
[Chainlit](https://chainlit.io) and plain Python package remote calls.

### Simple Chains

![myChain_Simple.png](doc%2Fimages%2FmyChain_Simple.png)

![openRouter.png](doc%2Fimages%2FopenRouter.png)

### Naive RAG

![ragChain_1.png](doc%2Fimages%2FragChain_1.png)

![ragChain_2.png](doc%2Fimages%2FragChain_2.png)

### Other

![multichain_fallback.png](doc%2Fimages%2Fmultichain_fallback.png)

![agent.png](doc%2Fimages%2Fagent.png)

![multiChain_routable.png](doc%2Fimages%2FmultiChain_routable.png)


## Repository organization

The repo is organized as follows:
- **app**: Contains the main application as well as most of the examples of this demo
- **doc/images**: Images included in this document
- **Evaluation**: Sample evaluation script. Note that you will need to modify the model name and dataset name as well 
as providing you our OpenRouter API key to use this example.
- **Packages**: External packages installed from the [Langchain templates repo](https://templates.langchain.com/)

## Installation

Install the LangChain CLI if you haven't yet

```bash
pip install -U langchain-cli
```

Install Poetry following the instructions [here](https://python-poetry.org/docs/#installing-with-the-official-installer).
Install all the dependencies and activate your environment


```bash
poetry install
poetry shell
```

## Set the environment variables

Setup Environment variables to call the LLM providers. Note that the OpenRouter key is only needed in the openRouter 
example and the sample evaluation script. So, if you are not using those examples, you do not need to set that variable.

```bash
export OPENAI_API_KEY=<yourOpenAiAPIkey>
export OPENROUTER_API_KEY=<yourOpenRouterkey>
```

## Adding additional packages

The repo comes with the 'pirate speak' package installed, but you can choose the add additional packages 
following the directions below

```bash
# adding packages from 
# https://github.com/langchain-ai/langchain/tree/master/templates
langchain app add $PROJECT_NAME

# adding custom GitHub repo packages
langchain app add --repo $OWNER/$REPO
# or with whole git string (supports other git providers):
# langchain app add git+https://github.com/hwchase17/chain-of-verification

# with a custom api mount point (defaults to `/{package_name}`)
langchain app add $PROJECT_NAME --api_path=/my/custom/path/rag
```

Note: you remove packages by their api path

```bash
langchain app remove my/custom/path/rag
```

## Setup LangSmith (Optional)
LangSmith will help us trace, monitor and debug LangChain applications. 
You can sign up for a free Langsmith account [here](https://smith.langchain.com/). 
If you don't have access, you can skip this section, but you will be missing out on some pretty 
amazing stuff :) 


```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # if not specified, defaults to "default"
```

## Launch the application using LangServe locally

```bash
langchain app serve
```

## Running the application using LangServe in Docker

This project folder includes a Dockerfile that allows you to easily build and host your LangServe app.

### Building the Image

To build the image, you simply:

```shell
docker build . -t my-langserve-app
```

If you tag your image with something other than `my-langserve-app`,
note it for use in the next step.

### Running the Image Locally

To run the image, you'll need to include any environment variables
necessary for your application.

In the below example, we inject the `OPENAI_API_KEY` environment
variable with the value set in my local environment
(`$OPENAI_API_KEY`)

We also expose port 8080 with the `-p 8080:8080` option.

```shell
docker run -e OPENAI_API_KEY=$OPENAI_API_KEY -p 8080:8080 my-langserve-app
```
## Deploying to AWS with AWS Copilot

install copilot if not already installed

```bash
brew install aws/tap/copilot-cli
```

Deploy the application

```bash
copilot init --app [application-name] --name [service-name] --type 'Load Balanced Web Service' --dockerfile './Dockerfile' --deploy
```

To remove the application from AWS, run the following command:

```bash
copilot app delete
```

Note that Copilot can sometimes leave IAM roles behind, sp please ensure that everything has been removed from 
your AWS account


## Useful Resources

- LangSmith Docs: https://docs.smith.langchain.com/tracing
- Langserve Application templates: https://templates.langchain.com
- LangChain Hub: https://smith.langchain.com/hub
- LangChain Python documentation: https://python.langchain.com/
- LangChain JS documentation: https://js.langchain.com
- Blog: https://blog.langchain.dev/
- Discord: https://discord.gg/cU2adEyC7w
- Repo for this demo: 
  - Backend: https://github.com/camba1/langChainDemo
  - Frontend: https://github.com/camba1/langchainDemoClient 