import numpy as np
from src.box_size_estimation import BoxSizeEstimation 

if __name__ == '__main__':
    solver = BoxSizeEstimation()
    l = 0.1

    # A = [720, 510, 1195]
    # a = [240, 330, 495]
    # dA = [5, 5, 5]
    # da = [5, 5, 5]
    # ans = solver.solveXyPlane(A, a, l)
    # print("solvr:", ans)
    # print("answr:", (0.308, 0.170, 0.242))

    s = 1 # error from image
    A_list = [
#        [58, 87, 100, 27, 30, 45, s, s, s, s, s, s],
        [34, 111, 95, 17, 35, 43, s, s, s, s, s, s],
#        [67, 67.5, 94, 31.5, 23, 42.5, s, s, s, s, s, s]
    ]
    ans = solver.estimate(A_list, l)

    print("statt:", ans)
    print("answer", (0.275, 0.415, 0.215))
