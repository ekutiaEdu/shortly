import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from src.domain.exceptions import UrlNotFoundException, ShortCodeAlreadyExists
from src.infrastructure.database import session_maker
from src.repositories.sqlalchemy.url_repository_sqlalchemy import UrlRepository
from src.repositories.unit_of_work import UnitOfWorkAbstract


def create_uow() -> UnitOfWorkAbstract:
    return UnitOfWorkSqlAlchemy(session_maker=session_maker)


class UnitOfWorkSqlAlchemy(UnitOfWorkAbstract):
    sessionmaker: sessionmaker

    def __init__(self, session_maker: sessionmaker):
        self.sessionmaker = session_maker

    def __enter__(self):
        self.session = self.sessionmaker()
        self.url_repo = UrlRepository(session=self.session)
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)
        self.session.close()

    def commit(self):
        try:
            self.session.commit()
        except IntegrityError as e:
            if not str(e).startswith("CHECK constraint failed: LENGTH"):
                raise ShortCodeAlreadyExists() from e
        except Exception as e:
            logging.error(e)
            self.rollback()
            raise Exception from e

    def rollback(self):
        self.session.rollback()

    def save_url_mapping(self, short_code: str, original_url: str) -> None:
        self.url_repo.add_url(short_code=short_code, url=original_url)

    def get_original_url(self, short_code: str) -> str:
        url = self.url_repo.get_url(short_code=short_code)
        if not url:
            raise UrlNotFoundException(short_code=short_code)
        return url

    def delete_by_short_code(self, short_code: str) -> None:
        url = self.url_repo.get_url(short_code=short_code)
        if url:
            self.url_repo.delete_url(short_code=short_code)
        else:
            raise UrlNotFoundException(short_code=short_code)
