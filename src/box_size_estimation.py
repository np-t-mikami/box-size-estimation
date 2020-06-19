import numpy as np
from scipy import optimize

class BoxSizeEstimation:
    """ Algorithms and statistical tools 
    for estimating edge lengths of rectangular boxes from its picture image.
    """

    def solveXyPlane(self, boxEdgeLengthsPx, refEdgeLengthsPx, refLengthMeter):
        """ Using pictures taken inside the XOY plane. (See: doc/explanation-estimateXy.pdf) 
        
        Args:
            boxEdgeLengthsPx: (OA, OB, OC) in pixels 
            refEdgeLengthsPx: (Oa, Ob, Oc) in pixels
            refLengthMeter: actual reference length in meter
        
        Returns:
            (OX, OY, OZ, SO) in meter
        """

        a, b, c = refEdgeLengthsPx
        A, B, C = boxEdgeLengthsPx
        L = refLengthMeter
        
        def fn(x):
            _v, _theta = x
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


    def estimate(self, edgeLengthsPxList, refLengthMeter, solver="xy-plane", numTrialPerInput = 200):
        """ Estimation based on Monte-Carlo algorithm

        Args:
            edgeLengthsPxList : list of
                OA, OB, OC,
                Oa, Ob, Oc,
                sigma(OA), sigma(OB), sigma(OC),
                sigma(Oa), sigma(Ob), sigma(Oc)
                in pixels

            refLengthMeter (float) : actual reference length in meter

            solver (str) : "xy-plane" only.
        
        Returns:
            (OX, OY, OZ, sigma(OX), sigma(OY), sigma(OZ))  in meter.

        """

        accumLengths = np.zeros(3,dtype=float)
        accumSquareLengths = np.zeros(3,dtype=float)
        accumNum = 0


        # currently, we have "xy-plane" solver only
        solverFn = self.solveXyPlane


        for lengths in edgeLengthsPxList:
            A = np.array(lengths[0:3])
            a = np.array(lengths[3:6])
            dA = np.array(lengths[6:9])
            da = np.array(lengths[9:12])

            for _ in range(numTrialPerInput):
                boxEdgeLengths = np.random.default_rng().normal(A, dA)
                refEdgeLengths = np.random.default_rng().normal(a, da)

                try:
                    _X, _Y, _Z, _ = solverFn(boxEdgeLengths, refEdgeLengths, refLengthMeter)
                
                    _E = np.array([_X, _Y, _Z])
                    accumLengths += _E
                    accumSquareLengths += _E**2
                    accumNum += 1
                except: 
                    print("error for", boxEdgeLengths, refEdgeLengths, refLengthMeter)
        
        X = accumLengths / accumNum
        dX = np.sqrt( accumSquareLengths / accumNum - X**2)

        return (X[0], X[1], X[2], dX[0], dX[1], dX[2])


