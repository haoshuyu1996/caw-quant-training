import os
import pandas as pd
import unittest
import check
import sys
data_dir = 'your test data directory'
sys.path.insert(
    1,
    'C:\\Users\\Louphero\\Documents\\GitHub\\caw-quant-training\\section1\\task1')

tests = [('A1', 'A2', 'A3'), ('B1', 'B2', 'B3'), ('c1', 'c2', 'c3')]
testd = [('A1', 'A2', 'A3'), ('B1', 'B2', 'B3'),
         ('C1', 'C2', 'C3'), ('C1', 'C2', 'C3')]
testdiff = [('c1', 'c2', 'c3', 'left_only'), ('C1', 'C2', 'C3', 'right_only')]
testremd = [('A1', 'A2', 'A3'), ('B1', 'B2', 'B3'), ('C1', 'C2', 'C3')]

tests = pd.DataFrame(tests)
testd = pd.DataFrame(testd)
testremd = pd.DataFrame(testremd)
testdiff = pd.DataFrame(testdiff, columns=[0, 1, 2, '_merge'])


class Testcheck(unittest.TestCase):

    def test_remove_duplicate(self):
        data = check.remove_duplicate(testd)
        self.assertTrue((data == testremd).all().all())

    def test_diff(self):
        result = check.diff(testd, tests)
        result = check.remove_duplicate(result)
        result.reset_index(inplace=True, drop=True)
        self.assertTrue((result == testdiff).all().all())


if __name__ == '__main__':
    unittest.main()
