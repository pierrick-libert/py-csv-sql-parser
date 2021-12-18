'''DB connection'''
import sys

from psycopg2 import connect, extensions, OperationalError

from settings.base import DATABASE


class DB:
    '''DB for connections purpose'''
    __connection = None

    # pylint: disable=too-many-arguments
    def __init__(self,
        name: str = DATABASE['NAME'],
        user: str = DATABASE['USER'],
        password: str = DATABASE['PASSWORD'],
        host: str = DATABASE['HOST'],
        port: int = DATABASE['PORT']
    ):
        '''Create the connection to the DB'''
        try:
            self.__connection = connect(
                database=name,
                user=user,
                password=password,
                host=host,
                port=port,
            )
            print("Connection to PostgreSQL DB successful")
        except OperationalError as err:
            print(f"An error occurred while connecting to the DB '{err}'")
            sys.exit(1)


    def __del__(self) -> None:
        '''Close the connection to the DB when the object is destroyed'''
        if self.__connection:
            self.__connection.close()


    def get_conn(self) -> extensions.connection:
        '''Return the connection object'''
        return self.__connection
