from typing import List

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_project_activeness,
    check_project_exists,
    check_project_investment,
    check_amount_update,
    check_project_name,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models import Donation
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investment import donation_process


router = APIRouter()


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
    await check_project_name(project.name, session)
    new_project = await charity_project_crud.create_project(project, session)
    new_project = await donation_process(new_project, Donation, session)
    await session.commit()
    await session.refresh(new_project)
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
    project = await check_project_exists(project_id, session)
    project = await check_project_activeness(project, session)
    if obj_in.name:
        await check_project_name(obj_in.name, session)
    if not obj_in.full_amount:
        project = await charity_project_crud.update_project(
            project, obj_in, session,
        )
        return project
    await check_amount_update(
        obj_in.full_amount, project.invested_amount, session,
    )
    charity_project = await charity_project_crud.update_project(project,
                                                                obj_in,
                                                                session)
    charity_project = await donation_process(project, Donation, session)
    return charity_project


@router.get(
    '/',
    response_model_exclude_none=True,
    response_model=List[CharityProjectDB]
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """Возвращает список всех проектов."""
    projects = await charity_project_crud.get_multi(session)
    return projects


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперъюзеров.

    Удаляет проект без внесённых в него средств.
    Нельзя удалить проект с уже внесёнными в него средствами,
    можно только закрыть.
    """
    project = await check_project_exists(project_id, session)
    await check_project_investment(project, session)
    project = await charity_project_crud.remove_project(project, session)
    return project
