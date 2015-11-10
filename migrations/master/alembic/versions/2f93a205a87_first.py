"""first

Revision ID: 2f93a205a87
Revises:
Create Date: 2015-11-10 23:02:13.528536

"""

# revision identifiers, used by Alembic.
revision = '2f93a205a87'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'MainTable',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(1024)),
        sa.Column('count', sa.Integer, server_default='0'),
        )


def downgrade():
    op.drop_table('MainTable')
