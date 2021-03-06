"""empty message

Revision ID: 251c2165086f
Revises: 005926094705
Create Date: 2021-11-02 20:58:57.554752

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '251c2165086f'
down_revision = '005926094705'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_basic', sa.Column('token', sa.String(length=128), nullable=True))
    op.add_column('user_basic', sa.Column('token_expire', sa.DateTime(), nullable=True))
    op.alter_column('user_basic', 'salt',
               existing_type=mysql.VARCHAR(length=64),
               nullable=False)
    op.create_unique_constraint(None, 'user_basic', ['account'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_basic', type_='unique')
    op.alter_column('user_basic', 'salt',
               existing_type=mysql.VARCHAR(length=64),
               nullable=True)
    op.drop_column('user_basic', 'token_expire')
    op.drop_column('user_basic', 'token')
    # ### end Alembic commands ###
