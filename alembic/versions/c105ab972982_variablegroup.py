"""VariableGroup

Revision ID: c105ab972982
Revises: e81e50a2960c
Create Date: 2020-09-06 18:27:52.075828

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c105ab972982'
down_revision = 'e81e50a2960c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('doku_variable_group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('document_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['document_id'], ['doku_document.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_unique_constraint(None, 'doku_snippet', ['id'])
    op.add_column('doku_variable', sa.Column('group_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'doku_variable', 'doku_variable_group', ['group_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'doku_variable', type_='foreignkey')
    op.drop_column('doku_variable', 'group_id')
    op.drop_constraint(None, 'doku_snippet', type_='unique')
    op.drop_table('doku_variable_group')
    # ### end Alembic commands ###
