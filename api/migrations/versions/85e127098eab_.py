"""empty message

Revision ID: 85e127098eab
Revises: 85f6f9c47c6c
Create Date: 2020-07-05 20:57:28.478623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85e127098eab'
down_revision = '85f6f9c47c6c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uniq_horse_name', 'horses', type_='unique')
    op.create_unique_constraint('uniq_horse_name', 'horses', ['name', 'year_born', 'location_born'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uniq_horse_name', 'horses', type_='unique')
    op.create_unique_constraint('uniq_horse_name', 'horses', ['name'])
    # ### end Alembic commands ###
