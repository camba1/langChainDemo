from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from .myChain import chain as simple_chain
from .openRouter import chain as openrouter_chain
from .rag import build_chain
from .agent import build_agent
from .multiChain import chain_with_fallback, routable_chain
from pirate_speak.chain import chain as pirateChain

# -------- Simple Auth ------------
# Uncomment this section to enable simple auth using the contents of a 'x-token' header
# Because we apply the security att he FastApi creation level, this applies to all paths
# created with add_routes. Alternatively this could ba added at api path level instead.

# from typing_extensions import Annotated
# from fastapi import Depends, Header, HTTPException

# async def verify_token(x_token: Annotated[str, Header()]) -> None:
#     """Verify the token is valid."""
#     # Replace this with your actual authentication logic
#     print(x_token)
#     if x_token != "secret-token":
#         raise HTTPException(status_code=400, detail="X-Token header invalid")
#
# app = FastAPI(dependencies=[Depends(verify_token)])

# --------End Simple Auth ------------

# -------- No Auth --------------------
# Comment this line if using the auth code above
app = FastAPI()
# -------- End No Auth ----------------


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

# Edit this to add the chain you want to add
add_routes(app, simple_chain, path="/simple")
add_routes(app, openrouter_chain, path="/openrouter")
add_routes(app, build_chain(), path="/rag")
add_routes(app, build_agent(), path="/agent")
add_routes(app, chain_with_fallback(), path="/multichain")
add_routes(app, routable_chain(), path="/route")


# Showing the endpoint and feedback require setting up LangSmith access
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
