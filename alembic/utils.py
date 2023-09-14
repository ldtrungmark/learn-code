import psycopg2
from sqlalchemy import create_engine
from urllib.parse import urlparse, unquote
import config
import re

def database_connect():
    """ Connect to the PostgreSQL database server """
    r = urlparse(config.DATABASE_URI)
    conn_args = {
        'host': r.hostname,
        'database': r.path[1:],
        'user': r.username,
        'password': unquote(r.password),
        'port': r.port
    }

    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**conn_args)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        # sys.exit(1)
    print("Connection successful")
    return conn

def camel_to_snake(cols):
    # convert camel to snake
    cols = ["_".join(re.findall(r'[a-z0-9]+', col.lower())) for col in cols]
    # remove 1st digit
    cols = ["_"+col if col[0].isdigit() else col for col in cols]
    return cols

def write_df_to_table(df, schema, table_name):
    conn_string = config.DATABASE_URI
    db = create_engine(conn_string)
    conn = db.connect()

    df.to_sql(table_name, con=conn, schema=schema, if_exists='replace', index=False)
    conn.commit()
    conn.close()
    print(f"Write to {schema}.{table_name} successful")

def commit_sql(sql: str, message: str):
    conn = database_connect()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    print(message)
    
