"""Create bookings table.

Revision ID: 20260907_01
Revises:
Create Date: 2026-09-07
"""

from collections.abc import Sequence
from alembic import op
import sqlalchemy as sa


revision: str = "20260907_01"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("phone", sa.String(length=12), nullable=False),
        sa.Column("booking_date", sa.Date(), nullable=False),
        sa.Column("booking_time", sa.Time(), nullable=False),
        sa.Column("guests", sa.SmallInteger(), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "active",
                "cancelled",
                name="booking_status",
                native_enum=False,
                create_constraint=True,
            ),
            server_default="active",
            nullable=False,
        ),
        sa.CheckConstraint("guests BETWEEN 1 AND 12", name="guests_range"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_bookings_booking_date", "bookings", ["booking_date"])
    op.create_index(
        "uq_bookings_active_slot",
        "bookings",
        ["booking_date", "booking_time"],
        unique=True,
        sqlite_where=sa.text("status = 'active'"),
    )


def downgrade() -> None:
    op.drop_index("uq_bookings_active_slot", table_name="bookings")
    op.drop_index("ix_bookings_booking_date", table_name="bookings")
    op.drop_table("bookings")
