import os
import importlib
import tempfile
import unittest
import freevle

class TestBase(object):
    def setUp(self):
        # Create a temporary database file (sqlite3).
        self.db_fd, self.db_path = tempfile.mkstemp()
        freevle.app.config['SQLALCHEMY_DATABASE_URI'] = \
                'sqlite:///' + self.db_path

        # Set up a testing Flask app.
        freevle.app.config['TESTING'] = True
        self.app = freevle.app.test_client()

        # And finally create the database.
        freevle.db.create_all()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)

class TestSetup(TestBase, unittest.TestCase):
    def test_setup(self):
        assert self.app is not None

if __name__ == '__main__':
    # We're going to be working with TestSuites here.
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))

    # Find and import testing suites from blueprints.
    apps = os.listdir(freevle.app.config['APPS_DIRECTORY'])
    for app_name in apps:
        app = importlib.import_module('freevle.apps.' + app_name)
        # App imported, let's see if it has a testing suite.
        try:
            suite = app.tests.suite
            suite.addTest(suite)
        except AttributeError:
            print("NOTICE: {} app has no test cases.".format(app_name))

    # And finish it all by running our tests.
    unittest.main()
