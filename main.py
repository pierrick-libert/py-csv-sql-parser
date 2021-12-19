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
    db_obj = DB(dry_run=dry_run)
    migration_table, created = db_obj.create_table_from_model(Migration())

    # Treat specifications
    specs = Specs(db_obj)
    # Start by looping on the specs folder
    for file in glob.glob('specs/*.csv'):
        # Create the table in DB
        try:
            table, created, columns = specs.create_table(file)
            txt = f'{BColors.BOLD}{BColors.OKCYAN}{file}\'s table already existed'
            if created is True:
                txt = f'{BColors.BOLD}{BColors.OKGREEN}{file}\'s table has been created'
            print(f'{txt}{BColors.ENDC}')
        except (Exception, SQLAlchemyError, FileErrorException) as error:
            print(f'{BColors.BOLD}{BColors.FAIL}{str(error)[1:]}{BColors.ENDC}\n')
            continue

        # Insert the data inside the table
        data = Data(table, columns, db_obj)
        for data_file in glob.glob(f'data/{table.name}_*.txt'):
            try:
                # Check if we already pass the migration to not insert data twice
                if db_obj.has_migration(data_file) is True:
                    txt = f'{BColors.BOLD}{BColors.OKCYAN}{data_file}'
                    print(f'{txt} has already been migrated{BColors.ENDC}\n')
                    continue
                # Insert the data for the file and the migration
                data.insert_data(data_file)
                db_obj.bulk_insert(migration_table, [{'filename': data_file}])
                txt = f'{BColors.BOLD}{BColors.OKGREEN}{data_file}\'s data has been inserted'
                print(f'{txt}{BColors.ENDC}\n')
            except (Exception, SQLAlchemyError) as error:
                print(f'{BColors.BOLD}{BColors.FAIL}{str(error)[1:]}{BColors.ENDC}\n')
                continue

if __name__ == '__main__':
    main('--dry-run' in sys.argv)
