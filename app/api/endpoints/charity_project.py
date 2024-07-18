from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.utils import get_project_or_404
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.charity_project import CharityProjectService

router = APIRouter()

charity_project_service = CharityProjectService()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    new_project = await charity_project_service.create_project(
        project, session,
    )
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    project = await get_project_or_404(
        project_id, session,
    )
    updated_project = await charity_project_service.update_project(
        project, obj_in, session,
    )
    return updated_project


@router.get(
    '/',
    response_model_exclude_none=True,
    response_model=list[CharityProjectDB]
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    projects = await charity_project_service.get_all_projects(session)
    return projects


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    project = await get_project_or_404(
        project_id, session,
    )
    removed_project = await charity_project_service.remove_project(
        project, session,
    )
    return removed_project
