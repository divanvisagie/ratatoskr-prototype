"""Create user table

Revision ID: cedd97387165
Revises: 
Create Date: 2023-02-25 20:57:36.934672

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cedd97387165'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('telegram_username', sa.String(255)),
        sa.Column('access_level', sa.Integer),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )

def downgrade() -> None:
    op.drop_table('user')
