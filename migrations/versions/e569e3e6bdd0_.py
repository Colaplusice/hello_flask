"""empty message

Revision ID: e569e3e6bdd0
Revises: 713e86ee90e8
Create Date: 2018-08-12 11:51:18.751509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e569e3e6bdd0"
down_revision = "713e86ee90e8"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "page_view", sa.Column("req_method", sa.String(length=64), nullable=False)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("page_view", "req_method")
    # ### end Alembic commands ###
