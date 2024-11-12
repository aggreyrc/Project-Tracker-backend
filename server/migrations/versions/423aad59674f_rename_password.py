"""Rename password

Revision ID: 423aad59674f
Revises: 899c6bbb49f7
Create Date: 2024-11-12 03:39:03.192007

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '423aad59674f'
down_revision = '899c6bbb49f7'
branch_labels = None
depends_on = None


def upgrade():
    # Rename password column to hashed_password
    op.alter_column('users', 'password_hash', new_column_name='password')

def downgrade():
    # Rename hashed_password back to password
    op.alter_column('users', 'password', new_column_name='password_hash')

    # ### end Alembic commands ###
