"""empty message

Revision ID: 5bd2be4991b8
Revises: c495118a9587
Create Date: 2018-06-07 19:12:16.275701

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5bd2be4991b8"
down_revision = "c495118a9587"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("posts", sa.Column("title", sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("posts", "title")
    # ### end Alembic commands ###
