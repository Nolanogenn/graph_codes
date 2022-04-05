import gzip
import sys

filename = sys.argv[1]
graph = gzip.open(filename).readlines()

vertices = []
edges = []

neighbors = {}

for edge_line in graph:
    edge_line_list = edge_line.split()
    subj = edge_line_list[0]
    target = edge_line_list[2]
    
    if subj not in vertices:
        vertices.append(subj)
    if target not in vertices:
        vertices.append(target)

    if subj not in neighbors:
        neighbors[subj] = [target]
    else:
        neighbors[subj].append(target)


colored_vertices = []

color_vertices = {k:'' for k in vertices}

for v in vertices:
    if v not in colored_vertices:
        color_vertices[v] = 'red'
        colored_vertices.append(v)
        for v2 in neighbors[v]:
            color_vertices[v2] = 'black'
            colored_vertices.append(v2)

is_bipartite = True

for e in edges:
    s = e[0]
    t = e[1]
    if color_vertices[s] == color_vertices[t]:
        is_bipartite= False
        break

print(is_bipartite)
