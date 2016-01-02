import shapefile
import gdal
import pandas as pd 
import matplotlib.pyplot as plt

class Weighted_graph:
    edges = []
    weight = []
    vertices = []

    def __init__(self, edge_list, weight):
        self.edges.append(edge_list)
        self.weight.append(weight)

    def __sort(self):
        if len(self.edges) != len(self.weight):
            return
        for i in range(1, len(self.weight)):
            temp_weight = self.weight[i]
            temp_edge = self.edges[i]
            current = i - 1
            while current >= 0 and temp_weight < self.weight[current]:
                self.weight[current+1] = self.weight[current]
                self.edges[current+1] = self.edges[current]
                current -= 1
            self.weight[current+1] = temp_weight
            self.edges[current+1] = temp_edge

        #print " "
        #print "printing in sorted order"
        #for i in range(len(self.edges)):
        #    print str(self.edges[i])+" weight "+ str(self.weight[i])

    def __makeset(self):
        for i in range(len(self.edges)):
            for j in range(len(self.edges[i])):             
                if self.edges[i][j] not in self.vertices:
                    self.vertices.append(self.edges[i][j])
        #print "vertices"
        for k in range(len(self.vertices)):
            #print self.vertices[k]
            self.vertices[k] = [self.vertices[k]]
        #print "+++++++++"

    def __findset(self, vertex):
        # returns index of the vertex
        for i in range(len(self.vertices)):
            for element in self.vertices[i]:
                if element == vertex:
                    return i
        return None

    def printVertices(self,longitudelist_merged,latitudelist_merged):
        self.__sort()
        self.__makeset()
        print len(self.vertices)
        for k in range(0,len(self.vertices)):
            print self.vertices[k]
            print str(longitudelist_merged[self.vertices[k][0]]) +" " + str(latitudelist_merged[self.vertices[k][0]])

    def __union(self, vertex1, vertex2):
        index1 = self.__findset(vertex1)
        index2 = self.__findset(vertex2)
        for element in self.vertices[index2]:
            self.vertices[index1].append(element)
        self.vertices.pop(index2)

    def add(self, edge_list, weight):
        """
        Add an edge(defined by 2 vertices in a list) and its corresponding weight( time in years ) to edges
        """
        self.edges.append(edge_list)
        self.weight.append(weight)
        print str(edge_list)+" weight "+ str(weight)

    def kruskal(self,longitudelist_merged,latitudelist_merged):
        self.__sort()
        self.__makeset()
        count, i = 0, 0
        w = shapefile.Writer(shapefile.POLYLINE)
        w.field('time','N','40')
        columns=['node','%_hh','time_years']
        df=pd.DataFrame(columns=columns) 
        while len(self.vertices) > 1:
            if self.__findset(self.edges[i][0]) != self.__findset(self.edges[i][1]):
                print "(%d %d) edge selected." % (self.edges[i][0], self.edges[i][1])
                count += 1
                self.__union(self.edges[i][0], self.edges[i][1])
                p1=float(longitudelist_merged[self.edges[i][0]])
                w.line(parts=[[[float(longitudelist_merged[self.edges[i][0]]),float(latitudelist_merged[self.edges[i][0]])],[float(longitudelist_merged[self.edges[i][1]]),float(latitudelist_merged[self.edges[i][1]])]]])
                w.record(self.weight[i])
            i += 1
        w.save('line_file')
        w = shapefile.Writer(shapefile.POINT)
        w.field('longitude')
        w.field('latitude')
        for i in range(0,len(longitudelist_merged)):
            w.point(float(longitudelist_merged[i]),float(latitudelist_merged[i]))
            w.record(longitudelist_merged[i],latitudelist_merged[i])
        w.save('points_file')

    def print_graph(self):
        """
        Print each set of edges in a graph and its corresponding edges
        """
        print self.edges
        print self.weight
        print self.vertices

def print_attributes(obj):
    for attr in obj.__dict__:
        print attr, getattr(obj, attr)

def find_defining_class(obj, method_name):
    for origin in type(obj).mro():
        if method_name in origin.__dict__:
            return origin

# if __name__ == "__main__":
#     test_graph = Weighted_graph([1,2], 0)
#     test_graph.add([2,3], 1)
#     test_graph.add([3,4], 0)
#     test_graph.add([4,5], 0)
#     test_graph.add([5,1], 0)
#     test_graph.kruskal()
#     test_graph.print_graph()