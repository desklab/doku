"""Author

Revision ID: 3040ce8bd808
Revises: b86f36e8e5f1
Create Date: 2020-08-15 21:30:48.791968

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table
from sqlalchemy.sql.expression import select


# revision identifiers, used by Alembic.
revision = '3040ce8bd808'
down_revision = 'b86f36e8e5f1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('doku_document', sa.Column('author', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'doku_document', ['id'])
    op.create_foreign_key(None, 'doku_document', 'doku_user', ['author'], ['id'])
    op.create_unique_constraint(None, 'doku_resource', ['id'])
    op.create_unique_constraint(None, 'doku_stylesheet', ['id'])
    op.create_unique_constraint(None, 'doku_template', ['id'])
    op.create_unique_constraint(None, 'doku_user', ['id'])
    op.create_unique_constraint(None, 'doku_variable', ['id'])
    documents = table(
        'doku_document',
        sa.Column('author', sa.Integer()),
    )
    op.execute(
        documents.update().values({documents.c.author: 1})
    )
    op.alter_column(
        table_name="doku_document",
        column_name="author",
        nullable=False,
        existing_nullable=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'doku_variable', type_='unique')
    op.drop_constraint(None, 'doku_user', type_='unique')
    op.drop_constraint(None, 'doku_template', type_='unique')
    op.drop_constraint(None, 'doku_stylesheet', type_='unique')
    op.drop_constraint(None, 'doku_resource', type_='unique')
    op.drop_constraint(None, 'doku_document', type_='foreignkey')
    op.drop_constraint(None, 'doku_document', type_='unique')
    op.drop_column('doku_document', 'author')
    # ### end Alembic commands ###
