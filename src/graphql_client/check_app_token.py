from typing import Optional

from .base_model import BaseModel


class CheckAppToken(BaseModel):
    app: Optional["CheckAppTokenApp"]


class CheckAppTokenApp(BaseModel):
    id: str


CheckAppToken.model_rebuild()
