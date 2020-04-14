from _cihub.db import initialize_database
from _cihub.db import install_example_data
from _cihub.db import wipe_older_than
from _cihub.cihub import app
import argparse
import sys
import uvicorn


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="CIHub - aggregates status of CI systems")
    parser.add_argument(
        '--init-db', help='Initialize the database and quit.',
        action='store_true')
    parser.add_argument(
        '--example-data', help='Put example data into the database and quit.',
        action='store_true')
    parser.add_argument(
        '--wipe-older-than',
        help=(
            'Wipe entries from database which are older than the given number'
            ' of days.'),
        action='store',
        type=int)
    parser.add_argument(
        '--debug', help='Start in debug mode - do not use in production.',
        action='store_true')
    args = parser.parse_args()

    if args.init_db:
        initialize_database()
        print('Initialized database.')
        sys.exit(0)
    elif args.example_data:
        install_example_data()
        print('Put example data into database')
        sys.exit(0)
    elif args.wipe_older_than:
        deleted = wipe_older_than(args.wipe_older_than)
        print(f'Removed {deleted} DB entries older'
              f' than {args.wipe_older_than} days.')
        sys.exit(0)
    if args.debug:
        app.debug = True

    uvicorn.run(app, host='0.0.0.0', port=8000)
