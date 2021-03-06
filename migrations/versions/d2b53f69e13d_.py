"""empty message

Revision ID: d2b53f69e13d
Revises: 2a9b371ef36b
Create Date: 2021-09-02 06:25:22.234084

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2b53f69e13d'
down_revision = '2a9b371ef36b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('address',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('company', sa.String(length=50), nullable=False),
    sa.Column('country', sa.String(length=50), nullable=False),
    sa.Column('street_add', sa.String(length=50), nullable=False),
    sa.Column('city', sa.String(length=50), nullable=False),
    sa.Column('postcode', sa.String(length=50), nullable=False),
    sa.Column('mobile_no', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_unique_constraint(None, 'customer', ['email'])
    op.create_unique_constraint(None, 'customer', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'customer', type_='unique')
    op.drop_constraint(None, 'customer', type_='unique')
    op.drop_table('address')
    # ### end Alembic commands ###
