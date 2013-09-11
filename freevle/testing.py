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
        self.app = freevle.app
        self.client = self.app.test_client()

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
        self.assertIsNotNone(self.client)

def run(blueprints=None, exclude=[]):
    """Run all tests, from all blueprints."""
    # We're going to be working with TestSuites here.
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))

    # Find and import testing suites from blueprints.
    if blueprints is None:
        blueprints = os.listdir(freevle.app.config['BLUEPRINTS_DIRECTORY'])

    for bp_name in [bp for bp in blueprints if not bp in exclude]:
        # Try importing test cases from the blueprint. If we can't, that's okay. :(
        try:
            tests = importlib.import_module('freevle.blueprints.{}.tests'\
                                            .format(bp_name))
            bp_suite = tests.suite
            suite.addTest(bp_suite)
        except ImportError as e:
            if len(e.args) and \
               e.args[0] == "No module named 'freevle.blueprints.{}.tests'"\
                            .format(bp_name):
                print("NOTICE: {} blueprint has no test cases.".format(bp_name))
            else:
                raise e

    # And finish it all by running our tests.
    res = unittest.TextTestRunner().run(suite)
    if len(res.failures) > 0:
        sys.exit(1)
