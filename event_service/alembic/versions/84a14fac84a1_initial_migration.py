from alembic import op
import sqlalchemy as sa

revision = 'd12a9c995bef'
down_revision = '05b646a9ce74'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'events',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('title', sa.String(length=100), nullable=True),
        sa.Column('description', sa.String(length=500), nullable=True),
        sa.Column('start_time', sa.DateTime(), nullable=True),
        sa.Column('end_time', sa.DateTime(), nullable=True),
        sa.Column('location', sa.String(length=200), nullable=True),
        sa.Column('participants', sa.Text(), nullable=True)
    )


def downgrade():
    op.drop_table('events')
