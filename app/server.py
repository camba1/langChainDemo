from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from pirate_speak.chain import chain as pirateChain
from .myChain import chain as simple_chain
from .rag import build_chain
from .agent import build_agent
from .multiChain import chain_with_fallback, routable_chain

app = FastAPI()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


# Edit this to add the chain you want to add
add_routes(app, simple_chain, path="/simple")
add_routes(app, build_chain(), path="/rag")
add_routes(app, build_agent(), path="/agent")
add_routes(app, chain_with_fallback(), path="/multichain")
add_routes(app, routable_chain(), path="/route")

# Showing the endpoint and feedback require setting up langsmith access
add_routes(app,
           pirateChain,
           path="/pirate",
           enable_feedback_endpoint=True,
           enable_public_trace_link_endpoint=True,
           # enabled_endpoints=["invoke"],
           playground_type="chat"
           )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
