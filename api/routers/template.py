from uuid import UUID

from fastapi import APIRouter, Depends
from core.repository.interfaces import TemplateRepositoryInterface
from core.service import TemplateService

template_router = APIRouter()


@template_router.get("/templates")
def get_templates(
    template_service: TemplateService = Depends(TemplateService)
) -> list[UUID]:
    return template_service.template_list()
