import polska
import numpy as np


class Vertex:
    def __init__(self, data):
        self.data = data
        self.firstEdge = None

    def __str__(self):
        return f"{self.data} : {self.firstEdge}"


class ForwardStar:
    def __init__(self):
        self.vertices = []
        self.connections = []

    def insertVertex(self, data):
        vertex = Vertex(data)
        self.vertices.append(vertex)

    def insertEdge(self, vertex1_idx, vertex2_idx):
        pair = [vertex1_idx, vertex2_idx]
        self.connections.append(pair)
        self.connections.sort()
        self.updateFirstEdges()

    def updateFirstEdges(self):
        for i in range(len(self.vertices)):
            self.vertices[i].firstEdge = self.findFirstEdge(i)

    def findFirstEdge(self, vertex1_idx):
        for i in range(len(self.connections)):
            if self.connections[i][0] == vertex1_idx:
                return i

    def deleteVertex(self, vertex_idx):
        self.connections = list(
            filter(lambda x: x[0] != vertex_idx, self.connections))
        self.connections = list(
            filter(lambda x: x[1] != vertex_idx, self.connections))

        for edge in self.connections:
            if edge[0] > vertex_idx:
                edge[0] -= 1
            if edge[1] > vertex_idx:
                edge[1] -= 1
        self.vertices.pop(vertex_idx)
        self.updateFirstEdges()

    def deleteEdge(self, vertex1_idx, vertex2_idx):
        while True:
            try:
                self.connections.remove([vertex1_idx, vertex2_idx])
            except:
                break
        self.updateFirstEdges()

    def getVertexIdx(self, key):
        for i in range(len(self.vertices)):
            if self.vertices[i].data == key:
                return i
        return None

    def getVertex(self, vertex_idx):
        return self.vertices[vertex_idx].data

    def neighbours(self, vertex_idx):
        idx1 = self.vertices[vertex_idx].firstEdge
        if vertex_idx < self.order()-1:
            idx2 = self.vertices[vertex_idx + 1].firstEdge
        else:
            idx2 = self.size()

        neigh = []
        for i in range(idx1, idx2):
            edge = self.connections[i]
            neigh.append(edge[1])
        return neigh

    def order(self):
        return len(self.vertices)

    def size(self):
        return len(self.connections)

    def edges(self):
        edges = []
        for i in self.connections:
            frm = self.getVertex(i[0])
            dest = self.getVertex(i[1])
            edges.append((frm, dest))
        return edges

    def print_graph(self):
        print("|=======+=================+==================|")
        print("|idx    |name:firstEdgeIdx|--> [Connections] |")
        print("|-------+-----------------+------------------|")
        for i in range(self.order()):
            neigh = self.neighbours(i)
            neigh_names = []
            for vert in neigh:
                neigh_names.append(self.getVertex(vert))
            text = f"|{i}\t|  {self.vertices[i]}\t  |--> {neigh_names}"
            print(text)
        print("|=======+=================+==================|")


def main():
    graph = ForwardStar()

    pol = polska.polska
    for city in pol:
        l = city[2]
        graph.insertVertex(l)

    graf = polska.graf
    for n1, n2 in graf:
        idx1 = graph.getVertexIdx(n1)
        idx2 = graph.getVertexIdx(n2)
        graph.insertEdge(idx1, idx2)

    graph.print_graph()

    print("\nSasiedzi wojewodztwa P (5):")
    print(graph.neighbours(5))

    print("\nUsuwanie wojewodztwa malopolskiego (K) z grafu...\n")
    idx = graph.getVertexIdx("K")
    graph.deleteVertex(idx)
    graph.print_graph()

    print("\nUsuwanie krawedzi miedzy mazowieckim(W) i lodzkim(E)...\n")
    idx1 = graph.getVertexIdx("W")
    idx2 = graph.getVertexIdx("E")
    graph.deleteEdge(idx1, idx2)
    graph.deleteEdge(idx2, idx1)
    graph.print_graph()

    print("Rysowanie grafu...")
    edges = graph.edges()
    polska.draw_map(edges)


main()
