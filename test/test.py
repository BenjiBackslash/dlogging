import unittest
from dlogging import dlogging


class MyTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_(self):
        dlogging.basicConfig("test", level=dlogging.INFO)
        dlogging.debug("test is starting")
        dlogging.debug("debug message")
        dlogging.warning("warning from the test")
        dlogging.debug("debug message 2")
        dlogging.error("error in the test")
        dlogging.debug("debug message 3")
        dlogging.critical("critical error in the test")
        dlogging.info("test is finished")

    def tearDown(self):
        pass
