'''Handle specs folder and create table'''
import re

from typing import List, Optional, Union

from psycopg2 import DatabaseError

from .models import DB
from .utils import Utils
from .specs import Column, FileErrorException


class Data:
    '''Class to handle the first part of the project'''
    __db = None

    def __init__(self, table_name: str, columns: List[Column], db_obj: DB):
        '''Save the db connection'''
        self.__db = db_obj
        self.table_name = table_name
        self.columns = columns

    def insert_data(self, file: str) -> str:
        '''Create the table from the file received'''
        errors = []
        # Here parse and create the table
        try:
            # Create a cursor to communicate with the DB
            cursor = self.__db.get_conn().cursor()
            query = f'''INSERT INTO {self.table_name} (
                {",".join([c.get("name") for c in self.columns])}) VALUES '''
            line_length = sum([c.get('size') for c in self.columns])
            # Parse the file
            with open(file, mode='r', encoding='utf-8') as txt_file:
                for idx, line in enumerate(txt_file):
                    # Add space if the line is not long enough, so our regex below can work
                    line = line.rstrip('\n').ljust(line_length)

                    # Automatically split the line based on the specs
                    values = re.findall(''.join(
                        f'(.{{{c.get("size")}}})' for c in self.columns), line
                    )
                    try:
                        # We add the data into the query if we got no error
                        query += self.check_values(values, file, idx)
                    except FileErrorException as error:
                        errors.append(str(error))
                        continue

            # Insert in DB
            cursor.execute(query[:-1], [])
            self.__db.get_conn().commit()
        except (Exception, DatabaseError):
            self.__db.get_conn().rollback()
            raise
        return errors

    # pylint: disable=no-self-use
    def format_value(self, datatype: str, value: str) -> Optional[Union[str, int, bool]]:
        '''Transform the value into the expected data type'''
        value = value.strip()

        if datatype == 'BOOL':
            if Utils.is_integer(value) is False or value not in ['0', '1']:
                return None
            return value == '1'
        if 'INT' in [datatype]:
            return None if Utils.is_integer(value) is False else int(value)

        return f'\'{value}\''


    def check_values(self, values: List[str], file: str, idx: int) -> str:
        '''Check values got from the regex and act accordingly'''
        tmp_query = ''
        # Check basic error
        if len(values) == 0:
            raise FileErrorException(file, idx + 1, 'Incorrect line')
        # Transform data based on the specs
        for val_idx, column in enumerate(self.columns):
            value = self.format_value(column.get('datatype'), values[0][val_idx])
            if value is None:
                raise FileErrorException(
                    file, idx + 1,
                    f'{column.get("name")} is not matching the datatype'
                )
            tmp_query += f'{value},'

        return f'({tmp_query[:-1]}),'
