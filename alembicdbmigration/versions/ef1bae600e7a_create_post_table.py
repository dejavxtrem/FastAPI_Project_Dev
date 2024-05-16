"""create post table

Revision ID: ef1bae600e7a
Revises: 
Create Date: 2024-03-18 08:50:23.031933

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef1bae600e7a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
                     sa.Column('title' , sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
 