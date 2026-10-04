from pydantic import BaseModel, EmailStr


class Customer(BaseModel):
    customer_id: str
    full_name: str
    email: EmailStr
    policy_number: str
    phone: str | None = None