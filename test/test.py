import unittest
from dlogging import dlogging
import time


class MyTest(unittest.TestCase):
    def setUp(self):
        pass

    def test(self):
        t = 10
        for i in range(t):
            self.test_iter(i)
            time.sleep(60)

    def test_iter(self, n):
        dlogging.basicConfig("test", level=dlogging.DEBUG)
        dlogging.info("test {} is starting".format(n))
        dlogging.debug("test {} debug message".format(n))
        dlogging.warning("test {} warning from the test".format(n))
        dlogging.debug("test {} debug message 2".format(n))
        dlogging.error("test {} error in the test".format(n))
        dlogging.debug("test {} debug message 3".format(n))
        dlogging.critical("test {} critical error in the test".format(n))
        dlogging.info("test {} is finished".format(n))


    def tearDown(self):
        pass
