"""Increase image_file length

Revision ID: 7c72ca518ac4
Revises: bc4f2e879c4c
Create Date: 2025-06-17 23:49:38.669686

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c72ca518ac4'
down_revision = 'bc4f2e879c4c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('image_file',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=120),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('image_file',
               existing_type=sa.String(length=120),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)

    # ### end Alembic commands ###
