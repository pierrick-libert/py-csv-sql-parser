'''DB connection'''
import sys

from typing import List, Optional, Union

from contextlib import contextmanager

from sqlalchemy import (
    Column, MetaData, Table, create_engine, inspect, insert
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.types import (
    Text, String, Boolean,
    SmallInteger, Integer, BigInteger
)
from sqlalchemy.schema import CreateTable
from sqlalchemy.engine import Engine
from sqlalchemy_utils import database_exists, create_database

from settings.base import DATABASE

from models.migration import Migration


class DB:
    '''DB for connections purpose'''
    dry_run = False
    __engine = None

    # pylint: disable=too-many-arguments
    def __init__(self,
        uri: str = DATABASE['URI'],
        dry_run: bool = False,
        verbose: bool = True,
    ):
        '''Create the connection to the DB'''
        try:
            self.dry_run = dry_run
            self.__engine = create_engine(uri, echo = verbose)
            if not database_exists(self.__engine.url):
                create_database(self.__engine.url)
        except SQLAlchemyError as error:
            print(f'An error occurred while connecting to the DB; {error}')
            sys.exit(1)

    @contextmanager
    # pylint: disable=unused-argument
    def get_session(self, *args, **kwargs) -> Session:
        '''Create a session for handling transactions'''
        session = Session(self.__engine)
        try:
            yield session
        except:
            session.rollback()
            raise
        else:
            if self.dry_run is True:
                return
            session.commit()

    def get_engine(self) -> Engine:
        '''Return the engine object created in the constructor'''
        return self.__engine

    def create_table(self, columns: List[Column], table_name: str) -> Union[Table, bool]:
        '''Create the table based on parameters'''
        table = Table(table_name, MetaData(), *columns)
        if inspect(self.__engine).has_table(table_name):
            return table, False

        with self.get_session() as session:
            # Create the table
            table_creation_sql = CreateTable(table)
            session.execute(table_creation_sql)
        return table, True

    def create_table_from_model(self, model) -> Union[Table, bool]:
        '''Create the table based on parameters'''
        if inspect(self.__engine).has_table(model.__table__.name):
            return model.__table__, False

        with self.get_session() as session:
            # Create the table
            table_creation_sql = CreateTable(model.__table__)
            session.execute(table_creation_sql)
        return model.__table__, True

    def bulk_insert(self, table: Table, values: List) -> None:
        '''Bulk insert data in a specific table'''
        with self.get_session() as session:
            session.execute(insert(table, values))

    def has_migration(self, filename: str) -> bool:
        '''Check if a migration exists or not'''
        with self.get_session() as session:
            result = session.query(Migration).filter_by(filename=filename).count()
            if result > 0:
                return True
        return False

    # pylint: disable=no-self-use
    def define_column_type(self, name: str, size: int, datatype: str) -> Optional[Column]:
        '''Return the column type based on datatype'''
        column = None
        if datatype in ['boolean', 'bool']:
            column = Column(name, Boolean)
        if datatype in ['integer', 'int']:
            if size < 5:
                column = Column(name, SmallInteger)
            elif size < 10:
                column = Column(name, Integer)
            else:
                column = Column(name, BigInteger)
        if datatype in ['text', 'varchar', 'char', 'str', 'string']:
            if size > (10 * 1024 * 1024):
                column = Column(name, Text)
            else:
                column = Column(name, String(size))
        return column
