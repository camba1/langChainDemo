# LangChainDemo

This repository shows a number of AI powered LangChain application examples. 
The repo was used to present a talk at AICamp. It uses:

- **LangServe** to create and serve the application inference endpoints
- **LangChain Templates** to pull pre-existing application templates
- **LangChain** to interact with the LLM models and build the application logic.
- **LangChain Hub** to pull pre-existing LLM prompts
- **OpenAI GPT 3.5 Turbo**, **GPT 4** as well as **Nous Hermes 2 Mixtral 8x7B MoE** (via [OpenRouter](https://openrouter.ai/docs#quick-start))
- **LangSmith** integration for observability, tracing, metrics and evaluation. See the section on LangSmith for details 
on how to enable sending data to LangSmith

The sister repository [LangChain Demo Client](https://github.com/camba1/langchainDemoClient ) includes simple client examples that can be used to call 
this application using: 
- [Gradio](https://www.gradio.app)
- [Streamlit](https://streamlit.io)
- [Chainlit](https://chainlit.io)
- Simple Python package remote calls.

## Quick start

To get the application going quickly, assuming you already have the LangChain-cli 
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
The application will be launched at http://127.0.0.1:8000 , and you can visit 
[LangSmith](https://smith.langchain.com) to see traces/metrics from running the application


To get the API keys needed, visit:
- OpenAI: https://openai.com
- OpenRouter: https://openrouter.ai
- LangChain: https://www.langchain.com/langsmith

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
  - **myChain**: Simple Chain that interacts OpenAI 
  - **openRouter.py**: Shows how you can use LangChain with OpenRouter, which exposes a number of models using the OpenAI API
  - **rag.py**: Create a simple RAG chain to query the document in the app/data directory
  - **server.py**: Main code to run the FastAPI webServer. Contains all the different application routes. By default, the
routes are public, but simple authentication across all end points can be enabled by uncommenting the appropriate code
section which is clearly marked in the code.
- **brunoapi**: Holds the sample API calls and tests that can be run using [Bruno](https://www.usebruno.com). See detail in the "Run API testing collection"
section for details.
- **copilot**: Manifests to deploy the application to AWS ECS fargate using AWS Copilot
- **doc/images**: Images included in this document
- **Evaluation**: Sample model evaluation script. Script runs a model 5 times and checks the responses for 
relevance and insensitivity
- **Packages**: External packages installed from the [LangChain templates repo](https://templates.langchain.com/). 
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
You can sign up for a free LangSmith account [here](https://smith.langchain.com/). 
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

### Authentication

By the default the sample API endpoints can be run directly in the browser without any authentication which allows us
to quickly start playing with the different endpoints and the playground.
The server.py file contains simple example on how to enable authentication, but it is initially commented out.
To try it out, uncomment the relevant code and then add the following header to the API call: x-token: secret-token.
For example using CURL, hit the /simple/invoke API with the command below:

```shell
  curl --request POST \
    --url http://127.0.0.1:8000/simple/invoke \
    --header 'Accept: application/json' \
    --header 'Content-Type: application/json' \
    --header 'x-token: secret-token' \
    --data '{
    "input": {
      "input": "Aquaman"
    },
    "config": {},
    "kwargs": {}
  }'
```

## Run the model evaluation sample script

Evaluating the answers that the LLMs provide is crucial to ensure that the end user experience is optimal. LangSmith 
can help in this task by providing out of the box evaluation methods and enabling the creation of custom metrics.
The project contains a sample evaluation script that shows how easy it is to set up a set of tests and record them in
LangSmith for review. 

To run the sample model evaluation script (evaluation/sampleEvaluator.py), please make sure that:
- You have enabled langSmith as explained above
- You have an OpenRouter API key setup in your terminal window (`export OPENROUTER_API_KEY=<yourOpenRouterkey>`)
- You have an OpenAI API key setup in your terminal window (`export OPENAI_API_KEY=<yourOpenAiAPIkey>`)

Note that if you do not have an OpenRouter API key and want to just use OpenAI instead, you can change 
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

Results from the evaluation will display in the terminal, but are also visible in **LangSmith**.
Note that everytime you re-run the evaluation script, you need to change the `run_on_dataset` object to have a different
`project_name`, otherwise LangSmith will throw an error.

## Run the API testing collection

Just like any other project, we should test not only the LLM replies, but also the application endpoints themselves.
The project includes a simple Bruno API collection that case be used to test that the different APIs are up and running.
To run the tests collection, assuming you have Bruno installed (installation instructions can be found [here](https://www.usebruno.com/downloads)):
- Using the Bruno UI: 
  - Open the brunoapi folder in Bruno which will automatically load the LangChainAPIDemo collection
  - Click on the ellipsis (...) menu next to collection name
  - Click Run
- Using the [Bruno CLI](npm install -g @usebruno/cli):
  - Change directory to brunoapi and run ``` bru run ```

**Note**: As of this writing, Bruno CLI has a dependency on vm2 which has been deprecated. Hopefully this will be addressed in
the near future, but keep that in mind.

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

To run the image, run the command below. Be sure to have the openAi and OpenRouter API keys set in your terminal.
The application will be exposed in port **8080**.

```shell
docker run --rm -e OPENAI_API_KEY=$OPENAI_API_KEY -e OPENROUTER_API_KEY=$OPENROUTER_API_KEY -p 8080:8080 my-langserve-app
```

## Deploying to AWS with AWS Copilot

#### Initializing the application

**Note**: Before deploying the sample app, it may be a good idea to at the very least enable the simple authentication
code in server.py. This will stop unauthorized users from (easily) running the different examples since they would be 
hitting OpenAI & OpenRouter and thus incurring costs. See the authentication section in this document for details.

install copilot if not already installed

```bash
brew install aws/tap/copilot-cli
```

Initialize copilot app and define tags. Then, create the dev environment where we will deploy the app.:

```bash
copilot app init langchain-demo --resource-tags app=langchain-demo
copilot env init --name dev --profile default --default-config
copilot env deploy --name dev
```

Generate the secrets to store the OpenAI and OpenRouter key in AWS. This is necessary so that the image can use them

```bash
copilot secret init --name openai --values dev=<yourOpenAiAPIKEY>
copilot secret init --name openrouter --values dev=<yourOpenRouterAPIKEY>
```

Initialize the application. When asked if you would like to deploy an environment, say no as we will need to update
the generated manifest:

```bash
copilot init --app langchain-demo --name langchain-demo-svc --type 'Load Balanced Web Service' --dockerfile './Dockerfile'
```

#### Updating the copilot manifest

Update the copilot manifest for the service to include the secrets for our OpenAI and OpenRouter API keys .
This file was automatically created by copilot and is located at ```copilot/langchain-demo-svc```. Add the 
following to the file:

```yaml
secrets:                      # Pass secrets from AWS Systems Manager (SSM) Parameter Store.
  OPENAI_API_KEY: /copilot/${COPILOT_APPLICATION_NAME}/${COPILOT_ENVIRONMENT_NAME}/secrets/openai
  OPENROUTER_API_KEY: /copilot/${COPILOT_APPLICATION_NAME}/${COPILOT_ENVIRONMENT_NAME}/secrets/openrouter
```

Update the amount of memory and cpu used by container. The default 512 MiB is not enough to run the container as it 
throws an out of memory error in ECS Fargate.

```yaml
cpu: 512       # Number of CPU units for the task.
memory: 1024    # Amount of memory in MiB used by the task.
```

Additionally, by default copilot will build your image as an X64 image. If you would like to build an ARM image, 
update the following line in the manifest:

```yaml
platform: linux/x86_64  # See https://aws.github.io/copilot-cli/docs/manifest/lb-web-service/#platform
```

to be instead:

```yaml
platform: linux/arm64  # See https://aws.github.io/copilot-cli/docs/manifest/lb-web-service/#platform
```

Finally, update the `http` section of the document to health check against the /docs instead of / if you have enabled
authentication as / will return an unauthorized error. Add the following line un `http`:

```yaml
  healthcheck: '/docs'
```

Deploy the application

```bash
copilot deploy --env dev
```

#### Deleting and trouble shooting the deployment

To remove the application from AWS, run the following command:

```bash
copilot app delete --yes
```

To remove the secret we created, since copilot will not delete them:

```bash
aws ssm delete-parameters --names "/copilot/langchain-demo/dev/secrets/openai" "/copilot/langchain-demo/dev/secrets/openrouter" 
```

To troubleshoot the deployment in case something goes wrong, check the logs using:

```bash
copilot svc logs -n langchain-demo-svc -e dev
```


## Useful Resources

- LangSmith Docs: https://docs.smith.langchain.com/tracing
- LangServe Application templates: https://templates.langchain.com
- LangChain Hub: https://smith.langchain.com/hub
- LangChain Python documentation: https://python.langchain.com/
- LangChain JS documentation: https://js.langchain.com
- LangChain Blog: https://blog.langchain.dev/
- LangChain Discord: https://discord.gg/cU2adEyC7w
- AWS Copilot documentation: https://aws.github.io/copilot-cli/docs/overview/ 
- Repo for this demo: 
  - Backend: https://github.com/camba1/langChainDemo
  - Frontend: https://github.com/camba1/langchainDemoClient 