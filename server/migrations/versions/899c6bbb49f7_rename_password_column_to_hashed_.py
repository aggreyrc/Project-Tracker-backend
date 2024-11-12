"""Rename password column to hashed_password

Revision ID: 899c6bbb49f7
Revises: 4e39fbbd84c8
Create Date: 2024-11-12 03:21:59.943895

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '899c6bbb49f7'
down_revision = '4e39fbbd84c8'
branch_labels = None
depends_on = None


def upgrade():
    # Rename password column to hashed_password
    op.alter_column('users', 'password', new_column_name='password_hash')

def downgrade():
    # Rename hashed_password back to password
    op.alter_column('users', 'password_hash', new_column_name='password')

    # ### end Alembic commands ###
