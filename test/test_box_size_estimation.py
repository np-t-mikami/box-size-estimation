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

        actual = classUnderTest.solveXyPlane(box, ref, L)

        # expect
        expect = (X, X, Z, v)

        # assert
        for i in range(4):
            self.assertAlmostEqual(expect[i], actual[i])
    
    def test_errorEstimation(self):

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

        ref = [a,a,c]
        box = [A,A,C]
        stds = [1E-10]*6
        actual = classUnderTest.estimate([box + ref + stds], L, 1000)

        # expect
        expect = (X, X, Z)

        # assert
        for i in range(3):
            self.assertAlmostEqual(expect[i], actual[i], delta=0.2)        

if __name__ == '__main__':
    unittest.main()