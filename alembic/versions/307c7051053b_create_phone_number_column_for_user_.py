"""create phone number column for user table

Revision ID: 307c7051053b
Revises: 
Create Date: 2022-06-24 09:14:45.341968

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "307c7051053b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # op.add_column("user", sa.Column("phone_number", sa.String(11), nullable=True))
    pass


def downgrade() -> None:
    op.drop_column("user", "phone_number")
