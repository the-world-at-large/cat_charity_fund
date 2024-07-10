from fastapi import APIRouter, HTTPException

from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)
user_routers = fastapi_users.get_users_router(UserRead, UserUpdate)

for route in user_routers.routes:
    if 'DELETE' in route.methods:
        user_routers.routes.remove(route)
        break
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['users'],
)


@router.delete(
    '/users/{id}',
    tags=['users'],
    deprecated=True,
)
def delete_user(id: str):
    raise HTTPException(
        status_code=405,
        detail='Невозможно удалить пользователя.',
    )
