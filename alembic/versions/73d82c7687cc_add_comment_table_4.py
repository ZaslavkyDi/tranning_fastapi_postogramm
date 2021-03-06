"""add comment table 4

Revision ID: 73d82c7687cc
Revises: 59b9b4ea798c
Create Date: 2021-03-01 17:37:19.926176

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73d82c7687cc'
down_revision = '59b9b4ea798c'
branch_labels = None
depends_on = None


def upgrade():
# ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('published_date', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
# ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    # ### end Alembic commands ###
