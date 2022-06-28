"""create address_id to users

Revision ID: 1f595d244ecb
Revises: c26714c02a0c
Create Date: 2022-06-24 09:46:20.288423

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "1f595d244ecb"
down_revision = "c26714c02a0c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("user", sa.Column("address_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "address_user_fk",
        source_table="user",
        referent_table="address",
        local_cols=["address_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("address_user_fk", table_name="user")
    op.drop_column("users", "address_id")
