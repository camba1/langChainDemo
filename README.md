# LangChainDemo

This repository shows a number of AI powered LangChain application examples. 
The repo was used to present a talk at AICamp. It uses:

- **LangServe** to create and serve the application inference endpoints
- **LangChain Templates** to pull pre-existing application templates
- **Langchain** to interact with the LLM models and build the application logic.
- **LangChain Hub** to pull pre-existing LLM prompts
- **OpenAI GPT 3.5 Turbo**, **GPT 4** as well as **Nous Hermes 2 Mixtral 8x7B MoE** (via [OpenRouter](https://openrouter.ai/docs#quick-start))
- **LangSmith** integration for observability, tracing, metrics and evaluation. See the section on Langsmith for details 
on how to enable sending data to Langsmith

The sister repository [LangChain Demo Client](https://github.com/camba1/langchainDemoClient ) includes simple client examples that can be used to call 
this application using: 
- [Gradio](https://www.gradio.app)
- [Streamlit](https://streamlit.io)
- [Chainlit](https://chainlit.io)
- Simple Python package remote calls.

## Quick start

To get the application going quickly, assuming you already have the Langchain-cli 
(`pip install -U langchain-cli`) and [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer) installed:

```shell
git clone https://github.com/camba1/langChainDemo.git
cd langChainDemo
poetry install
poetry shell
export OPENAI_API_KEY=<YOUR OPENAI_API_KEY>
export OPENROUTER_API_KEY=<YOUR OPENROUTER_API_KEY> 
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<YOUR LANGCHAIN_API_KEY>
export LANGCHAIN_PROJECT="Test Project"    
langchain app serve  
```
The application will be launched at http://127.0.0.1:8000 and you can visit 
[langsmith](https://smith.langchain.com) to see traces/metrics from running the application


To get the API keys needed, visit:
- OpenAI: https://openai.com
- OpenRouter: https://openrouter.ai
- Langchain: https://www.langchain.com/langsmith

Note that running this project as configured will call OpenAI and OpenRouter endpoints. This will have a **modest cost**,
but it will unfortunately **not free**.

Refer to the information on the rest of the document for more details on getting started with the application

## Diagrams of the different chains used in the application

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
  - **agent.py**: Uses an agent and tools for addition, multiplication and exponentiation tools to allow LLM to perform math
  - **multichain.py**: Contains two chains:
    - **Chain with back**: Show how to set up a fallback chain in case there is an error in the main chain
    - **Routable chain**: Uses a routing chain to send the user's query to the appropriate 'expert' chain
  - **openRouter.py**: Shows how you can use LangChain with OpenRouter, which exposes a number of models using the OpenAI API
  - **rag.py**: Create a simple RAG chain to query the document in the app/data directory
  - **server.py**: Main code to run the FastAPI webServer. Contains all the different application routes
- **doc/images**: Images included in this document
- **Evaluation**: Sample model evaluation script. Script runs a model 5 times and checks the responses for 
relevance and insensitivity
- **Packages**: External packages installed from the [Langchain templates repo](https://templates.langchain.com/). 
In this case we have installed and used the **pirate speak** template. We also configured the WebServer endpoint for
this example to use the new **Playground** interface that also allows the end user to provide feedback and to link to the 
**LangSmith** trace of the run. Note, that for these additional buttons to show up in the screen LangSmith must be
enabled for the project (See Langsmith section below)

## Installation

### Prerequisites

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

### Set the environment variables

Setup Environment variables to call the LLM providers. Note that the OpenRouter key is only needed in the openRouter 
example and the sample evaluation script. So, if you are not using those examples, you do not need to set that variable.

```bash
export OPENAI_API_KEY=<yourOpenAiAPIkey>
export OPENROUTER_API_KEY=<yourOpenRouterkey>
```

### Adding additional packages (Optional)

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

### Setup LangSmith (Optional)
LangSmith will help us trace, monitor and debug LangChain applications. 
You can sign up for a free Langsmith account [here](https://smith.langchain.com/). 
If you don't have access, you can skip this section, but you will be missing out on some pretty 
cool stuff :) 


```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # if not specified, defaults to "default"
```

![langSmith.png](doc%2Fimages%2FlangSmith.png)

## Launch the application using LangServe locally

```bash
langchain app serve
```

This command will launch the web server running at http://127.0.0.1:8000. The server enables the following endpoints:
- **/** : Root of the application. It gets automatically redirected to /docs
- **/docs**: Display the auto-generated Open API (Swagger) documentation for the application
- **/{example route name}/playground**: Provides access to the playground testing interface for the different example.
For example, '/simple/playground' will open the playground for the simple OpenAI chain. See the app/server.py for
the list of routes available.

![routes.png](doc%2Fimages%2Froutes.png)

## Run the model evaluation sample script

To run the sample model evaluation script (evaluation/sampleEvaluator.py), please make sure that:
- You have enabled lanSmith as explained above
- You have an OpenRouter API key setup in your terminal window (`export OPENROUTER_API_KEY=<yourOpenRouterkey>`)
- You have an OpenAI API key setup in your terminal window (`export OPENAI_API_KEY=<yourOpenAiAPIkey>`)

Note that if you do not have an OpenRouter API key and want to just use openAI, you can change 
the model definition as follows:

Original:

```python
model = ChatOpenAI(temperature=MODEL_TEMPERATURE,
                   model=MODEL_NAME,
                   openai_api_key=openrouter_api_key,
                   openai_api_base=OPENROUTER_API_BASE,
                   )
```

Modified:

```python
model = ChatOpenAI(temperature=MODEL_TEMPERATURE)
```

To **run the evaluation** script, run the following command:

```shell
python evaluation/sampleEvaluator.py
```

Results from the evaluation will display in the terminal, but are also visible in **LangSmith**

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