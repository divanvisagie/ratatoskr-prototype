"""Create history table

Revision ID: 9b92ff2daff0
Revises: cedd97387165
Create Date: 2023-02-25 21:02:10.013685

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b92ff2daff0'
down_revision = 'cedd97387165'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'history',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('question', sa.Text, nullable=False),
        sa.Column('answer', sa.Text, nullable=False),
        sa.Column('answered_by', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE')
    )


def downgrade() -> None:
    op.drop_table('history')
