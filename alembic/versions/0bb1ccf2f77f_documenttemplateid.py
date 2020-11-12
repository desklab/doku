"""DocumentTemplateID

Revision ID: 0bb1ccf2f77f
Revises: c105ab972982
Create Date: 2020-11-12 17:49:46.605577

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0bb1ccf2f77f'
down_revision = 'c105ab972982'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('doku_document', 'template_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_constraint('doku_variable_group_id_fkey', 'doku_variable', type_='foreignkey')
    op.create_foreign_key(None, 'doku_variable', 'doku_variable_group', ['group_id'], ['id'], ondelete='SET NULL')
    op.create_unique_constraint(None, 'doku_variable_group', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'doku_variable_group', type_='unique')
    op.drop_constraint(None, 'doku_variable', type_='foreignkey')
    op.create_foreign_key('doku_variable_group_id_fkey', 'doku_variable', 'doku_variable_group', ['group_id'], ['id'])
    op.alter_column('doku_document', 'template_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
