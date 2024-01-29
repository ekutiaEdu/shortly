import logging

from fastapi import APIRouter, Depends, Request, HTTPException
from starlette import status
from starlette.responses import RedirectResponse

from src.domain.exceptions import UrlNotFoundException
from src.repositories.sqlalchemy.unit_of_work_sqlalchemy import create_uow
from src.repositories.unit_of_work import UnitOfWorkAbstract
from src.schemas.dto.url_dto import AddUrlDto, DeleteUrlDto
from src.services.url_shortener_service import UrlShortenerService

urls_router = APIRouter()


@urls_router.put("/api/url", status_code=status.HTTP_201_CREATED)
def create_short_url(
    body: AddUrlDto, request: Request, uow: UnitOfWorkAbstract = Depends(create_uow)
):
    try:
        service = UrlShortenerService(uow=uow)
        short_code = service.shorten_url(str(body.url))
        url = f"{str(request.base_url)}{short_code}"
        return {"short_code": short_code, "url": url}
    except Exception as e:
        logging.ERROR
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error message: {str(e)}",
        )


@urls_router.delete("/api/url", status_code=status.HTTP_200_OK)
def delete_short_url(body: DeleteUrlDto, uow: UnitOfWorkAbstract = Depends(create_uow)):
    try:
        service = UrlShortenerService(uow=uow)
        service.delete_by_short_code(short_code=body.short_code)
    except UrlNotFoundException as e:
        logging.info(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error message: {str(e)}",
        )


@urls_router.get("/{short_code}")
def redirect_to_original_url(
    short_code: str, uow: UnitOfWorkAbstract = Depends(create_uow)
):
    try:
        service = UrlShortenerService(uow=uow)
        original_url = service.get_original_url(short_code=short_code)
        return RedirectResponse(
            url=original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT
        )
    except UrlNotFoundException as e:
        logging.info(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error message: {str(e)}",
        )
