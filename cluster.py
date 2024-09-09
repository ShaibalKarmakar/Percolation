import os
import random
import numpy as np
import pickle
from itertools import combinations_with_replacement

import matplotlib.pyplot as plt

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
        while stack:
            vertex = stack.pop()
            if vertex in visited:
                continue
            visited.add(vertex)
            for nbr in adj_dict[vertex]:
                stack.append(nbr)
                a,b,c = self.to_vertex_dict[nbr]
                if max(abs(a), abs(b), abs(c)) >= self.n:
                    return 1
        return 0

                
if __name__ == "__main__":
    # C = cluster(n=50)
    # adj_dict = C.adj_dict(p=0.2)
    # print(C.dfs(adj_dict))
    # p_range = np.linspace(0.2, 0.25, 10)
    filename = "new_record_025.pkl"
    p_range = [0.25]
    if os.path.exists(os.path.join(os.getcwd(), filename)):
        with open(filename, "wb+") as gp:
            info = dict(pickle.load(gp))
    else:
        info = {}
    for p in p_range[:1]:
        n_range = range(5, 30)
        rec = {}
        for l,n in enumerate(n_range):
            C = Graph(n)
            success = 0
            trials = int(1000*n)
            for _ in tqdm(range(trials), desc = f"n={n}"):
                adj_dict = C.adj_dict(p)
                success += C.dfs(adj_dict)
            rec[n] = (success/trials, trials)
            info[p] = rec.copy()
            with open(filename, "wb") as fp:
                pickle.dump(info, fp)
        plt.plot(n_range, rec)
        plt.title(f"trials = {trials}")
        plt.savefig(f"{os.getcwd()}/images/p={p}.png")
        plt.close()


