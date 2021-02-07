# Change file name to 'production.py'.

import os

__PRODUCTION_ENVIRONMENT_VARIABLES = {
    # Add your keys here.
    
    'DJANGO_SECRET_KEY': '',
}


def add_variables():
    for variable in __PRODUCTION_ENVIRONMENT_VARIABLES:
        os.environ[variable] = __PRODUCTION_ENVIRONMENT_VARIABLES[variable]