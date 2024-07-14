from uuid import UUID

from fastapi import APIRouter, Depends

from app.core.service import TemplateService

template_router = APIRouter()


@template_router.get("/templates")
def get_templates(template_service: TemplateService = Depends(TemplateService)) -> list[UUID]:
    try:
        template_list = template_service.template_list()
    except RecursionError as err:
        raise err

    return template_list
