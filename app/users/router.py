from fastapi import APIRouter, HTTPException, status, Response, Depends
from users.schemas import SUserRigister
from users.dao import UserDAO
from users.auth import get_password_hash, authenticate_user, create_access_token
from users.dependencies import get_current_user
from users.models import Users
from exception import UserAlreadyExistsException, IncorrectEmail0rPasswordException

router = APIRouter(
    prefix="/auth",
    tags=["Аутентификация"]
)

@router.post("/register")
async def register_user(user_data: SUserRigister):
    existing_user = await UserDAO.find_by_fil(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UserDAO.add(email=user_data.email, hashed_password=hashed_password)

@router.post("/login")
async def register_user(response: Response, user_data: SUserRigister):
    existing_user = await authenticate_user(user_data.email, user_data.password)
    if not existing_user:
        raise IncorrectEmail0rPasswordException

    access_token = create_access_token({"sub": str(existing_user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token

@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")


@router.get("/me")
async def read_users_me(user: Users = Depends(get_current_user)):
    return user