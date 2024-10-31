from pydantic import BaseModel, EmailStr

class SUserRigister(BaseModel):
    email: EmailStr
    password: str