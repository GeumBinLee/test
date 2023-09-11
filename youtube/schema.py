from datetime import date

from pydantic import BaseModel, Field, condecimal, validator


class Youtube(BaseModel):
    search: str = Field(
        max_length=100,
        description="검색어",
        examples="challenge",
    )
