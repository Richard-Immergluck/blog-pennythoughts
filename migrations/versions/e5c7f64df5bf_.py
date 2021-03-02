"""empty message

Revision ID: e5c7f64df5bf
Revises: 8a697a22a03d
Create Date: 2021-03-01 22:01:16.113136

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5c7f64df5bf'
down_revision = '8a697a22a03d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('first_name', table_name='user')
    op.drop_index('last_name', table_name='user')
    op.drop_index('username', table_name='user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('username', 'user', ['username'], unique=True)
    op.create_index('last_name', 'user', ['last_name'], unique=True)
    op.create_index('first_name', 'user', ['first_name'], unique=True)
    # ### end Alembic commands ###