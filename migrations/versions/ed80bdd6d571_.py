"""empty message

Revision ID: ed80bdd6d571
Revises: 570bf4297ae7
Create Date: 2025-01-22 17:17:33.015577

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed80bdd6d571'
down_revision = '570bf4297ae7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cliente', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nombre_completo', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('apellidos', sa.String(length=20), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cliente', schema=None) as batch_op:
        batch_op.drop_column('apellidos')
        batch_op.drop_column('nombre_completo')

    # ### end Alembic commands ###
