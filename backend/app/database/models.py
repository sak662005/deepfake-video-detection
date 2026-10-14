from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class DetectionJob(Base):
    __tablename__ = "detection_jobs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    video_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    video_name: Mapped[str] = mapped_column(String(255), nullable=False)

    file_path: Mapped[str] = mapped_column(String(500), nullable=False)

    status: Mapped[str] = mapped_column(String(50), default="uploaded")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow
    )

    is_fake: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)

    result_path: Mapped[str | None] = mapped_column(String(500), nullable=True)