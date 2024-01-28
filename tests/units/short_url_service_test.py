import pytest

from src.domain.exceptions import UrlNotFoundException
from src.repositories.unit_of_work import UnitOfWorkAbstract
from src.services.url_shortener_service import UrlShortenerService


class FakeUnitOfWork(UnitOfWorkAbstract):
    def __init__(self):
        self.url_mapping = {}

    def commit(self):
        pass

    def rollback(self):
        pass

    def save_url_mapping(self, short_code, original_url):
        self.url_mapping[short_code] = original_url

    def get_original_url(self, short_code) -> str | None:
        return self.url_mapping.get(short_code)

    def delete_by_short_code(self, short_code: str) -> None:
        del self.url_mapping[short_code]


@pytest.fixture
def url_shortener_service():
    return UrlShortenerService(FakeUnitOfWork())


@pytest.mark.asyncio
async def test_url_shortener_service_generates_short_code(url_shortener_service):
    original_url = "https://example.com/somepath/a?user_id=22312"

    short_code = url_shortener_service.shorten_url(original_url)

    assert short_code is not None


@pytest.mark.asyncio
async def test_url_shortener_service_saves_to_database(url_shortener_service):
    original_url = "https://example.com/somepath/a?user_id=22312"
    short_code = url_shortener_service.shorten_url(original_url)

    saved_url = url_shortener_service.get_original_url(short_code)

    assert saved_url == original_url


@pytest.mark.asyncio
async def test_url_shortener_service_generate_2_codes_return_correct_url_by_code(url_shortener_service):
    original_url_1 = "https://example.com/somepath_1/a?user_id=22312"
    original_url_2 = "https://example.com/somepath_2/a?user_id=22312"
    short_code_1 = url_shortener_service.shorten_url(original_url_1)
    short_code_2 = url_shortener_service.shorten_url(original_url_2)

    saved_url_1 = url_shortener_service.get_original_url(short_code_1)
    saved_url_2 = url_shortener_service.get_original_url(short_code_2)

    assert saved_url_1 == original_url_1
    assert saved_url_2 == original_url_2


@pytest.mark.asyncio
async def test_url_shortener_service_deleted_entry_is_not_existed(url_shortener_service):
    original_url = "https://example.com/somepath/a?user_id=22312"
    short_code = url_shortener_service.shorten_url(original_url)

    url_shortener_service.delete_by_short_code(short_code)

    with pytest.raises(Exception):
        url_shortener_service.get_original_url(short_code)


@pytest.mark.asyncio
async def test_url_shortener_service_get_nonexistent_short_code_raises_exception(url_shortener_service):
    with pytest.raises(UrlNotFoundException):
        url_shortener_service.get_original_url("fake")
