"""Change house.name to be of type string not int

Revision ID: c921b344e2f7
Revises: a27d350193bd
Create Date: 2018-03-13 15:30:30.282780

"""

# revision identifiers, used by Alembic.
revision = 'c921b344e2f7'
down_revision = 'a27d350193bd'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('houses', 'name', existing_type=sa.Integer(),
                    type_=sa.String())


def downgrade():
    op.alter_column('houses', 'name', existing_type=sa.String(),
                    type_=sa.Integer())
