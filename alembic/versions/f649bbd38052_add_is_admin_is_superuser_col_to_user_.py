"""add is_admin is_superuser col to user table

Revision ID: f649bbd38052
Revises: ce9c6be83cbe
Create Date: 2022-06-30 11:27:56.077645

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f649bbd38052"
down_revision = "ce9c6be83cbe"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "user", sa.Column("is_admin", sa.Boolean, default=False, nullable=False)
    )
    op.add_column(
        "user", sa.Column("is_superuser", sa.Boolean, default=False, nullable=False)
    )


def downgrade() -> None:
    op.drop_column("user", "is_admin")
    op.drop_column("user", "is_superuser")
