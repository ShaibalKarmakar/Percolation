import os
import pickle
from upload_files_to_github import upload_files_to_github

filepath = os.path.join(os.getcwd(), "fine_mesh")
files = os.listdir(filepath)
#filenames = [os.path.join(filepath, filename) for filename in files if filename[-3:]=="png"]
#filenames = [os.path.join(os.getcwd(), "fine_mesh.zip")]
filenames = [os.path.join(os.getcwd(), "test_text.txt")]
repo = "pecacio/Percolation"
token = "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"
upload_files_to_github(filenames, repo, token, branch = 'main')
