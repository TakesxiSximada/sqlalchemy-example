"""first

Revision ID: 2b6d6c9267c
Revises:
Create Date: 2015-11-10 23:08:00.119608

"""

# revision identifiers, used by Alembic.
revision = '2b6d6c9267c'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa



def upgrade():
    op.create_table(
        'OtherTable',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name_other', sa.String(1024)),
        sa.Column('count_other', sa.Integer, server_default='0'),
        )


def downgrade():
    op.drop_table('OtherTable')
