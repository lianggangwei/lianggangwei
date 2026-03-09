import sqlite3
import pandas as pd
from sqlalchemy import create_engine, text
from typing import List, Dict, Any, Optional
import os


class SQLiteTool:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_path)
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()

    def execute(self, sql: str, params: tuple = None):
        if not self.connection:
            self.connect()
        cursor = self.connection.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        self.connection.commit()
        return cursor

    def query(self, sql: str, params: tuple = None) -> List[Dict]:
        if not self.connection:
            self.connect()
        cursor = self.connection.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def query_to_df(self, sql: str, params: tuple = None) -> pd.DataFrame:
        if not self.connection:
            self.connect()
        return pd.read_sql_query(sql, self.connection, params=params)

    def insert(self, table: str, data: Dict):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        self.execute(sql, tuple(data.values()))

    def insert_many(self, table: str, data_list: List[Dict]):
        if not data_list:
            return
        columns = ', '.join(data_list[0].keys())
        placeholders = ', '.join(['?' for _ in data_list[0]])
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        if not self.connection:
            self.connect()
        cursor = self.connection.cursor()
        cursor.executemany(sql, [tuple(d.values()) for d in data_list])
        self.connection.commit()

    def update(self, table: str, data: Dict, where: str, where_params: tuple = None):
        set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where}"
        params = tuple(data.values()) + (where_params or ())
        self.execute(sql, params)

    def delete(self, table: str, where: str, params: tuple = None):
        sql = f"DELETE FROM {table} WHERE {where}"
        self.execute(sql, params)

    def create_table(self, table: str, columns: Dict[str, str]):
        column_defs = ', '.join([f"{k} {v}" for k, v in columns.items()])
        sql = f"CREATE TABLE IF NOT EXISTS {table} ({column_defs})"
        self.execute(sql)

    def get_tables(self) -> List[str]:
        result = self.query("SELECT name FROM sqlite_master WHERE type='table'")
        return [row['name'] for row in result]

    def df_to_table(self, df: pd.DataFrame, table: str, if_exists: str = 'replace'):
        if not self.connection:
            self.connect()
        df.to_sql(table, self.connection, if_exists=if_exists, index=False)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class SQLAlchemyTool:
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        self.connection = None

    def connect(self):
        self.connection = self.engine.connect()
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()

    def execute(self, sql: str, **kwargs):
        if not self.connection:
            self.connect()
        return self.connection.execute(text(sql), **kwargs)

    def query(self, sql: str, **kwargs) -> pd.DataFrame:
        return pd.read_sql_query(text(sql), self.engine, **kwargs)

    def df_to_table(self, df: pd.DataFrame, table: str, if_exists: str = 'replace', schema: str = None):
        df.to_sql(table, self.engine, if_exists=if_exists, index=False, schema=schema)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
