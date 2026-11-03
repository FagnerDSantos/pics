from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, String, func, text
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Studio(Base):
    __tablename__ = "studios"
    __table_args__ = (
        CheckConstraint(
            "status IN ('active', 'suspended', 'canceled')", name="ck_studios_status"
        ),
        CheckConstraint(
            "slug ~ '^[a-z0-9][a-z0-9-]{1,38}[a-z0-9]$' AND slug NOT IN "
            "('admin', 'api', 'app', 'www', 'mail', 'static', 'assets')",
            name="ck_studios_slug",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        server_default=text("gen_random_uuid()"),
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    status: Mapped[str] = mapped_column(
        String(16), nullable=False, default="active", server_default="active"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
