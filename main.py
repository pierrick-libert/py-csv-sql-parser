'''Entrypoint of the application'''
import sys
import glob

from sqlalchemy.exc import SQLAlchemyError

from utils.data import Data
from utils.models import DB
from utils.utils import BColors
from utils.specs import Specs, FileErrorException

from models.migration import Migration


# pylint: disable=broad-except
def main(dry_run: bool) -> None:
    '''Launch the process to create table and fill them'''
    # Instantiate the DB and create the migration table
    db_obj = DB(dry_run)
    migration_table = db_obj.create_table_from_model(Migration())

    # Treat specifications
    specs = Specs(db_obj)
    # Start by looping on the specs folder
    for file in glob.glob('specs/*.csv'):
        # Create the table in DB
        try:
            table, columns = specs.create_table(file)
        except (Exception, SQLAlchemyError, FileErrorException) as error:
            print(f'{BColors.BOLD}{BColors.FAIL}{error}{BColors.ENDC}')
            continue

        # Insert the data inside the table
        data = Data(table, columns, db_obj)
        for data_file in glob.glob(f'data/{table.name}_*.txt'):
            try:
                # Check if we already pass the migration to not insert data twice
                if db_obj.has_migration(data_file) is True:
                    txt = f'{BColors.BOLD}{BColors.OKCYAN}{data_file} '
                    print(f'{txt} has already been migrated{BColors.ENDC}')
                    continue
                errors = data.insert_data(data_file)
                if len(errors) > 0:
                    print(f'{BColors.FAIL}Error(s) occurred during the process:{BColors.ENDC}')
                    for error in errors:
                        print(f'{BColors.BOLD}{BColors.FAIL}   {error}{BColors.ENDC}')
                else:
                    db_obj.bulk_insert(migration_table, [{'filename': data_file}])
            except (Exception, SQLAlchemyError) as error:
                print(f'{BColors.BOLD}{BColors.FAIL}{error}{BColors.ENDC}')
                continue

if __name__ == '__main__':
    main('--dry-run' in sys.argv)
