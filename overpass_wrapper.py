## Imports ##
import overpy
from collections import defaultdict
from euler_coord import euler_coord
import sys
sys.setrecursionlimit(10000)

## Class Instantiation ##
class overpy_extractor(object):
    bounding_box = [0.0, 0.0, 0.0, 0.0]
    adj_list = []

    def __init__(self, bbox):
        self.bounding_box = bbox
        self.adj_list = []
        self.api = overpy.Overpass()

    def find_euler_tour(self, graph):
        tour = []
        E = graph

        numEdges = defaultdict(int)

        def find_tour(u):
            for e in range(len(E)):
                if E[e] == 0:
                    continue
                if u == E[e][0]:
                    u, v = E[e]
                    E[e] = 0
                    find_tour(v)
                elif u == E[e][1]:
                    v, u = E[e]
                    E[e] = 0
                    find_tour(v)
            tour.insert(0, u)

        for i, j in graph:
            numEdges[i] += 1
            numEdges[j] += 1

        start = graph[0][0]
        for i, j in numEdges.items():
            if j % 2 > 0:
                start = i
                break

        current = start
        find_tour(current)

        if tour[0] != tour[-1]:
            return None
        return tour

    # ensures that there is not overdraw happening from overpass api
    def helper_func_in_bbox_smart(self, c):
        la = float(c.latitude)
        lo = float(c.longitude)
        bbox0 = float(self.bounding_box[0])
        bbox1 = float(self.bounding_box[1])
        bbox2 = float(self.bounding_box[2])
        bbox3 = float(self.bounding_box[3])
        if (la > (bbox0 - .0005) and la < (bbox2 + .0005)):
            if (lo > (bbox1 - .0005) and lo < (bbox3 + .0005)):
                return True
        return False

    def adjacency_list_builder(self, coord_list):
        # ADJACENCY LIST
        adj = {}
        
        # Initialize adjacency list with all nodes
        for w in coord_list:
            for i in range(0, len(w)):
                adj[w[i]] = []
        
        # Append the adjacent nodes to each node in dictionary
        for w in coord_list:
            for i in range(0, len(w)):
                if i == 0 and i < len(w)-1:
                    adj[w[i]] = adj[w[i]] + [w[i + 1]]
                elif i == len(w) - 1:
                    adj[w[i]] = adj[w[i]] + [w[i - 1]]
                else:
                    adj[w[i]] = adj[w[i]] + [w[i - 1]] + [w[i + 1]]
        
        # remove duplicates from adjacency list
        for e in adj:
            adj[e] = list(set(adj[e]))

        # convert adjacency list to graph
        g = []
        for k in adj:
            for v in adj[k]:
                g.append((k, v))

        return g

    # Interacts with overpass, gets all the residential roads
    def extract(self):
        ## overpass extract ##
        bbox = str(self.bounding_box[0]) + "," + str(self.bounding_box[1]) + "," + str(self.bounding_box[2]) + "," + str(self.bounding_box[3])
        
        query_string = f"""(
                way[highway=motorway]({bbox}); node[highway=motorway]({bbox});
                way[highway=trunk]({bbox}); node[highway=trunk]({bbox});
                way[highway=primary]({bbox}); node[highway=primary]({bbox}); 
                way[highway=secondary]({bbox}); node[highway=secondary]({bbox}); 
                way[highway=tertiary]({bbox}); node[highway=tertiary]({bbox}); 
                way[highway=unclassified]({bbox}); node[highway=unclassified]({bbox});
                way[highway=residential]({bbox}); node[highway=residential]({bbox}); 

                way[highway=living_street]({bbox}); node[highway=living_street]({bbox});
                way[highway=service]({bbox}); node[highway=service]({bbox});
                way[highway=pedestrian]({bbox}); node[highway=pedestrian]({bbox});
                way[highway=track]({bbox}); node[highway=track]({bbox});

            ); 
            (._;>;); 
            out body;
            """

        result = self.api.query(query_string)  # calls overpass api with query

        ## convert to way_s list and euler_coords ##
        euler_coord_list =[]
        way_s = []
        for way in result.ways:
            a = []
            for node in way.nodes:
                euler_c = euler_coord(node.lat, node.lon, node.id)
                if(self.helper_func_in_bbox_smart(euler_c)):
                    euler_coord_list.append(euler_c)
                    a.append(node.id)
            way_s.append(a)
        del result

        ## handling error ##
        if(len(way_s) < 2):
            return 101
        if(len(euler_coord_list)>2500):
            return 102
        ## tour generation ##
        g = self.adjacency_list_builder(way_s)
        t = self.find_euler_tour(g)

        ## sending it back to the server to be drawn ##
        new_euler_dict = []
        for ta1 in t:
            found = False
            for i in range(0, len(euler_coord_list)):
                if found != True and ta1 == euler_coord_list[i].get_node_id():
                    found = True
                    new_euler_dict.append([euler_coord_list[i].get_lat(), euler_coord_list[i].get_long()])
        return new_euler_dict
