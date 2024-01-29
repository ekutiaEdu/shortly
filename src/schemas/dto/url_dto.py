from pydantic import Field, HttpUrl, BaseModel


class AddUrlDto(BaseModel):
    url: HttpUrl


class DeleteUrlDto(BaseModel):
    short_code: str = Field()
