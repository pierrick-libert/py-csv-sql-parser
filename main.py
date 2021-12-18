'''Entrypoint of the application'''
import glob

from psycopg2 import DatabaseError

from utils.data import Data
from utils.models import DB
from utils.specs import Specs, FileErrorException


# pylint: disable=broad-except
def main() -> None:
    '''Launch the process to create table and fill them'''
    db_obj = DB()

    specs = Specs(db_obj)
    # Start by looping on the specs folder
    for file in glob.glob('specs/*.csv'):
        # Create the table in DB
        try:
            table_name, columns = specs.create_table(file)
        except (Exception, DatabaseError, FileErrorException) as error:
            print(error)
            continue

        # Insert the data inside the table
        data = Data(table_name, columns, db_obj)
        for data_file in glob.glob(f'data/{table_name}_*.txt'):
            try:
                errors = data.insert_data(data_file)
                if len(errors) > 0:
                    print('Error(s) occurred during the process, other data has been inserted')
                    for error in errors:
                        print(error)
            except (Exception, DatabaseError) as error:
                print(error)
                continue

if __name__ == '__main__':
    main()
