FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install poetry
RUN poetry install

CMD ["poetry", "run", "python", "src/main.py"]

EXPOSE 8001
