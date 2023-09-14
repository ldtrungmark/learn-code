"""2_create_table_region.language_code

Revision ID: 28e7a8d501e6
Revises: 9c34d78c70af
Create Date: 2023-09-14 15:05:26.951108

"""
from alembic import op
import sqlalchemy as sa

from utils import commit_sql


# revision identifiers, used by Alembic.
revision = '28e7a8d501e6'
down_revision = '9c34d78c70af'
branch_labels = None
depends_on = None


def upgrade() -> None:
    commit_sql("""
            CREATE TABLE region.language_code(
                country_code VARCHAR(2) UNIQUE,
                lang_code VARCHAR(2) UNIQUE
            );
        """,
        "\n Create table region.language_code successfully!")


def downgrade() -> None:
    commit_sql("""
            drop table if exists region.language_code;
        """,
        "\n Remove table region.language_code successfully!")