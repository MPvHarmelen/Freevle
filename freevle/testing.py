import sys, os
import importlib
import tempfile
import unittest
import freevle

class TestBase(unittest.TestCase):
    def setUp(self):
        # Create a temporary database file (sqlite3).
        if freevle.app.config.get('UGLY_TEST_WORKAROUND', False):
            self.db_path = 'C:\\tempfileforsqlalchemy'
            self.db_fd = open(self.db_path, 'w')
        else:
            self.db_fd, self.db_path = tempfile.mkstemp()
        freevle.app.config['SQLALCHEMY_DATABASE_URI'] = \
                'sqlite:///' + self.db_path

        # Set up a testing Flask app.
        freevle.app.config['TESTING'] = True
        self.app = freevle.app.test_client()

        # And finally create the database.
        freevle.db.create_all()

    def tearDown(self):
        freevle.db.session.close_all()
        if freevle.app.config.get('UGLY_TEST_WORKAROUND', False):
            self.db_fd.close()
        else:
            os.close(self.db_fd)
        os.unlink(self.db_path)

class TestSetup(TestBase):
    def test_setup(self):
        self.assertIsNotNone(self.app)

def run():
    """Run all tests, from all apps."""
    # We're going to be working with TestSuites here.
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))

    # Find and import testing suites from blueprints.
    apps = os.listdir(freevle.app.config['APPS_DIRECTORY'])
    for app_name in apps:
        # Try importing test cases from the app. If we can't, that's okay. :(
        try:
            tests = importlib.import_module('freevle.apps.{}.tests'\
                                            .format(app_name))
            app_suite = tests.suite
            suite.addTest(app_suite)
        except ImportError as e:
            if len(e.args) and \
               e.args[0] == "No module named 'freevle.apps.{}.tests'"\
                            .format(app_name):
                print("NOTICE: {} app has no test cases.".format(app_name))
            else:
                raise e

    # And finish it all by running our tests.
    res = unittest.TextTestRunner().run(suite)
    if len(res.failures) > 0:
        sys.exit(1)
