"""Change required fields

Revision ID: 46c3782c6e9a
Revises: 51e69d5b278a
Create Date: 2023-05-25 20:59:53.849759

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '46c3782c6e9a'
down_revision = '51e69d5b278a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.alter_column('genres',
               existing_type=postgresql.ARRAY(sa.VARCHAR(length=120)),
               nullable=False)

    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.alter_column('phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
        batch_op.alter_column('genres',
               existing_type=postgresql.ARRAY(sa.VARCHAR(length=120)),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.alter_column('genres',
               existing_type=postgresql.ARRAY(sa.VARCHAR(length=120)),
               nullable=True)
        batch_op.alter_column('phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)

    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.alter_column('genres',
               existing_type=postgresql.ARRAY(sa.VARCHAR(length=120)),
               nullable=True)

    # ### end Alembic commands ###
