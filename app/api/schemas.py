from typing import Optional

from pydantic import BaseModel


class ClaimRequest(BaseModel):
    claim_description: str
    image_path: Optional[str] = None