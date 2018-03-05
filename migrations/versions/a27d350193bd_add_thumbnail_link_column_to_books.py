"""Add thumbnail_link column to books

Revision ID: a27d350193bd
Revises: b6673fe8ed45
Create Date: 2018-03-04 20:47:08.059654

"""

# revision identifiers, used by Alembic.
revision = 'a27d350193bd'
down_revision = 'b6673fe8ed45'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('thumbnail_link', sa.String(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('books', 'thumbnail_link')
    ### end Alembic commands ###
