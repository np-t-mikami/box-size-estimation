import numpy as np
from src.box_size_estimation import BoxSizeEstimation 

if __name__ == '__main__':
    solver = BoxSizeEstimation()

    ans = solver.estimateXy((720,510,1195),(240,330,495), 0.1)

    print("est:", ans)
    print("ans:", (0.308, 0.170, 0.242))
