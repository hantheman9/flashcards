"""change description

Revision ID: 9044c86ccb56
Revises: 
Create Date: 2023-07-20 14:45:59.693710

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9044c86ccb56'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=120), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('password_hash'),
    sa.UniqueConstraint('username')
    )
    op.create_table('flashcard',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('word', sa.String(length=120), nullable=False),
    sa.Column('definition', sa.Text(), nullable=False),
    sa.Column('bin', sa.Integer(), nullable=True),
    sa.Column('next_review_time', sa.DateTime(), nullable=True),
    sa.Column('incorrect_count', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('flashcard')
    op.drop_table('user')
    # ### end Alembic commands ###
