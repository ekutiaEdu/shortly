from abc import ABC, abstractmethod


class UrlRepositoryAbstract(ABC):
    @abstractmethod
    def is_exist(self, short_code: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_url(self, short_code: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def add_url(self, short_code: str, url: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_url(self, short_code: str) -> None:
        raise NotImplementedError
