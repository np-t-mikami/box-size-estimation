import unittest
import numpy as np
from src.box_size_estimation import BoxSizeEstimation 

class TestEstimateXy(unittest.TestCase):

    def test_45degBox(self):

        classUnderTest = BoxSizeEstimation()
        
        # actual 
        L = 0.1
        v = 1.0
        X = 0.5
        w = 0.4
        Z = 0.5

        a = w * L / (L + np.sqrt(2)*v)
        A = w * X / (X + np.sqrt(2)*v)

        c = w * L / v
        C = w * Z / v

        ref = (a,a,c)
        box = (A,A,C)

        actual = classUnderTest.estimateXy(box, ref, L)

        # expect
        expect = (X, X, Z, v)

        # assert
        for i in range(4):
            self.assertAlmostEquals(actual[i], expect[i])
        

if __name__ == '__main__':
    unittest.main()