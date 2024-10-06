"""Initial migration

Revision ID: f7dfc7a14a66
Revises: 
Create Date: 2024-10-06 01:30:53.900289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7dfc7a14a66'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todo_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task', sa.String(length=100), nullable=False),
    sa.Column('completed', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('todo_item')
    # ### end Alembic commands ###
