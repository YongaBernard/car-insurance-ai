from pydantic import BaseModel, Field


class Claim(BaseModel):
    claim_id: str
    customer_id: str
    policy_number: str
    accident_date: str
    accident_location: str
    description: str
    estimated_damage: float = Field(ge=0)
    image_paths: list[str] = []