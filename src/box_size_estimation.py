import numpy as np
from scipy import optimize

class BoxSizeEstimation:

    def estimateXy(self, boxEdgeLengthsPx, refEdgeLengthsPx, refLengthMeter):
        """
        param:
            boxEdgeLengthPx: (OA, OB, OC) in pixels 
            refEdgeLengthPx: (Oa, Ob, Oc) in pixels
            refLengthMeter: actual refelence length in meter
        return:
            (OX, OY, OZ, SO) in meter
        """
        a, b, c = refEdgeLengthsPx
        A, B, C = boxEdgeLengthsPx
        L = refLengthMeter
        
        def fn(x):
            _v = x[0]
            _theta = x[1]
            return [
                (c*_v/b)*np.sin(_theta) - (_v + L*np.cos(_theta)),
                (c*_v/a)*np.cos(_theta) - (_v + L*np.sin(_theta)) 
            ]

        res = optimize.root(fn, [10*L, np.pi/4 ], method="broyden1")

        if not res.success:
            raise Exception("Solution not found.")

        v, theta = res.x
        w = c*v/L

        X = v/np.sin(theta)/(w/A - np.tan(theta))
        Y = v/np.cos(theta)/(w/B - 1/np.tan(theta))
        Z = v*C/w

        return (X, Y, Z, v)


