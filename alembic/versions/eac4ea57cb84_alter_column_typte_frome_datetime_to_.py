"""alter column typte frome datetime to timestamp'


Revision ID: eac4ea57cb84
Revises: 7f3eb1e55c94
Create Date: 2022-06-28 17:17:39.770324

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.sql as func
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = "eac4ea57cb84"
down_revision = "7f3eb1e55c94"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "todo",
        "created_at",
        type=sa.TIMESTAMP,
        server_default=func.now(),
        existing_type=sa.DateTime(),
    )
    op.alter_column(
        "todo",
        "updated_at",
        type=sa.TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        existing_type=sa.DateTime(),
    )
    op.alter_column(
        "user",
        "created_at",
        type=sa.TIMESTAMP,
        server_default=func.now(),
        existing_type=sa.DateTime(),
    )
    op.alter_column(
        "user",
        "updated_at",
        type=sa.TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        existing_type=sa.DateTime(),
    )
    op.alter_column(
        "address",
        "created_at",
        type=sa.TIMESTAMP,
        server_default=func.now(),
        existing_type=sa.DateTime(),
    )
    op.alter_column(
        "address",
        "updated_at",
        type=sa.TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        existing_type=sa.DateTime(),
    )


def downgrade() -> None:
    pass
