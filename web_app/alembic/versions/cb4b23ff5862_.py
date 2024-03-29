"""empty message

Revision ID: cb4b23ff5862
Revises: 52c5864674ea
Create Date: 2022-03-04 13:40:22.999426

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "cb4b23ff5862"
down_revision = "52c5864674ea"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("dataset", sa.Column("md5_hash", sa.String(), nullable=False))
    op.create_unique_constraint(None, "dataset", ["md5_hash"])
    op.add_column("model", sa.Column("md5_hash", sa.String(), nullable=False))
    op.create_unique_constraint(None, "model", ["md5_hash"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "model", type_="unique")
    op.drop_column("model", "md5_hash")
    op.drop_constraint(None, "dataset", type_="unique")
    op.drop_column("dataset", "md5_hash")
    # ### end Alembic commands ###
