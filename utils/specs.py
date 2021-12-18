'''Handle specs folder and create table'''
import re
import csv

from typing import List, Optional, TypedDict

from psycopg2 import DatabaseError

from .models import DB
from .utils import Utils


class FileErrorException(Exception):
    '''Custom Exception for specs file parsing'''
    def __init__(self, file: str, idx: int, message: str ="Unexpected Error"):
        self.file = file
        self.idx = idx
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'In file "{self.file}", line {self.idx}: {self.message}'


class Column(TypedDict):
    '''Type dict for column'''
    name: str
    size: int
    datatype: str


class Specs:
    '''Class to handle the first part of the project'''
    __db = None

    def __init__(self, db_obj: DB):
        '''Save the db connection'''
        self.__db = db_obj

    def create_table(self, file: str) -> List[Column]:
        '''Create the table from the file received'''
        try:
            table_name = re.search('specs/(.+?).csv', file).group(1)
        except AttributeError as error:
            raise Exception(error) from error

        columns = []
        # Here parse and create the table
        try:
            # Create a cursor to communicate with the DB
            cursor = self.__db.get_conn().cursor()
            query = f'CREATE TABLE IF NOT EXISTS {table_name} ('

            # Parse the file
            with open(file, mode='r', encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                # By pass header
                next(csv_reader)
                # Start to retrieve data from the file
                for idx, row in enumerate(csv_reader):
                    # Check the right amount of columns
                    if len(row) != 3:
                        raise FileErrorException(file, idx + 2, '3 columns are required')

                    # Check if the size is an integer
                    if Utils.is_integer(row[1]) is False:
                        raise FileErrorException(file, idx + 2, 'Width must be an integer')
                    # Proceed to small modifications on the data to avoid easy mistake
                    column = re.sub(r'[-\t\s]+', '_', row[0].strip().lower())
                    size = int(row[1].strip())
                    datatype = row[2].strip().lower()

                    # Check if the size if inferior to 1
                    if size < 1:
                        raise FileErrorException(file, idx + 2, 'Width must be a positive integer')

                    # Check if we don't have any error in the type
                    row_type = self.define_row_type(size, datatype)
                    if row_type is None:
                        raise FileErrorException(file, idx + 2, 'Unknown datatype')

                    # Dynamically create the query
                    query += f'{column} {row_type} NOT NULL,'
                    columns.append({'name': column, 'size': size, 'datatype': row_type})

            query = f'{query[:-1]})'
            cursor.execute(query, [])
            self.__db.get_conn().commit()

        except (Exception, DatabaseError, FileErrorException):
            self.__db.get_conn().rollback()
            raise
        return table_name, columns

    # pylint: disable=no-self-use
    def define_row_type(self, size: int, datatype: str) -> Optional[str]:
        '''Define the row type based on datatype'''
        if datatype in ['boolean', 'bool']:
            return 'BOOL'
        if datatype in ['integer', 'int']:
            if size < 5:
                return 'SMALLINT'
            if size < 10:
                return 'INTEGER'
            return 'BIGINT'
        if datatype in ['text', 'varchar', 'char', 'str', 'string']:
            if size > (10 * 1024 * 1024):
                return 'TEXT'
            return f'VARCHAR({size})'
        return None
