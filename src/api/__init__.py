from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


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


__all__ = ["setup_app"]
