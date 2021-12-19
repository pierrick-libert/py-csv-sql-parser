'''Handle specs folder and create table'''
import re

from typing import List, Optional, Union

from sqlalchemy import Table
from sqlalchemy.exc import SQLAlchemyError

from .models import DB
from .utils import Utils
from .specs import CustomColumn, FileErrorException


class Data:
    '''Class to handle the first part of the project'''
    __db = None

    def __init__(self, table: Table, columns: List[CustomColumn], db_obj: DB):
        '''Save the db connection'''
        self.__db = db_obj
        self.table = table
        self.errors = []
        self.columns = columns

    def insert_data(self, file: str) -> str:
        '''Create the table from the file received'''
        # Here parse and create the table
        try:
            data = []
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
                        data.append(self.check_values(values, file, idx))
                    except FileErrorException as error:
                        self.errors.append(str(error))
                        continue
            # Insert data if we're got no error
            if len(self.errors) == 0:
                self.__db.bulk_insert(self.table, data)
        except (Exception, SQLAlchemyError) as error:
            raise Exception(error) from error
        return self.errors

    # pylint: disable=no-self-use
    def format_value(self, datatype: str, value: str) -> Optional[Union[str, int, bool]]:
        '''Transform the value into the expected data type'''
        value = value.strip()
        if datatype == 'BOOLEAN':
            if Utils.is_integer(value) is False or value not in ['0', '1']:
                return None
            return value == '1'
        if 'INT' in [datatype]:
            return None if Utils.is_integer(value) is False else int(value)

        return value

    def check_values(self, values: List[str], file: str, idx: int) -> str:
        '''Check values got from the regex and act accordingly'''
        value = {}
        # Check basic error
        if len(values) == 0:
            raise FileErrorException(file, idx + 1, 'Incorrect line')
        # Transform data based on the specs
        for val_idx, column in enumerate(self.columns):
            tmp_value = self.format_value(column.get('datatype'), values[0][val_idx])
            if tmp_value is None:
                raise FileErrorException(
                    file, idx + 1,
                    f'{column.get("name")} is not matching the datatype'
                )
            value[column.get('name')] = tmp_value

        return value
