"""Main factory builder of ``FastAPI`` server."""

from fastapi import FastAPI

from app.configuration import __containers__
from app.configuration.server import Server


def create_app() -> FastAPI:
    """Create ``FastAPI`` application.

    :func:`.create_app` is a global point of your application.
    In :func:`.create_app` you can add all your middlewares, routes, dependencies, etc.
    required for global server startup.
    """
    app = FastAPI()
    __containers__.wire_packages(app=app)
    return Server(app).get_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:create_app", host="localhost", port=5001, reload=True)
