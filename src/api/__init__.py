from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import recommend


def setup_app(app: FastAPI) -> None:
    """
    Setup FastAPI app.

    Args:
        app (FastAPI): FastAPI app
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(recommend.router)


__all__ = ["setup_app"]
