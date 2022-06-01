#Poprawione
# Indeks J jest sprawdzany jako ostatni w danym algorytmie jako że nie 
# znaleziono kolejnego wierzchołka który nie jeszcze nie był odwiedzony,
# algorytm dodawał po raz kolejny krawędź która była już wcześniej dodana.
# Poprawiłem zwracanie wyniku algorytmu do maina, oraz dodałem
# część kodu sprawdzającą czy dana połączenie istnieje już w krawędziach należących
# do danego wierzchołka by nie występowały powtórzenia


import graf_mst


class Node:
    def __init__(self, key):
        self.key = key
        self.color = None
        self.conections = []


class GraphList:
    def __init__(self):
        self.size = 0
        self.list = []

    def insertVertex(self, data):
        for n in self.list:
            if n.key == data:
                return
        node = Node(data)
        self.list.append(node)
        self.size += 1

    def insertEdge(self, vertex1_idx, vertex2_idx, weight):
        node = self.list[vertex1_idx]
        dest = self.list[vertex2_idx]
        node.conections.append([dest.key, weight])

    def deleteVertex(self, vertex_idx):
        key = self.getVertex(vertex_idx).key
        self.list.pop(vertex_idx)
        for i in self.list:
            for j in range(len(i.conections)):
                if i.conections[j].count(key):
                    i.conections.pop(j)
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

    def nodeEdges(self, vertex_idx):
        edges = []
        key = self.list[vertex_idx].key
        # for neigh in self.list[vertex_idx].conections:
        #     edges.append([self.list[vertex_idx].key, neigh[0], neigh[1]])
        for vertex in self.list:
            if vertex == self.list[vertex_idx]:
                # continue
                for neigh in vertex.conections:
                    edges.append(
                        [neigh[0], vertex.key, neigh[1]])
            else:
                for neigh in vertex.conections:
                    if neigh[0] == key:
                        edges.append([vertex.key, neigh[0], neigh[1]])
        return edges

    def print_graph(self):
        print("==================")
        for i in range(self.size):
            temp = self.list[i]
            print("[idx: " + str(i) + "] --- " + str(temp.key) + ":", end="")
            print(" -> {}".format(temp.conections), end="")
            print(" \n")
        print("==================")

    def MST(self, start_v_idx):
        n = self.size
        intree = [0 for i in range(n)]
        distance = [float('inf') for i in range(n)]
        parent = [-1 for i in range(n)]
        treeMST = GraphList()

        for i in self.list:
            treeMST.insertVertex(i.key)

        v = start_v_idx
        while intree[v] == 0:
            intree[v] = 1
            neigh = self.nodeEdges(v)
            for somsiad in neigh:
                idx = self.getVertexIdx(somsiad[0])
                if distance[idx] > somsiad[2] and intree[idx] == 0:
                    distance[idx] = somsiad[2]
                    parent[idx] = v

            min_weight = float('inf')
            next_idx = v
            for i in range(len(distance)):
                if intree[i] == 0:
                    if distance[i] < min_weight:
                        min_weight = distance[i]
                        next_idx = i
            v = next_idx
            id1 = treeMST.getVertex(v).key
            id2 = treeMST.getVertex(parent[v]).key
            c = treeMST.neighbours(v)
            inconections = False
            for i in c:
                if parent[v] == treeMST.getVertexIdx(i[0]):
                    inconections = True
            if not inconections:
                treeMST.insertEdge(v, parent[v], distance[v])
        return treeMST


def main():
    graph = GraphList()
    data = graf_mst.graf
    for edge in data:
        graph.insertVertex(edge[0])
        graph.insertVertex(edge[1])
        idx1 = graph.getVertexIdx(edge[0])
        idx2 = graph.getVertexIdx(edge[1])
        graph.insertEdge(idx1, idx2, edge[2])
    graph.print_graph()
    print("Krawędzie wierzchołka o indeksie 1 (B):")
    print(graph.nodeEdges(1))
    MST = graph.MST(0)
    print("\n=========== MST graph =============")
    MST.print_graph()


main()