"""add apt_num col to address table

Revision ID: 8367264c3042
Revises: f6f04071870e
Create Date: 2022-06-25 11:38:29.553765

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8367264c3042"
down_revision = "f6f04071870e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("address", sa.Column("apt_num", sa.String(20), nullable=True))


def downgrade() -> None:
    op.drop_column("address", "apt_num")
