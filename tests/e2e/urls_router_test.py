import pytest
from fastapi.exceptions import RequestValidationError
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.models.urls import Base
from src.repositories.sqlalchemy.unit_of_work_sqlalchemy import (
    create_uow,
    UnitOfWorkSqlAlchemy,
)
from src.routers.urls_router import urls_router


@pytest.fixture()
def engine():
    engine = create_engine(f"sqlite:///test.db")
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture
def client(engine):
    session_maker = sessionmaker(bind=engine)

    def override_crete_uow():
        return UnitOfWorkSqlAlchemy(session_maker=session_maker)

    app.dependency_overrides[create_uow] = override_crete_uow
    test_client = TestClient(app=app)
    return test_client


def test_create_short_url_success(client):
    url_to_shorten = "https://example.com/somepath/a?user_id=22312"

    response = client.put("/api/url", json={"url": url_to_shorten})

    assert response.status_code == 201
    assert "short_code" in response.json()
    assert "url" in response.json()
    assert (
        response.json()["url"] == f"http://testserver/{response.json()['short_code']}"
    )


def test_create_short_url_failure():
    client = TestClient(urls_router)
    url_to_shorten = "invalid_url"

    with pytest.raises(RequestValidationError):
        client.put("/api/url", json={"url": url_to_shorten})


def test_delete_short_url_success(client):
    response_create = client.put("/api/url", json={"url": "https://example.com/test"})
    assert response_create.status_code == 201
    short_code = response_create.json()["short_code"]

    response_delete = client.request(
        "DELETE", "/api/url/", json={"short_code": response_create.json()["short_code"]}
    )

    assert response_delete.status_code == 200


def test_delete_short_url_not_found(client):
    response_delete = client.request(
        "DELETE", "/api/url", json={"short_code": "nonexistent_code"}
    )
    assert response_delete.status_code == 404


def test_delete_short_url_internal_server_error(client, monkeypatch):
    def mock_delete_by_short_code(*args, **kwargs):
        raise Exception("Test exception")

    monkeypatch.setattr(
        "src.services.url_shortener_service.UrlShortenerService.delete_by_short_code",
        mock_delete_by_short_code,
    )

    # Попытка удаления с вызовом исключения в сервисе
    response_delete = client.request(
        "DELETE", "/api/url", json={"short_code": "some_code"}
    )
    assert response_delete.status_code == 500
    assert "detail" in response_delete.json()
    assert "Test exception" in response_delete.json()["detail"]


def test_redirect_to_original_url_success(client):
    response_create = client.put("/api/url", json={"url": "https://example.com/test"})
    assert response_create.status_code == 201
    short_code = response_create.json()["short_code"]

    response_redirect = client.get(f"/{short_code}", allow_redirects=False)

    assert response_redirect.status_code == 307
    assert response_redirect.headers["location"] == "https://example.com/test"


def test_redirect_to_original_url_not_found(client):
    response_redirect = client.get("/nonexistent_code")
    assert response_redirect.status_code == 404


def test_redirect_to_original_url_internal_server_error(client, monkeypatch):
    def mock_get_original_url(*args, **kwargs):
        raise Exception("Test exception")

    monkeypatch.setattr(
        "src.services.url_shortener_service.UrlShortenerService.get_original_url",
        mock_get_original_url,
    )

    response_redirect = client.get("/some_code")
    assert response_redirect.status_code == 500
    assert "detail" in response_redirect.json()
    assert "Test exception" in response_redirect.json()["detail"]
