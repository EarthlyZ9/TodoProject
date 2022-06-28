"""make resident_id un-nullable

Revision ID: f6f04071870e
Revises: ea76a659263f
Create Date: 2022-06-24 14:00:22.528348

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f6f04071870e"
down_revision = "ea76a659263f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "address", "resident_id", nullable=False, existing_type=sa.Integer()
    )


def downgrade() -> None:
    pass
