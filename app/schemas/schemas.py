from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PageMeta(BaseModel):
    total: int
    page: int
    size: int
    pages: int


class PlaceImport(BaseModel):
    external_id: int = Field(..., description="Art Institute artwork ID")


class PlaceCreate(BaseModel):
    external_id: int = Field(..., description="Art Institute artwork ID")
    notes: Optional[str] = Field(None, max_length=5000)


class PlaceUpdate(BaseModel):
    notes: Optional[str] = Field(None, max_length=5000)
    is_visited: Optional[bool] = None


class PlaceOut(BaseModel):
    id: int
    project_id: int
    external_id: int
    title: str
    artist: Optional[str]
    image_url: Optional[str]
    notes: Optional[str]
    is_visited: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PlaceListResponse(PageMeta):
    items: List[PlaceOut]


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    start_date: Optional[date] = None
    places: Optional[List[PlaceImport]] = Field(
        default=None,
        description="Optional places to add at creation (max 10)",
    )

    @field_validator("places")
    @classmethod
    def validate_places(cls, v):
        if v is None:
            return v
        if len(v) > 10:
            raise ValueError("Cannot add more than 10 places to a project")
        ids = [p.external_id for p in v]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate place IDs in the request")
        return v


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    start_date: Optional[date] = None


class ProjectOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    start_date: Optional[date]
    is_completed: bool
    owner_id: int
    places_count: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProjectDetail(ProjectOut):
    places: List[PlaceOut]


class ProjectPage(PageMeta):
    items: List[ProjectOut]
