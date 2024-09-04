"""create temperature table

Revision ID: 9dac9cbaaadc
Revises: a940617491f3
Create Date: 2024-09-04 20:47:16.923455

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9dac9cbaaadc'
down_revision: Union[str, None] = 'a940617491f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_temperature_id', table_name='temperature')
    op.drop_table('temperature')
    op.drop_index('ix_city_id', table_name='city')
    op.drop_table('city')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('city',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), nullable=False),
    sa.Column('additional_info', sa.VARCHAR(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index('ix_city_id', 'city', ['id'], unique=False)
    op.create_table('temperature',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('city_id', sa.INTEGER(), nullable=True),
    sa.Column('date_time', sa.DATETIME(), nullable=True),
    sa.Column('temperature', sa.FLOAT(), nullable=True),
    sa.ForeignKeyConstraint(['city_id'], ['city.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_temperature_id', 'temperature', ['id'], unique=False)
    # ### end Alembic commands ###
