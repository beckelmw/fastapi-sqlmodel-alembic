"""notes

Revision ID: cc73a24c52c7
Revises: ded6320fada4
Create Date: 2022-08-17 10:55:30.481794

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "cc73a24c52c7"
down_revision = "ded6320fada4"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "notes",
        sa.Column(
            "uuid",
            sqlmodel.sql.sqltypes.GUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("note", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint("uuid"),
    )
    op.create_index(op.f("ix_notes_note"), "notes", ["note"], unique=False)
    op.create_index(op.f("ix_notes_uuid"), "notes", ["uuid"], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_notes_uuid"), table_name="notes")
    op.drop_index(op.f("ix_notes_note"), table_name="notes")
    op.drop_table("notes")
    # ### end Alembic commands ###
