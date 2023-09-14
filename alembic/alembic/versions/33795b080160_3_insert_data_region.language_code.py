"""3_insert_data_region.language_code

Revision ID: 33795b080160
Revises: 28e7a8d501e6
Create Date: 2023-09-14 15:31:31.819017

"""
from alembic import op
import sqlalchemy as sa

from utils import commit_sql

# revision identifiers, used by Alembic.
revision = '33795b080160'
down_revision = '28e7a8d501e6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    commit_sql("""
            insert into region.language_code(country_code,lang_code)
            values ('en','en'), ('vn','vi');
        """,
        "\n Insert 2 values into table region.language_code successfully!")


def downgrade() -> None:
    commit_sql("""
            DELETE FROM region.language_code
            WHERE (country_code = 'en' AND lang_code = 'en')
                OR (country_code = 'vn' AND lang_code = 'vi');
        """,
        "\n Remove 2 values from table region.language_code successfully!")