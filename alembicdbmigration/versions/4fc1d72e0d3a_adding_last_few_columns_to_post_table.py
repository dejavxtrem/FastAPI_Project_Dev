"""adding last few columns to post table

Revision ID: 4fc1d72e0d3a
Revises: 894ef798a647
Create Date: 2024-05-13 09:32:09.530207

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4fc1d72e0d3a'
down_revision: Union[str, None] = '894ef798a647'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False , server_default='True'))
    op.add_column('posts' , sa.Column(
        'created_at' , sa.TIMESTAMP(timezone=True), nullable=False , server_default=sa.text('NOW()')))
    
    pass


def downgrade():
    op.drop_column('posts' , 'published')
    op.drop_column('posts' , 'created_at')
    pass
