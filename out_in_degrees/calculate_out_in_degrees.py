import sys
import networkx as nx

# given a graph from a file
# this code outputs the node(s) with the
# highest out-degree
# and the node(s) with the highest in-degree
##
# the file is supposed to be in the following format
# 
# n
# s1 t1
# s2 t2
# ...
# sn tn
#
# where n is the number of vertices
# and each following row represents and edge
# where sn is the source vertice
# and tn the target vertice

filename = sys.argv[1]
file= open(filename).readlines()

num_vertices = int(file[0])

edges = [(int(x.split()[0]), int(x.split()[1])) for x in file[1:]]
vertices = [x for x in range(num_vertices)]

vertices_out_degrees = {v:0 for v in vertices}
vertices_in_degrees = {v:0 for v in vertices}


for e in edges:
    s = e[0]
    t = e[1]
    vertices_out_degrees[s] += 1
    vertices_in_degrees[t] += 1


sorted_out_degrees = sorted([vertices_out_degrees[x] for x in vertices_out_degrees], reverse=True)
sorted_in_degrees = sorted([vertices_in_degrees[x] for x in vertices_in_degrees], reverse=True)

highest_out = sorted_out_degrees[0]
highest_in = sorted_in_degrees[0]

highest_out_nodes = [x for x in vertices_out_degrees if vertices_out_degrees[x] == highest_out]
highest_in_nodes = [x for x in vertices_in_degrees if vertices_in_degrees[x] == highest_in]


def get_verb(list_nodes):
    if len(list_nodes) > 1:
        subj, verb = "The nodes", 'are'
    else:
        subj, verb = "The node", 'is'
    return subj, verb

subj_out, verb_out = get_verb(highest_out_nodes)
subj_in, verb_in = get_verb(highest_in_nodes)

print("{} with the highest out-degree {} {}, with an out-degree of {}".format(subj_out,  verb_out, highest_out_nodes,highest_out))
print("{} with the highest in-degree {} {}, with an in-degree of {}".format(subj_in, verb_in,highest_in_nodes,  highest_in))
