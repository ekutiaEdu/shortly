FROM python:3.11

RUN apt-get update && apt-get install -y
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV POETRY_VERSION=1.6.1
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app
COPY . /app

EXPOSE 5000
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi
CMD ["sh", "-c" , "poetry run uvicorn src.main:app --host 0.0.0.0 --port 5000 --reload"]