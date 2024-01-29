import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.domain.exceptions import UrlNotFoundException, ShortCodeAlreadyExists
from src.models.urls import Base
from src.repositories.sqlalchemy.unit_of_work_sqlalchemy import UnitOfWorkSqlAlchemy


@pytest.fixture
def temp_database():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def unit_of_work(temp_database):
    engine = temp_database
    session_maker = sessionmaker(bind=engine)
    return UnitOfWorkSqlAlchemy(session_maker=session_maker)


def test_add_and_delete_url(unit_of_work):
    short_code = "test_short_code"
    original_url = "https://example.com/test"

    with unit_of_work:
        unit_of_work.save_url_mapping(short_code, original_url)

    with unit_of_work:
        assert unit_of_work.url_repo.is_exist(short_code)

    with unit_of_work:
        unit_of_work.delete_by_short_code(short_code)

    with unit_of_work:
        assert not unit_of_work.url_repo.is_exist(short_code)


def test_rollback_transaction(unit_of_work):
    short_code = "test_short_code"
    original_url = "https://example.com/test"

    with unit_of_work as session:
        unit_of_work.save_url_mapping(short_code, original_url)
        session.rollback()

    with unit_of_work:
        assert not unit_of_work.url_repo.is_exist(short_code)


def test_get_original_url(unit_of_work):
    short_code = "test_short_code"
    original_url = "https://example.com/test"

    with unit_of_work:
        unit_of_work.save_url_mapping(short_code, original_url)

    with unit_of_work:
        retrieved_url = unit_of_work.get_original_url(short_code)
        assert retrieved_url == original_url


def test_get_original_url_nonexistent(unit_of_work):
    short_code = "nonexistent_short_code"

    with pytest.raises(UrlNotFoundException):
        with unit_of_work:
            unit_of_work.get_original_url(short_code)


def test_double_add_url_raise_exception(unit_of_work):
    short_code = "test_short_code"
    original_url = "https://example.com/test"

    with pytest.raises(ShortCodeAlreadyExists):
        with unit_of_work:
            unit_of_work.save_url_mapping(short_code, original_url)
            unit_of_work.save_url_mapping(short_code, original_url)
