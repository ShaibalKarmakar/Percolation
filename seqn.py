import os 
import numpy as np


import multiprocess_far_point as mfp

p_fine_mesh = [0.2475, 0.2480, 0.2485, 0.2490, 0.2495, 0.2500]
p_sparsh_mesh = [0.20, 0.21, 0.22, 0.23, 0.24, 0.25]
p_long = [0.24, 0.25]
for p in p_fine_mesh[:-1]:
    p = 0.2495
    mfp.main(p, n_max = 100, test_folder = "test6", mesh_folder = "fine_ultralong_mesh")
    break