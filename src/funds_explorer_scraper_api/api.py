import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .scraper import fetch_fii_data
from .settings import SERVER_HOST, SERVER_PORT
import importlib.metadata

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/version/")
async def version_route():
    return {"version": importlib.metadata.version("funds_explorer_scraper")}


@app.get("/api/fii/{code}/")
async def fii_route(code: str):
    try:
        return {"fii": await fetch_fii_data(code)}
    except Exception as error:
        return JSONResponse({"error": str(error)}, 404)


def make_api_server():
    config = uvicorn.Config(
        app,
        host=SERVER_HOST,
        port=SERVER_PORT,
    )
    return uvicorn.Server(config).serve()
