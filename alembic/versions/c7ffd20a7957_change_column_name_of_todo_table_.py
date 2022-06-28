"""change column name of todo table, complete to isCompleted

Revision ID: c7ffd20a7957
Revises: 20d61709297f
Create Date: 2022-06-28 15:07:45.459897

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c7ffd20a7957"
down_revision = "20d61709297f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "todo", "complete", new_column_name="isCompleted", existing_type=sa.Boolean()
    )


def downgrade() -> None:
    pass
