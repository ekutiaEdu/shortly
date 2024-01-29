from sqlalchemy.orm import Session

from src.models.urls import UrlDb
from src.repositories.url_repository import UrlRepositoryAbstract


class UrlRepository(UrlRepositoryAbstract):
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def is_exist(self, short_code: str) -> bool:
        return self.session.query(UrlDb).filter_by(code=short_code).count() > 0

    def get_url(self, short_code: str) -> str | None:
        url_db = self.session.query(UrlDb).filter_by(code=short_code).first()
        return url_db.url if url_db else None

    def add_url(self, short_code: str, url: str) -> None:
        new_url = UrlDb(code=short_code, url=url)
        self.session.add(new_url, _warn=True)

    def delete_url(self, short_code: str) -> None:
        url_db = self.session.query(UrlDb).filter_by(code=short_code).first()
        if url_db:
            self.session.delete(url_db)
