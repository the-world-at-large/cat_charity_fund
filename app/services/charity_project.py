from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject, Donation
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate,
)
from app.services.investment import donation_process


class CharityProjectService:

    @staticmethod
    async def check_project_name(
        project_name: str,
        session: AsyncSession
    ) -> None:
        project_id = await charity_project_crud.get_id_by_name(
            project_name, session,
        )
        if project_id:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Проект с таким именем уже существует.',
            )

    @staticmethod
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

    @staticmethod
    async def check_project_activeness(
        charity_project: CharityProject,
        session: AsyncSession,
    ) -> CharityProject:
        if charity_project.fully_invested:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Нельзя редактировать закрытый проект.',
            )
        return charity_project

    @staticmethod
    async def check_project_investment(
        charity_project: CharityProject,
        session: AsyncSession,
    ) -> None:
        if charity_project.invested_amount:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Нельзя удалить проект с уже внесёнными средствами.',
            )

    @staticmethod
    async def check_amount_update(
        obj_in_full_amount: int,
        actual_amount: int,
        session: AsyncSession,
    ) -> None:
        if obj_in_full_amount < actual_amount:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail='Нельзя установить сумму, меньшую вложенной.',
            )

    @staticmethod
    async def create_project(
        project: CharityProjectCreate,
        session: AsyncSession,
    ) -> CharityProject:
        await CharityProjectService.check_project_name(
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

    @staticmethod
    async def update_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession,
    ) -> CharityProject:
        project = await CharityProjectService.get_project_or_404(
            project_id, session
        )
        project = await CharityProjectService.check_project_activeness(
            project, session,
        )
        if obj_in.name:
            await CharityProjectService.check_project_name(
                obj_in.name, session,
            )
        if not obj_in.full_amount:
            project = await charity_project_crud.update_project(
                project, obj_in, session,
            )
            await session.commit()
            await session.refresh(project)
            return project
        await CharityProjectService.check_amount_update(
            obj_in.full_amount, project.invested_amount, session,
        )
        charity_project = await charity_project_crud.update_project(
            project, obj_in, session,
        )
        charity_project = await donation_process(project, Donation, session)
        await session.commit()
        await session.refresh(charity_project)
        return charity_project

    @staticmethod
    async def remove_project(
        project_id: int,
        session: AsyncSession,
    ) -> CharityProject:
        project = await CharityProjectService.get_project_or_404(
            project_id, session,
        )
        await CharityProjectService.check_project_investment(
            project, session,
        )
        project = await charity_project_crud.remove_project(
            project, session,
        )
        await session.commit()
        return project

    @staticmethod
    async def get_all_projects(
        session: AsyncSession
    ) -> list[CharityProject]:
        projects = await charity_project_crud.get_multi(session)
        return projects
