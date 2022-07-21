"""empty message

Revision ID: c7d3e7e86fe0
Revises: b6f593818541
Create Date: 2022-06-17 18:58:45.565407

"""
from alembic import op
import sqlalchemy as sa
from doku.models import TSVector


# revision identifiers, used by Alembic.
revision = 'c7d3e7e86fe0'
down_revision = 'b6f593818541'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('doku_resource', sa.Column('__ts_vector__', TSVector(), sa.Computed("to_tsvector('english', name)", persisted=True), nullable=True))
    op.create_index('doku_resource___ts_vector__', 'doku_resource', ['__ts_vector__'], unique=False, postgresql_using='gin')
    op.add_column('doku_snippet', sa.Column('__ts_vector__', TSVector(), sa.Computed("to_tsvector('english', name)", persisted=True), nullable=True))
    op.create_index('doku_snippet___ts_vector__', 'doku_snippet', ['__ts_vector__'], unique=False, postgresql_using='gin')
    op.add_column('doku_stylesheet', sa.Column('__ts_vector__', TSVector(), sa.Computed("to_tsvector('english', name)", persisted=True), nullable=True))
    op.create_index('doku_stylesheet___ts_vector__', 'doku_stylesheet', ['__ts_vector__'], unique=False, postgresql_using='gin')
    op.add_column('doku_template', sa.Column('__ts_vector__', TSVector(), sa.Computed("to_tsvector('english', name)", persisted=True), nullable=True))
    op.create_index('doku_template___ts_vector__', 'doku_template', ['__ts_vector__'], unique=False, postgresql_using='gin')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('doku_template___ts_vector__', table_name='doku_template', postgresql_using='gin')
    op.drop_column('doku_template', '__ts_vector__')
    op.drop_index('doku_stylesheet___ts_vector__', table_name='doku_stylesheet', postgresql_using='gin')
    op.drop_column('doku_stylesheet', '__ts_vector__')
    op.drop_index('doku_snippet___ts_vector__', table_name='doku_snippet', postgresql_using='gin')
    op.drop_column('doku_snippet', '__ts_vector__')
    op.drop_index('doku_resource___ts_vector__', table_name='doku_resource', postgresql_using='gin')
    op.drop_column('doku_resource', '__ts_vector__')
    # ### end Alembic commands ###