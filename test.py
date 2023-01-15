import unittest
import sys
from io import StringIO
from csvCombiner import main
import pandas as pd

class TestCSVCombiner(unittest.TestCase):

    def test_empty_file(self):
        # check if empty files are handled correctly
        # https://stackoverflow.com/questions/33767627/python-write-unittest-for-console-print
        sys.argv = ['csvCombiner.py', 'clothing.csv', 'empty.csv']
        captured_output = StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__
        self.assertIn("empty.csv does not exist or is empty", captured_output.getvalue())

    def test_missing_file(self):
        # check if missing files are handled correctly
        sys.argv = ['csvCombiner.py', 'clothing.csv', 'fakename.csv']
        captured_output = StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__
        self.assertIn("fakename.csv does not exist or is empty", captured_output.getvalue())

    def test_merge(self):
        # Test that the merging of files is done correctly
        sys.argv = ['csvCombiner.py', 'accessories.csv', 'clothing.csv','household_cleaners.csv']
        main()
        length1 = len(pd.read_csv("fixtures/accessories.csv"))
        length2 = len(pd.read_csv("fixtures/clothing.csv"))
        length3 = len(pd.read_csv("fixtures/household_cleaners.csv"))
        result = pd.read_csv("out/combined.csv")
        self.assertEqual(length1+length2+length3, len(result)) #check if number of rows are correct
        self.assertEqual(result.shape[1],3) #check if number of columns are correct

    def test_diff_num_cols(self):
        # Test that the merging of files is done correctly when # of columns differs
        sys.argv = ['csvCombiner.py', 'accessories.csv','extraCol.csv']
        main()
        length1 = len(pd.read_csv("fixtures/accessories.csv"))
        length2 = len(pd.read_csv("fixtures/extraCol.csv"))
        result = pd.read_csv("out/combined.csv")

        self.assertEqual(length1+length2, len(result)) #check if number of rows are correct
        self.assertEqual(result.shape[1],4) #check if number of columns are correct

    def test_no_args(self):
        # test if no arguments passed in 
        sys.argv = ['csvCombiner.py']
        captured_output = StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__
        self.assertIn("No files were read.", captured_output.getvalue())


if __name__ == '__main__':
    unittest.main()
