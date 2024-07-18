from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.utils import get_project_or_404
from app.crud.charity_project import charity_project_crud
from app.models import CharityProject, Donation
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate,
)
from app.services.investment import donation_process


class CharityProjectService:

    async def check_project_name(
        self,
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

    def check_project_activeness(
        self,
        charity_project: CharityProject,
    ) -> None:
        if charity_project.fully_invested:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Нельзя редактировать закрытый проект.',
            )

    def check_project_investment(
        self,
        charity_project: CharityProject,
    ) -> None:
        if charity_project.invested_amount:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Нельзя удалить проект с уже внесёнными средствами.',
            )

    def check_amount_update(
        self,
        obj_in_full_amount: int,
        actual_amount: int,
    ) -> None:
        if obj_in_full_amount < actual_amount:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail='Нельзя установить сумму, меньшую вложенной.',
            )

    async def create_project(
        self,
        project: CharityProjectCreate,
        session: AsyncSession,
    ) -> CharityProject:
        await self.check_project_name(
            project.name, session,
        )
        new_project = await charity_project_crud.create_project(
            project, session,
        )
        new_project = await donation_process(
            new_project, Donation, session,
        )
        await session.commit()
        await session.refresh(new_project)
        return new_project

    async def update_project(
        self,
        project: CharityProject,
        obj_in: CharityProjectUpdate,
        session: AsyncSession,
    ) -> CharityProject:
        project = await get_project_or_404(
            project.id, session,
        )
        self.check_project_activeness(project)
        if obj_in.name:
            await self.check_project_name(
                obj_in.name, session,
            )
        if not obj_in.full_amount:
            project = await charity_project_crud.update_project(
                project, obj_in, session,
            )
            await session.commit()
            await session.refresh(project)
            return project
        self.check_amount_update(
            obj_in.full_amount, project.invested_amount,
        )
        charity_project = await charity_project_crud.update_project(
            project, obj_in, session,
        )
        charity_project = await donation_process(
            project, Donation, session,
        )
        await session.commit()
        await session.refresh(charity_project)
        return charity_project

    async def remove_project(
        self,
        project: CharityProject,
        session: AsyncSession,
    ) -> CharityProject:
        project = await get_project_or_404(
            project.id, session,
        )
        self.check_project_investment(project)
        project = await charity_project_crud.remove_project(
            project, session,
        )
        await session.commit()
        return project

    async def get_all_projects(
        self,
        session: AsyncSession
    ) -> list[CharityProject]:
        projects = await charity_project_crud.get_multi(session)
        return projects
