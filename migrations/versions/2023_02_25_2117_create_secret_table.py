"""Create secret table

Revision ID: 6b1b22353ccb
Revises: 9b92ff2daff0
Create Date: 2023-02-25 21:17:15.369546

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b1b22353ccb'
down_revision = '9b92ff2daff0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'secret',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('app_id', sa.Integer(), nullable=False),
        sa.Column('question', sa.Text(), nullable=False),
        sa.Column('answer', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE')
    )


def downgrade() -> None:
    op.drop_table('secret')
