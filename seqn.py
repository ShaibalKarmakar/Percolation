import os 
import numpy as np


import multiprocess_far_point as mfp

p_fine_mesh = [0.2475, 0.2480, 0.2485, 0.2490, 0.2495, 0.2500]
p_sparsh_mesh = [0.20, 0.21, 0.22, 0.23, 0.24, 0.25]
p_long = [0.24, 0.25]
p_ultrafine_mesh = [0.2485, 0.249]
for p in p_ultrafine_mesh:
    mfp.main(p, n_max = 150, trials = 1000, num_processes = 5, test_folder = "test8", mesh_folder = "ultrafine_ultralong2_mesh")