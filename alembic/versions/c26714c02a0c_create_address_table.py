"""create address table

Revision ID: c26714c02a0c
Revises: 307c7051053b
Create Date: 2022-06-24 09:40:14.212732

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "c26714c02a0c"
down_revision = "307c7051053b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # op.create_table(
    #     "address",
    #     sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
    #     sa.Column("address1", sa.String(100), nullable=False),
    #     sa.Column("address2", sa.String(100), nullable=False),
    #     sa.Column("city", sa.String(50), nullable=False),
    #     sa.Column("state", sa.String(50), nullable=False),
    #     sa.Column("country", sa.String(100), nullable=False),
    #     sa.Column("zipcode", sa.String(5), nullable=False),
    # )
    pass


def downgrade() -> None:
    op.drop_table("address")
