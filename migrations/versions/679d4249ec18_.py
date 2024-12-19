"""empty message

Revision ID: 679d4249ec18
Revises: 
Create Date: 2024-12-19 19:57:03.031642

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '679d4249ec18'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cliente',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.Column('telefono', sa.String(length=15), nullable=True),
    sa.Column('direccion', sa.String(length=200), nullable=True),
    sa.Column('fecha_creacion', sa.DateTime(), nullable=True),
    sa.Column('fecha_nacimiento', sa.Date(), nullable=True),
    sa.Column('tipo_documento', sa.String(length=20), nullable=True),
    sa.Column('numero_documento', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('numero_documento')
    )
    op.create_table('seguro',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tipo', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tipo_transaccion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=50), nullable=True),
    sa.Column('descripcion', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('asesor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=True),
    sa.Column('puesto', sa.String(length=50), nullable=True),
    sa.Column('fecha_contratacion', sa.DateTime(), nullable=True),
    sa.Column('activo', sa.Boolean(), nullable=True),
    sa.Column('cliente_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cliente_id'], ['cliente.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('configuracion_usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_usuario', sa.Integer(), nullable=True),
    sa.Column('modo_oscuro', sa.Boolean(), nullable=True),
    sa.Column('idioma', sa.String(length=5), nullable=True),
    sa.Column('componentesSave', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['id_usuario'], ['cliente.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cuenta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('numero_cuenta', sa.String(length=20), nullable=True),
    sa.Column('tipo_cuenta', sa.String(length=50), nullable=True),
    sa.Column('saldo', sa.Float(), nullable=True),
    sa.Column('cliente_id', sa.Integer(), nullable=True),
    sa.Column('estado', sa.Integer(), nullable=True),
    sa.Column('seguro_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cliente_id'], ['cliente.id'], ),
    sa.ForeignKeyConstraint(['seguro_id'], ['seguro.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('numero_cuenta')
    )
    op.create_table('transaccion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cuenta_id', sa.Integer(), nullable=True),
    sa.Column('tipo', sa.String(length=50), nullable=True),
    sa.Column('monto', sa.Float(), nullable=True),
    sa.Column('fecha', sa.DateTime(), nullable=True),
    sa.Column('descripcion', sa.String(length=200), nullable=True),
    sa.Column('tipo_transaccion_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cuenta_id'], ['cuenta.id'], ),
    sa.ForeignKeyConstraint(['tipo_transaccion_id'], ['tipo_transaccion.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transaccion')
    op.drop_table('cuenta')
    op.drop_table('configuracion_usuario')
    op.drop_table('asesor')
    op.drop_table('user')
    op.drop_table('tipo_transaccion')
    op.drop_table('seguro')
    op.drop_table('cliente')
    # ### end Alembic commands ###