from read_complex_graphs import read_complex_graphs
import sys 

filename = sys.argv[1]

graph = read_complex_graphs(filename, is_directed=True)

vertices, edges = graph.get_graph()
triangles = []

for v in vertices:
    starting_es = []
    ending_es = []
    for e in edges:
        if e[0] == v:
            starting_es.append(e)
        elif e[1] == v:
            ending_es.append(e)
    if len(starting_es) > 1 and len(ending_es) > 1:
        for starting_e in starting_es:
            for ending_e in ending_es:
                middle_s = starting_e[1]
                middle_t = ending_e[0]
                for e in edges:
                    if e[0] == middle_s and e[1] == middle_t:
                        triangles.append([starting_e, e, ending_e])


num_triangles = len(triangles)//6

print("The graph has {} triangles".format(num_triangles))


