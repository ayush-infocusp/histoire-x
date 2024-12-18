"""added unique and not nullable constraint on new column uuid to user table

Revision ID: e57a47ac0248
Revises: 2fc0b68bbc50
Create Date: 2024-10-16 13:30:11.618733

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from uuid import uuid4


# revision identifiers, used by Alembic.
revision: str = 'e57a47ac0248'
down_revision: Union[str, None] = '2fc0b68bbc50'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('uuid', sa.String(length=36), nullable=True))

    conn = op.get_bind()
    result = conn.execute(sa.text("SELECT id FROM user"))
    rows = result.fetchall()

    for row in rows:
        uuid = str(uuid4())
        conn.execute(
            sa.text("UPDATE user SET uuid = :uuid WHERE id = :id"),
            {"uuid": uuid, "id": row.id}
        )

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('uuid', existing_type=sa.String(length=36), nullable=False)
        batch_op.create_unique_constraint('uq_user_email', ['email'])
        batch_op.create_unique_constraint('uq_user_uuid', ['uuid'])

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('uq_user_email', type_='unique')
        batch_op.drop_constraint('uq_user_uuid', type_='unique')
        batch_op.drop_column('uuid')
    # ### end Alembic commands ###
