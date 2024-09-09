import os
import random
import numpy as np
import pickle

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

                
if __name__ == "__main__":

    p = 0.20
    n_max = 20
    trials = 10000
    hit_rec = { "p":p, "trials_done":0}
    for i in range(1, n_max+1):
        hit_rec[i] = 0
    filepath = os.path.join(os.getcwd(), "all_", f"p={p}_record.pkl")
    
    G = Graph(n_max)
    for l in tqdm(range(trials)):
        adj_dict = G.adj_dict(p)
        max_dist = G.dfs(adj_dict)
        for i in range(1, max_dist+1):
            hit_rec[i] += 1
        hit_rec["trials_done"] = l+1

        with open(filepath, "wb") as fp:
            pickle.dump(hit_rec, fp)
