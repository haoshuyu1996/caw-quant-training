import os
import sys
import pandas as pd
import unittest
import check

tests = pd.read_csv('BTC_USDT_1h sample.csv')
testd = pd.read_csv('BTC_USDT_1h duplicate.csv')
testc = pd.read_csv('BTC_USDT_1h change.csv')
testdiff = pd.read_csv('BTC_USDT_1h diff.csv')

testdiff

class Testcheck(unittest.TestCase):

    def test_remove_duplicate(self):
        data = check.remove_duplicate(testd)
        self.assertTrue((data == tests).all().all())

    def test_diff(self):
        result = check.diff(testc, tests)
        result = check.remove_duplicate(result)
        result.reset_index(inplace=True, drop=True)
        self.assertTrue((result == testdiff).all().all())


if __name__ == '__main__':
    unittest.main()
