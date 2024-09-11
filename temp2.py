import os
import pickle

path = os.path.join(os.getcwd(), "test5")
files = os.listdir(path)

done = 0
for file_ in files:
    with open(os.path.join(path, file_), "rb") as fp:
        a = dict(pickle.load(fp))
        if a["p"] == 0.2475:
            done += a["trials_done"]
print(done)