"""Make cohort_id nullable in projects

Revision ID: 63f974196517
Revises: 49540b071e77
Create Date: 2024-11-13 00:22:00.753039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63f974196517'
down_revision = '49540b071e77'
branch_labels = None
depends_on = None


def upgrade():
    # Make 'cohort_id' column nullable
    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.alter_column('cohort_id',
                              existing_type=sa.Integer(),
                              nullable=True)


def downgrade():
    # Revert 'cohort_id' column to NOT NULL if you need to roll back
    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.alter_column('cohort_id',
                              existing_type=sa.Integer(),
                              nullable=False)

    # ### end Alembic commands ###
