"""empty message

Revision ID: 97df6af4309e
Revises: c3b98818affb
Create Date: 2021-11-02 17:39:01.413586

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97df6af4309e'
down_revision = 'c3b98818affb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_basic', sa.Column('nickname', sa.String(length=16), nullable=True))
    op.add_column('user_basic', sa.Column('password', sa.String(length=64), nullable=True))
    op.add_column('user_basic', sa.Column('salt', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_basic', 'salt')
    op.drop_column('user_basic', 'password')
    op.drop_column('user_basic', 'nickname')
    # ### end Alembic commands ###