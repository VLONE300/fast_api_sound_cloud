"""create some models 5

Revision ID: 3924da5d0d2e
Revises: 1d66a3ded6cf
Create Date: 2024-05-15 20:34:36.960505

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3924da5d0d2e'
down_revision: Union[str, None] = '1d66a3ded6cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###