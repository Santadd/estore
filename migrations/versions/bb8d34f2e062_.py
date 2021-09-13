"""empty message

Revision ID: bb8d34f2e062
Revises: d2b53f69e13d
Create Date: 2021-09-02 15:02:42.786860

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb8d34f2e062'
down_revision = 'd2b53f69e13d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customer_order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('invoice', sa.String(length=50), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('customer_id', sa.String(length=50), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('orders', estore.users.models.JsonEncodedDict(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('invoice')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('customer_order')
    # ### end Alembic commands ###
