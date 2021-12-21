'''Handle specs folder and create table'''
import re
import csv

from typing import List, TypedDict

from sqlalchemy.exc import SQLAlchemyError

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


class CustomColumn(TypedDict):
    '''Type dict for column'''
    name: str
    size: int
    datatype: str


# pylint: disable=too-few-public-methods
class Specs:
    '''Class to handle the first part of the project'''
    __db = None
    prefix = ''

    def __init__(self, db_obj: DB, prefix: str = 'specs/'):
        '''Save the db connection'''
        self.__db = db_obj
        self.prefix = prefix

    # pylint: disable=too-many-locals
    def create_table(self, file: str) -> List[CustomColumn]:
        '''Create the table from the file received'''
        table_name: str = re.search(f'{self.prefix}(.+?).csv', file).group(1)

        columns = []
        custom_columns = []
        # Parse the file
        error_txt = ''
        with open(file, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            # By pass header
            next(csv_reader)
            # Start to retrieve data from the file
            for idx, row in enumerate(csv_reader):
                try:
                    # Check the right amount of columns
                    if len(row) != 3:
                        raise FileErrorException(file, idx + 2, '3 columns are required')

                    # Check if the size is an integer
                    if Utils.is_integer(row[1]) is False:
                        raise FileErrorException(file, idx + 2, 'Width must be an integer')
                    # Proceed to small modifications on the data to avoid easy mistake
                    name = re.sub(r'[\W]+', '_', row[0].strip().lower())
                    size = int(row[1].strip())
                    datatype = row[2].strip().lower()

                    # Check if the size if inferior to 1
                    if size < 1:
                        raise FileErrorException(file, idx + 2, 'Width must be a positive integer')

                    # Check if we don't have any error in the type
                    column = self.__db.define_column_type(name, size, datatype)
                    if column is None:
                        raise FileErrorException(file, idx + 2, 'Unknown datatype')
                    columns.append(column)
                    custom_columns.append({
                        'name': name, 'size': size, 'datatype': str(column.type)})
                except FileErrorException as error:
                    error_txt = f'{error_txt}\n{str(error)}'
                    continue

        # Create the table if it doesn't exist
        if len(error_txt) != 0:
            raise Exception(error_txt)
        if len(columns) == 0:
            raise FileErrorException(file, 1, 'Empty file')

        table, created = self.__db.create_table(columns, table_name)
        return table, created, custom_columns
