'''Unit Test file'''
import unittest

from sqlalchemy_utils import database_exists, drop_database

from settings.base import DATABASE

from utils.models import DB
from utils.utils import BColors, Utils
from utils.data import Data
from utils.specs import Specs


# pylint: disable=unused-variable
class TestProcess(unittest.TestCase):
    '''Unit Test class for the process'''

    __db_obj = None
    __db_uri = f'{DATABASE["URI"]}_test'

    def test_specs_success(self) -> None:
        '''Test the import of successful specs'''
        # Init specs
        specs = Specs(self.__db_obj, 'specs/test/')
        # Test creation and ignore for a big table
        table, created, columns = specs.create_table('specs/test/long.csv')
        self.assertEqual(table.name, 'long')
        table, created, columns = specs.create_table('specs/test/long.csv')
        self.assertEqual(table.name, 'long')
        self.assertEqual(created, False)

        # Test creation for a tricky file
        table, created, columns = specs.create_table('specs/test/tricky.csv')
        self.assertEqual(table.name, 'tricky')

        # Test creation for a normal file
        table, created, columns = specs.create_table('specs/test/normal.csv')
        self.assertEqual(table.name, 'normal')

    def test_specs_error(self) -> None:
        '''Test the import of wrong specs'''
        # Init specs
        specs = Specs(self.__db_obj, 'specs/test/')
        # Test exceptions
        self.assertRaises(Exception, specs.create_table, 'specs/test/exception.csv')
        self.assertRaises(Exception, specs.create_table, 'specs/test/empty.csv')

    def test_data_success(self) -> None:
        '''Test the import of successful data'''
        # Init
        specs = Specs(self.__db_obj, 'specs/test/')

        # Test data for normal file
        table, created, columns = specs.create_table('specs/test/normal.csv')
        data = Data(table, columns, self.__db_obj)
        self.assertEqual(None, data.insert_data('data/test/normal_2021-12-12.txt'))

        # Test data for long file
        table, created, columns = specs.create_table('specs/test/long.csv')
        data = Data(table, columns, self.__db_obj)
        self.assertEqual(None, data.insert_data('data/test/long_2021-12-12.txt'))

        # Test data for tricky file
        table, created, columns = specs.create_table('specs/test/tricky.csv')
        data = Data(table, columns, self.__db_obj)
        self.assertEqual(None, data.insert_data('data/test/tricky_2021-12-12.txt'))

    def test_data_error(self) -> None:
        '''Test the import of wrong data'''
        # Init
        specs = Specs(self.__db_obj, 'specs/test/')
        table, created, columns = specs.create_table('specs/test/normal.csv')
        data = Data(table, columns, self.__db_obj)
        # Test exceptions
        self.assertRaises(Exception, data.insert_data, 'data/test/normal_2021-12-11.txt')
        self.assertRaises(Exception, data.insert_data, 'data/test/normal_2021-10-12.txt')

    @classmethod
    def setUpClass(cls) -> None:
        '''Setup method to create the test database'''
        # Create the Test Database
        cls.__db_obj = DB(uri=cls.__db_uri, verbose=False)
        Utils.display(
            f'{cls.__db_uri[cls.__db_uri.rfind("/") + 1:]} DB Created', BColors.OKGREEN)

    @classmethod
    def tearDownClass(cls) -> None:
        '''Method called after all tests are performed to remove the DB'''
        if database_exists(cls.__db_obj.get_engine().url):
            drop_database(cls.__db_obj.get_engine().url)
            Utils.display(
                f'\n{cls.__db_uri[cls.__db_uri.rfind("/") + 1:]} DB Deleted', BColors.OKGREEN)

if __name__ == '__main__':
    unittest.main()
