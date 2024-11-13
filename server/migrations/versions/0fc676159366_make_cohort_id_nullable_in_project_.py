"""Make cohort_id nullable in project_members

Revision ID: 0fc676159366
Revises: 63f974196517
Create Date: 2024-11-13 00:27:17.693950

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0fc676159366'
down_revision = '63f974196517'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('project_members', schema=None) as batch_op:
        batch_op.alter_column('cohort_id',
                              existing_type=sa.Integer(),
                              nullable=True)

def downgrade():
    with op.batch_alter_table('project_members', schema=None) as batch_op:
        batch_op.alter_column('cohort_id',
                              existing_type=sa.Integer(),
                              nullable=False)

    # ### end Alembic commands ###
