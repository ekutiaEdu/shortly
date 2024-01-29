from datetime import datetime

from sqlalchemy import func, Index, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class UrlDb(Base):
    __tablename__ = "urls"
    __table_args__ = (
        UniqueConstraint("code"),
        CheckConstraint("LENGTH(code) >= 1"),
        CheckConstraint("LENGTH(url) >= 10"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column()
    code: Mapped[str] = mapped_column(index=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


url_code_index = Index("url_code_index", UrlDb.code, unique=True)
