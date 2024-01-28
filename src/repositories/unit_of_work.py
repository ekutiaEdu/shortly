from abc import ABC, abstractmethod


class UnitOfWorkAbstract(ABC):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError

    @abstractmethod
    def save_url_mapping(self, short_code: str, original_url: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_original_url(self, short_code: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def delete_by_short_code(self, short_code: str) -> None:
        raise NotImplementedError
