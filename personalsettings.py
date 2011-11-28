# Database settings. If you have no clue what this means, keep it at this.
DATABASE_ENGINE = 'sqlite3'   # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'cygy.sqlite' # Or path to database file if using sqlite3.
DATABASE_USER = ''            # Not used with sqlite3.
DATABASE_PASSWORD = ''        # Not used with sqlite3.
DATABASE_HOST = ''            # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''            # Set to empty string for default. Not used with sqlite3.

ADMINS = (
    ('Your Name', 'yourmail@provider.tld'),
)

# The URL to this instance of CyGy. Just keep it at this for testing.
URL_ROOT = 'localhost:8000/'
# The absolute path to the CyGy directory on your system.
# We do not officially support Windows, but you can try it...
PATH_ROOT = '/absolute/path/to/cygy/'

# Make this unique, and don't share it with anybody.
# Not really needed for development servers. Production? YES.
SECRET_KEY = 'SomethingRandom'

# Wether you want debug options.
DEBUG = True

