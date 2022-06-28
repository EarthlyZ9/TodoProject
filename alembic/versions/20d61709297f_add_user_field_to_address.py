"""add user field to address

Revision ID: 20d61709297f
Revises: 8367264c3042
Create Date: 2022-06-28 12:49:18.173370

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "20d61709297f"
down_revision = "8367264c3042"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("address", sa.Column("user_id", sa.Integer()))
    op.create_foreign_key(
        "fk_address_user_id",
        source_table="address",
        referent_table="user",
        local_cols=["user_id"],
        remote_cols=["id"],
    )


def downgrade() -> None:
    op.drop_constraint("fk_Address_user_id", "address", "foreignkey")
    op.drop_column("address", "user_id")
