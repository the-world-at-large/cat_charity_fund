from http import HTTPStatus

from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_project_name(
    project_name: str,
    session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_id_by_name(
        project_name, session,
    )
    if project_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует.',
        )


async def check_project_exists(
    charity_project_id: int,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get_project_by_id(
        charity_project_id,
        session,
    )
    if not charity_project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден.',
        )
    return charity_project


async def check_project_activeness(
    charity_project: CharityProject,
    session: AsyncSession,
) -> CharityProject:
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя редактировать закрытый проект.'
        )
    return charity_project


async def check_project_investment(
    charity_project: CharityProject,
    session: AsyncSession,
) -> None:
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя удалить проект с уже внесёнными средствами.'
        )


async def check_amount_update(
    obj_in_full_amount: int,
    actual_amount: int,
    session: AsyncSession
) -> None:
    if obj_in_full_amount < actual_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Нельзя установить сумму, меньшую вложенной изначально.',
        )
