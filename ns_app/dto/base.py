from pydantic import BaseModel, ConfigDict


class BaseDTO(BaseModel):
    """Base DTO for all other DTOs."""

    model_config = ConfigDict(from_attributes=True)
