import pandas as pd
import numpy as np
import unittest as ut
from pandas.testing import assert_frame_equal

from removeFaultyData import CleanData

class TestCleaner(ut.TestCase):
    def test1(self):
        #test that dataframe is not modified in case of no errors in data
        clean = pd.DataFrame([['x',10.0,15.0,20.0],['y',3.0,6.0,9.0]],columns=['a','b','c','d'])
        dirty = pd.DataFrame([['x',10.0,15.0,20.0],['y',3.0,6.0,9.0]],columns=['a','b','c','d'])

        result = CleanData.preClean(dirty)

        assert_frame_equal(clean,result)

    def test2(self):
        #test for dropping repeat rows
        clean = pd.DataFrame([['x',10.0,15.0,20.0],['y',3.0,6.0,9.0],['z',3.0,6.0,9.0]],columns=['a','b','c','d'])
        dirty = pd.DataFrame([['x',10.0,15.0,20.0],['y',3.0,6.0,9.0],['x',10.0,15.0,20.0],['z',3.0,6.0,9.0]],columns=['a','b','c','d'])

        result = CleanData.preClean(dirty)

        assert_frame_equal(clean,result)

    def test3(self):
        clean = pd.DataFrame([['x',10.0,0.0,20.0],['y',3.0,6.0,9.0],['z',0.0,6.0,9.0]],columns=['a','b','c','d'])
        dirty = pd.DataFrame([['x',10.0,np.nan,20.0],['y',3.0,6.0,9.0],['z',np.nan,6.0,9.0]],columns=['a','b','c','d'])

        result = CleanData.preClean(dirty)

        assert_frame_equal(clean,result)

if __name__ == '__main__':
    ut.main()
