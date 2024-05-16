"""Add content column to post table

Revision ID: ca0cbc1e3813
Revises: ef1bae600e7a
Create Date: 2024-03-26 09:25:44.476463

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ca0cbc1e3813'
down_revision: Union[str, None] = 'ef1bae600e7a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts' , sa.Column('content' , sa.String() , nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
