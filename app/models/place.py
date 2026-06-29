from typing import Optional
from sqlalchemy import ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Place(Base):
    __tablename__ = "places"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    external_id: Mapped[str] = mapped_column(String(225), index=True)
    title: Mapped[str] = mapped_column(String(255))
    artist: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_visited: Mapped[bool] = mapped_column(default=False)

    project: Mapped["Project"] = relationship(back_populates="places")
