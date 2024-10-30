# models.py

from pydantic import BaseModel, EmailStr, Field

class UserData(BaseModel):
    name: str = Field(..., description="使用者的姓名")
    email: EmailStr = Field(..., description="使用者的電子郵件")
    phone: str = Field(..., description="使用者的電話號碼")
