import uvicorn
from fastapi import FastAPI

from api import setup_app
from core import settings

app = FastAPI()


def main() -> None:
    setup_app(app)
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)


if __name__ == "__main__":
    main()
