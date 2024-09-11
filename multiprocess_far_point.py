import os
import random
import numpy as np
import pickle
import time
import multiprocessing
from tqdm import tqdm


class Graph:
    def __init__(self, n=10):
        self.n = n
        x_range = np.arange(-n, n+1)
        self.vertices = []
        for i in x_range:
            for j in x_range:
                for k in x_range:
                    self.vertices.append((i,j,k))
        # self.vertices = list(combinations_with_replacement(x_range, r = 3))
        self.vertex_dict = dict(zip(self.vertices, range(len(self.vertices))))
        self.to_vertex_dict = dict(zip(range(len(self.vertices)), self.vertices))
        # print(self.vertex_dict)
    
    def adj_dict(self, p):
        adj_dict = {}
        # initialize dict
        for vertex in self.vertices: adj_dict[self.vertex_dict[vertex]] = []

        for vertex in self.vertices:
            x,y,z = vertex
            # print(vertex)
            nbrs = [(x-1,y,z), (x+1, y, z), (x,y-1,z), (x,y+1,z), (x,y,z-1), (x,y,z+1)]
            for nbr in nbrs:
                a,b,c = nbr
                if max(abs(a), abs(b), abs(c)) <= self.n:
                    if random.random() <= p:
                        adj_dict[self.vertex_dict[vertex]].append(self.vertex_dict[nbr])
                        # adj_dict[self.vertex_dict[nbr]].append(self.vertex_dict[vertex])
        return adj_dict
    
    def dfs(self, adj_dict):
        start = self.vertex_dict[(0,0,0)]
        visited = set()
        stack = [start]
        max_dist = 0
        while stack:
            vertex = stack.pop()
            if vertex in visited:
                continue
            visited.add(vertex)
            for nbr in adj_dict[vertex]:
                stack.append(nbr)
                a,b,c = self.to_vertex_dict[nbr]
                max_dist = max(max_dist, abs(a), abs(b), abs(c))
                if max_dist >= self.n:
                    return max_dist
        return max_dist

def process_far_point(p, n_max, trials, filepath, process_id):
    
    new_filepath = f"{filepath}_{process_id}.pkl"
    sub_hit_rec = {"p":p, "trials_done":0}
    for i in range(n_max+1):
        sub_hit_rec[i] = 0
    
    G = Graph(n_max)
    for l in range(trials):
        adj_dict = G.adj_dict(p)
        max_dist = G.dfs(adj_dict)
        for i in range(1, max_dist+1):
            sub_hit_rec[i] += 1
        sub_hit_rec["trials_done"] = l+1

        with open(new_filepath, "wb") as fp:
            pickle.dump(sub_hit_rec, fp)

def compile_all_data(p, n_max, num_processes, sub_filepath, final_filepath, trials):
    time.sleep(5)
    while(True):
        hit_rec = { "p":p, "trials_done":0, "files_accessed":0}
        for i in range(1, n_max+1):
            hit_rec[i] = 0  

        for i in range(num_processes):
            if not os.path.exists(f"{sub_filepath}_{i}.pkl"): continue
            with open(f"{sub_filepath}_{i}.pkl", "rb") as fp:
                sub_hit_rec = dict(pickle.load(fp))
            hit_rec["trials_done"] += sub_hit_rec["trials_done"]
            for j in range(1, n_max+1):
                hit_rec[j] += sub_hit_rec[j]
            hit_rec["files_accessed"] += 1

        with open(final_filepath, "wb") as gp:
            pickle.dump(hit_rec, gp)

        if hit_rec["trials_done"] >= trials:
            return
            
        time.sleep(5)


                
def main(p, n_max, test_folder, mesh_folder):
    # p_range = np.linspace(0.24, 0.25, 20)
    #p = 0.2485 
    #n_max = 30
    trials = 10000 # should be divisible by 'num_processes'
    num_processes = 10
    hit_rec = { "p":p, "trials_done":0}
    for i in range(1, n_max+1):
        hit_rec[i] = 0
    sub_filepath = os.path.join(os.getcwd(), test_folder, f"p={p}_record")
    final_filepath = os.path.join(os.getcwd(), mesh_folder, f"p={p}_record.pkl")

    processes = []
    for i in range(num_processes):
        processes.append(multiprocessing.Process(target = process_far_point, args = (p, n_max, trials//num_processes, sub_filepath, i)))
    processes.append(multiprocessing.Process(target = compile_all_data, args = (p, n_max, num_processes, sub_filepath, final_filepath, trials)))
    
    for process in processes:
        process.start()
    
    for i, process in enumerate(processes):
        process.join()
        print(f"Process {i} finished for p={p}")
        
    print("Finshed")


if __name__ == "__main__":
    main(p = 0.2485)