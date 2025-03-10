"""empty message

Revision ID: 94626e894e04
Revises: 2f623eb354df
Create Date: 2024-11-18 16:25:07.742934

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94626e894e04'
down_revision: Union[str, None] = '2f623eb354df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images', sa.Column('filename', sa.String(), nullable=False))
    op.drop_column('images', 'image_path')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images', sa.Column('image_path', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('images', 'filename')
    # ### end Alembic commands ###
