import os
import numpy as np

import pickle
import statsmodels.api as sm


with open(os.path.join(os.getcwd(), "all_record", "record.pkl"), "rb") as fp:
    data = dict(pickle.load(fp))

