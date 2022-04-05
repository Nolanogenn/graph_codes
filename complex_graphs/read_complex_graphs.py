class read_complex_graphs:
    def __init__(self, filename, is_directed=False):
        self.filename = filename
        self.is_directed = is_directed
    
    #given a list, this function return a list of the int() of the element of the original list
    def turn_int_elements(self,list_elements):
        new_list = [int(x) for x in list_elements]
        return new_list

    def get_graph(self):
        graph = open(self.filename).readlines()

        first_row = graph[0].split()
        num_vertices = int(first_row[0])
        num_edges = int(first_row[1])

        vertices = [int(x.split()[0]) for x in graph[1:]]
        neighbors = [self.turn_int_elements(x.split()[1:]) for x in graph[1:]]
        
        edges = []

        for enum, v in enumerate(vertices):
            neighbor_list = neighbors[enum]
            for t in neighbor_list:
                edge_single = (v,t)
                if self.is_directed:
                    edges.append(edge_single)
                else:
                    edge_single_opposite = edge_single[::-1]
                    if edge_single not in edges and edge_single_opposite not in edges:
                        edges.append(edge_single)

        return vertices, edges
