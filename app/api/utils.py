from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def get_project_or_404(
    charity_project_id: int,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get_project_by_id(
        charity_project_id, session,
    )
    if not charity_project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден.',
        )
    return charity_project
