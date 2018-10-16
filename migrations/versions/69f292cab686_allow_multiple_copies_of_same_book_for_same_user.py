"""Modify owned_book_copies to have primary key 'id', not 'id, user_id, book_id'

Revision ID: 69f292cab686
Revises: 6fd667f1d6ae
Create Date: 2018-10-16 15:47:47.916881

"""

# revision identifiers, used by Alembic.
revision = '69f292cab686'
down_revision = '6fd667f1d6ae'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_table('owned_book_copies')
    op.create_table('owned_book_copies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('borrower_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
    sa.ForeignKeyConstraint(['borrower_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('owned_book_copies')
    op.create_table('owned_book_copies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('borrower_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
    sa.ForeignKeyConstraint(['borrower_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('owner_id', 'book_id', 'id')
    )
