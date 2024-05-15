"""create some models 6

Revision ID: 2dae0aeb875e
Revises: 3924da5d0d2e
Create Date: 2024-05-15 20:35:39.040784

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2dae0aeb875e'
down_revision: Union[str, None] = '3924da5d0d2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'genres', ['name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'genres', type_='unique')
    # ### end Alembic commands ###
