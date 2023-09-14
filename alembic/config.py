import os

DATABASE_URI = os.environ.get('DATABASE_URI',  r'postgresql+psycopg2://dummy:dummy@localhost:5432/postgres') 