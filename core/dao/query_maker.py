import pandas as pd
import psycopg2
from config import SQLALCHEMY_DATABASE_URL

def conn_tear_down(query_func):
    
    def func(*args, **kwargs):
        
        conn = psycopg2.connect(SQLALCHEMY_DATABASE_URL)
        cursor = conn.cursor()
        try:
            result = query_func(*args, cursor = cursor, **kwargs)
        finally:
            cursor.close()
            conn.close()
        
        return result
    
    return func

@conn_tear_down
def make_query(query, cursor):
    
    cursor.execute(query)
    
    return cursor.fetchall()


class QueryMaker:

    def __init__(self):

        self.tables = self.list_tables()

    def list_tables(self):

        tables = """select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';"""

        rows =  make_query(tables)

        return [r[0] for r in rows]

    def query_estrela(self, table, limit = None):
        
        if limit is None:
            query = f"""SELECT * FROM sj2234o.{table}"""
        else:
            query = f"""SELECT * FROM sj2234o.{table} limit {limit}"""
        
        return make_query(query)

    def get_col_names(self, table):
    
        query = f"""
            SELECT *
            FROM information_schema.columns
            WHERE table_schema = 'sj2234o'
            AND table_name   = '{table}';
            """
        
        rows = make_query(query)
        
        nom_cols = [r[3] for r in rows]
        
        return nom_cols

    def table_as_df(self, table, limit=10):
    
        rows = self.query_estrela(table, limit)
        columns = self.get_col_names(table)
        
        return pd.DataFrame(data = rows, columns = columns)

    def __call__(self, table, limit=10):

        if table not in self.tables:
            raise ValueError(f'Table {table} must be in {self.tables}')

        return self.table_as_df(table, limit)