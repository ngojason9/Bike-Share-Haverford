"""del foreign key

Revision ID: 71a40535706c
Revises: b0d5babecb38
Create Date: 2019-01-13 14:52:21.691221

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71a40535706c'
down_revision = 'b0d5babecb38'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bike', schema=None) as batch_op:
        batch_op.drop_column('holder')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('withholding', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('withholding')

    with op.batch_alter_table('bike', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'user', ['holder'], ['id'])

    # ### end Alembic commands ###
