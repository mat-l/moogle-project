#!/usr/bin/env python

import sys
from os import environ
from os.path import join, normpath


if __name__ == '__main__':
    # TODO use argparse
    # See https://github.com/united-academics/uarepocamp/blob/master/campaign/scripts/send_bulk_email2.py

    if sys.argv[1] == 'syncdb':
        """
        Setup the SQLAlchemy db as configured in the settings.
        """
        from crawlers.dbutils import setup_db
        setup_db()

    elif sys.argv[1] == 'loaddata':
        """
        Load a fixture into the database.
        """
        from crawlers.dbutils import loaddata
        path = normpath(join(environ['PWD'], sys.argv[2]))
        loaddata(path)

    elif sys.argv[1] == 'shell':
        """
        Start a debug shell and automatically imports the models.
        """
        # TODO it should import from all models.py in all packages

        from crawlers.dbutils import Session, get_all_models_classes

        # Import all models
        models_names = []
        for cls in get_all_models_classes():
            model_name = cls.__name__
            models_names.append(model_name)
            globals()[model_name] = getattr(
                __import__('crawlers.models', fromlist=[model_name]), model_name)

        # Create a new session
        sex = Session()

        # Print some info
        print('')
        print("The following models have been loaded:\n{}".format(models_names))
        print("A session has been open with name `sex`.")
        print("You can run a query like:\n    sex.query({}).all()".format(models_names[0]))
        print('')

        # Start a debug session
        # Try import bpdb (which requires Bpython), if not import plain pdb
        try:
            import bpdb as debug
        except:
            import pdb
        debug.set_trace()
