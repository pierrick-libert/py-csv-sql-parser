'''Entrypoint of the application'''
import sys
import glob

from sqlalchemy.exc import SQLAlchemyError

from utils.data import Data
from utils.models import DB
from utils.utils import Utils, BColors
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
            if created is True:
                Utils.display(f'{file}\'s table has been created', BColors.OKGREEN)
            else:
                Utils.display(f'{file}\'s table already existed', BColors.OKCYAN)
        except (Exception, SQLAlchemyError, FileErrorException) as error:
            Utils.display(f'{str(error)[1:]}\n', BColors.FAIL)
            continue

        # Insert the data inside the table
        data = Data(table, columns, db_obj)
        for data_file in glob.glob(f'data/{table.name}_*.txt'):
            try:
                # Check if we already pass the migration to not insert data twice
                if db_obj.has_migration(data_file) is True:
                    Utils.display(f'{data_file} has already been migrated\n', BColors.OKCYAN)
                    continue
                # Insert the data for the file and the migration
                data.insert_data(data_file)
                if dry_run is False:
                    db_obj.bulk_insert(migration_table, [{'filename': data_file}])
                # Print information
                Utils.display(f'{data_file}\'s data has been inserted\n', BColors.OKGREEN)
            except (Exception, SQLAlchemyError) as error:
                Utils.display(f'{str(error)[1:]}\n', BColors.FAIL)
                continue

if __name__ == '__main__':
    main('--dry-run' in sys.argv)
