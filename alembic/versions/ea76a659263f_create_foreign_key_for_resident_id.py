"""create foreign key for resident_id

Revision ID: ea76a659263f
Revises: 1f595d244ecb
Create Date: 2022-06-24 13:54:45.977380

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ea76a659263f"
down_revision = "1f595d244ecb"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("address", sa.Column("resident_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "fk_address_user_id",
        source_table="address",
        referent_table="user",
        local_cols=["resident_id"],
        remote_cols=["id"],
    )


def downgrade() -> None:
    op.drop_constraint("fk_address_user_id", "address", "foreignkey")
    op.drop_column("address", "resident_id")
