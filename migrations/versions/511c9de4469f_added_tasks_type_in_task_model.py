"""added tasks type in task model

Revision ID: 511c9de4469f
Revises: e57a47ac0248
Create Date: 2024-10-21 11:13:21.268147

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from common.constants.app_constant import tasksType


# revision identifiers, used by Alembic.
revision: str = '511c9de4469f'
down_revision: Union[str, None] = 'e57a47ac0248'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type', sa.String(length=40)))

    conn = op.get_bind()
    result = conn.execute(sa.text("SELECT id FROM task"))
    rows = result.fetchall()

    for row in rows:
        taskType = tasksType.TEXT.value
        conn.execute(
            sa.text("UPDATE task SET type = :type WHERE id = :id"),
            {"type": taskType, "id": row.id}
        )

    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.alter_column('type', existing_type=sa.String(length=40), nullable=False)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.drop_column('type')

    # ### end Alembic commands ###
