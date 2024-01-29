import src.domain.short_code_generator as generator
from src.domain.exceptions import UrlNotFoundException
from src.repositories.unit_of_work import UnitOfWorkAbstract


class UrlShortenerService:

    def __init__(self, uow: UnitOfWorkAbstract):
        self.uow = uow

    def shorten_url(self, original_url: str) -> str:
        with self.uow:
            short_code = generator.generate()
            self.uow.save_url_mapping(short_code=short_code, original_url=original_url)
            return short_code

    def get_original_url(self, short_code: str) -> str:
        with self.uow:
            url = self.uow.get_original_url(short_code=short_code)
            if not url:
                raise UrlNotFoundException(short_code)
            return url

    def delete_by_short_code(self, short_code: str) -> None:
        with self.uow:
            self.uow.delete_by_short_code(short_code)
