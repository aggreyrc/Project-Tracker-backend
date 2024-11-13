"""Add cohort relationship to project member

Revision ID: 49540b071e77
Revises: a2c036404d16
Create Date: 2024-11-11 22:53:18.563859

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49540b071e77'
down_revision = 'a2c036404d16'
branch_labels = None
depends_on = None


def upgrade():
# Use batch mode to work around SQLite limitations
    with op.batch_alter_table('project_members', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cohort_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            'fk_project_members_cohort',
            'cohorts',
            ['cohort_id'],
            ['id']
        )


def downgrade():
    with op.batch_alter_table('project_members', schema=None) as batch_op:
        batch_op.drop_constraint('fk_project_members_cohort', type_='foreignkey')
        batch_op.drop_column('cohort_id')

    # ### end Alembic commands ###
