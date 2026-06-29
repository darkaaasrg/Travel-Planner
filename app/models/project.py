from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    func,
)  # Додали ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    start_date = Column(DateTime, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="projects")
    places = relationship(
        "Place", back_populates="project", cascade="all, delete-orphan"
    )

    @property
    def places_count(self) -> int:
        # Ми перевіряємо, чи списокplaces вже завантажений в пам'ять (не None і не порожній lazy)
        # Якщо SQLAlchemy не завантажила це автоматично — просто повертаємо 0
        if hasattr(self, "places") and self.places is not None:
            return len(self.places)
        return 0

    @property
    def is_completed(self) -> bool:
        if hasattr(self, "places") and self.places:
            return all(p.is_visited for p in self.places)
        return False
