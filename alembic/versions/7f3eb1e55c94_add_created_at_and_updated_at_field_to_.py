"""add created_at and updated_at field to each table

Revision ID: 7f3eb1e55c94
Revises: c7ffd20a7957
Create Date: 2022-06-28 16:43:44.208320

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision = "7f3eb1e55c94"
down_revision = "c7ffd20a7957"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "todo",
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=func.now()),
    )
    op.add_column(
        "todo",
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), onupdate=func.now(), nullable=True
        ),
    )
    op.add_column(
        "user",
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=func.now()),
    )
    op.add_column(
        "user",
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), onupdate=func.now(), nullable=True
        ),
    )
    op.add_column(
        "address",
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=func.now()),
    )
    op.add_column(
        "address",
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), onupdate=func.now(), nullable=True
        ),
    )


def downgrade() -> None:
    pass
