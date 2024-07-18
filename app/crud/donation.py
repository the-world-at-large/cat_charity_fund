from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.services.investment import donation_process
from app.models import CharityProject, Donation, User
from app.schemas.donation import DonationCreate


class CRUDDonation(CRUDBase[Donation]):

    async def create_and_process_donation(
        self,
        obj_in: DonationCreate,
        session: AsyncSession,
        user: User,
    ) -> Donation:
        obj_in_data = obj_in.dict()
        obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)

        db_obj = await donation_process(
            db_obj, CharityProject, session,
        )
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_by_user(
        self, user: User, session: AsyncSession
    ) -> list[Donation]:
        donations = await session.execute(select(Donation).where(
            Donation.user_id == user.id,
        ))
        donations = donations.scalars().all()
        return donations


donation_crud = CRUDDonation(Donation)
