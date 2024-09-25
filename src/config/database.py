import os
import pyodbc
import pandas as pd
from config import MDB_FILE
from contextlib import ContextDecorator

class BaseConnection(ContextDecorator):
    @property
    def connection_string(self):
        raise NotImplementedError("Subclasse precisa definir!")
    
    def __enter__(self):
        self.conn = pyodbc.connect(self.connection_string)
        self.cursor = self.conn.cursor()
        print("Conexão criada!")

        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close() if self.cursor else {}
        self.conn.close() if self.conn else {}

        return True
    
    def fetch(self, sql_file:str):
        query = self.read_sql_file(sql_file)

        if not sql_file:
            raise ValueError("Missing query statement")
        
        self.cursor.execute(query)

        rows = self.cursor.fetchall()
        columns = [column[0] for column in self.cursor.description]

        return pd.DataFrame.from_records(rows, columns=columns)
    
    @staticmethod
    def read_sql_file(filename: str):
        if not filename:
            raise ValueError('Provide SQL file name.')

        query_file = os.path.join(os.getcwd(), "queries", f"{filename}.sql")
        with open(query_file) as sql:
            query = sql.read()

        return query

class Mdb(BaseConnection):
    def __init__(self, source_file=MDB_FILE) -> None:
        self.source_file = source_file

    @property
    def connection_string(self):
        return (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            f'DBQ={self.source_file};'
        )