"""1_initial_create_public_schema

Revision ID: 9c34d78c70af
Revises: 
Create Date: 2023-09-14 13:41:44.628948

"""
from alembic import op
import sqlalchemy as sa
import pandas as pd
import pathlib

from utils import camel_to_snake, write_df_to_table, commit_sql


# revision identifiers, used by Alembic.
revision = '9c34d78c70af'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    commit_sql(upgrade_sql,"\nCreate schema region successfully!")
    
    # Create gsma data
    path = pathlib.Path().resolve()
    country_code_df = pd.read_csv(f'{path}/data/country_code.csv', sep=',', on_bad_lines='skip')
    # convert camel to snake columns
    country_code_df.columns = camel_to_snake(country_code_df.columns)
    # write df to postgre table
    write_df_to_table(country_code_df, schema='region', table_name='country_code')

    print("\nCreate table region.country_code successfully!")


def downgrade() -> None:
    commit_sql(downgrade_sql,"\nRemove region.country_code successfully!")

upgrade_sql = f"""
    CREATE SCHEMA IF NOT EXISTS region;
"""

downgrade_sql = f"""
    drop table if exists region.country_code;
    drop schema if exists region;
"""
