# shortly
Minimal url shortener service

## Installation
### Using Docker
To run the service in a Docker container, use the following command:
`docker-compose up --build -d`.
The database is stored in a Docker volume, so it will be deleted when the Docker container is removed.
### Local
Run the following commands in the directory with pyproject.toml:
`poetry install && poetry run uvicorn src.main:app --host 0.0.0.0 --port 5000 --reload`