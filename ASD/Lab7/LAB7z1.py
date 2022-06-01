# Skonczone

import polska
import numpy as np


class GraphMatrix:
    def __init__(self):
        self.size = 0
        self.matrix = np.zeros((self.size, self.size))
        self.vertices = []

    def insertVertex(self, data):
        self.matrix.resize((self.size+1, self.size+1))
        self.size += 1
        self.vertices.append(data)

    def insertEdge(self, vertex1_idx, vertex2_idx):
        self.matrix[vertex1_idx][vertex2_idx] = 1

    def deleteVertex(self, vertex_idx):
        self.matrix = np.delete(self.matrix, vertex_idx, 0)
        self.matrix = np.delete(self.matrix, vertex_idx, 1)
        self.size -= 1
        self.vertices.pop(vertex_idx)

    def deleteEdge(self, vertex1_idx, vertex2_idx):
        self.matrix[vertex1_idx][vertex2_idx] = 0

    def getVertexIdx(self, key):
        for i in range(len(self.vertices)):
            if key == self.vertices[i]:
                return i
        return None

    def getVertex(self, vertex_idx):
        return self.vertices[vertex_idx]

    def neighbours(self, vertex_idx):
        neigh = []
        for i in range(self.size):
            if self.matrix[i][vertex_idx] == 1:
                neigh.append(self.vertices[i])
            if self.matrix[vertex_idx][i] == 1:
                neigh.append(self.vertices[i])

        return neigh

    def order(self):
        return len(self.vertices)

    def size(self):
        edges = self.edges()
        return len(edges)

    def edges(self):
        edges = []
        for i, j in np.ndindex(self.matrix.shape):
            if self.matrix[i][j] == 1:
                edge = self.vertices[i], self.vertices[j]
                edges.append(edge)
        return edges

    def print_graph(self):
        print("==================")
        print(self.matrix)
        print("==================")


class Node:
    def __init__(self, key):
        self.key = key
        self.conections = []


class GraphList:
    def __init__(self):
        self.size = 0
        self.list = []

    def insertVertex(self, data):
        node = Node(data)
        self.list.append(node)
        self.size += 1

    def insertEdge(self, vertex1_idx, vertex2_idx):
        node = self.list[vertex1_idx]
        dest = self.list[vertex2_idx]
        node.conections.append(dest.key)

    def deleteVertex(self, vertex_idx):
        key = self.getVertex(vertex_idx).key
        self.list.pop(vertex_idx)
        for i in self.list:
            if i.conections.count(key):
                i.conections.remove(key)
        self.size -= 1

    def deleteEdge(self, vertex1_idx, vertex2_idx):
        node = self.list[vertex1_idx]
        key = self.getVertex(vertex2_idx).key
        if node.conections.count(key):
            node.conections.remove(key)

    def getVertexIdx(self, key):
        for i in range(len(self.list)):
            temp = self.list[i]
            if temp.key == key:
                return i
        return None

    def getVertex(self, vertex_idx):
        if len(self.list) > 0:
            return self.list[vertex_idx]
        return None

    def neighbours(self, vertex_idx):
        return self.list[vertex_idx].conections

    def order(self):
        return self.size

    def size(self):
        edges = self.edges()
        return len(edges)

    def edges(self):
        edges = []
        for vertex in self.list:
            for c in vertex.conections:
                pair = vertex.key, c
                edges.append(pair)
        return edges

    def print_graph(self):
        print("==================")
        for i in range(self.size):
            temp = self.list[i]
            print("[idx: " + str(i) + "] --- " + str(temp.key) + ":", end="")
            print(" -> {}".format(temp.conections), end="")
            print(" \n")
        print("==================")


def test(typ):
    if typ == 1:
        graph = GraphMatrix()
    elif typ == 2:
        graph = GraphList()

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

    print("Usuwanie województwa małopolskiego (K) z grafu...")
    idx = graph.getVertexIdx("K")
    graph.deleteVertex(idx)
    graph.print_graph()

    print("Usuwanie krawędzi między mazowieckim(W) i łódzkim(E)...")
    idx1 = graph.getVertexIdx("W")
    idx2 = graph.getVertexIdx("E")
    graph.deleteEdge(idx1, idx2)
    graph.deleteEdge(idx2, idx1)
    graph.print_graph()

    print("Rysowanie grafu...")
    edges = graph.edges()
    polska.draw_map(edges)


def main():
    print("Choose method number:")
    print("[1] AdjacencyMatrix\n[2] AdjacencyList")
    method = int(input("Wpisz numer metody:"))
    test(method)


if __name__ == '__main__':
    main()
