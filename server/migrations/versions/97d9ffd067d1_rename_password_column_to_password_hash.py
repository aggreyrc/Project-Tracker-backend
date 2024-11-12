"""Rename password column to password_hash

Revision ID: 97d9ffd067d1
Revises: 423aad59674f
Create Date: 2024-11-12 03:42:32.662737

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97d9ffd067d1'
down_revision = '423aad59674f'
branch_labels = None
depends_on = None


def upgrade():
    # Rename password column to hashed_password
    op.alter_column('users', 'password', new_column_name='password_hash')

def downgrade():
    # Rename hashed_password back to password
    op.alter_column('users', 'password_hash', new_column_name='password')

    # ### end Alembic commands ###
