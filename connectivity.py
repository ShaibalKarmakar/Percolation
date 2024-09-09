import os
import random
import numpy as np
import pickle
#ifrom itertools import combinations_with_replacement

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
    
    def find_biggest_conn_comp(self, adj_dict):
        vertices = list(adj_dict.keys())
        size = len(vertices)
        flag = [False for v in vertices]
        max_comp_size = 0
        for vert in vertices:
            if flag[vert] == False:
                visited = set()
                stack = [vert]
                while stack:
                    u = stack.pop()
                    if u not in visited:
                        visited.add(u)
                        flag[u] = True
                        for nbr in adj_dict[u]:
                            stack.append(nbr)
                max_comp_size = max(len(visited), max_comp_size)
        return max_comp_size/size


if __name__ == "__main__":
    n_range = range(20,32,2)
    n_trials = 10000
    p_range = np.linspace(0.1, 0.9, 20)
    info = {}
    for n in n_range:
        G = Graph(n)
        rec = []
        for p in p_range:
            s = 0
            for _ in tqdm(range(n_trials), desc = f"n={n},p={p:.3f}"):
                adj_dict = G.adj_dict(p = 0.2)
                s += G.find_biggest_conn_comp(adj_dict)
            rec.append(s/n_trials)
            info[n] = rec.copy()

            with open("comp_record.pkl", "wb") as fp:
                pickle.dump(info, fp)
        plt.plot(p_range, rec)
        plt.savefig(f"{os.getcwd()}/comp_images/n={n}.png")
        plt.close()
