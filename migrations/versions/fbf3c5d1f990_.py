"""empty message

Revision ID: fbf3c5d1f990
Revises: 251c2165086f
Create Date: 2021-11-02 21:00:36.181144

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fbf3c5d1f990'
down_revision = '251c2165086f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
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
    # ### end Alembic commands ###
