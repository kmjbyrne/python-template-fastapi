"""create item

Revision ID: 0b788dd4e28f
Revises:
Create Date: 2026-08-21 00:08:48.327649
"""

from collections.abc import Sequence

import sqlalchemy as sa
import sqlmodel.sql.sqltypes

from alembic import op

revision: str = "0b788dd4e28f"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Apply the migration."""
    op.create_table(
        "item",
        sa.Column("guid", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("guid"),
    )


def downgrade() -> None:
    """Revert the migration."""
    op.drop_table("item")
