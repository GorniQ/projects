class Node:
    def __init__(self, key):
        self.key = key
        self.conections = []


class Edge:
    def __init__(self, vertex1, vertex2, flow=0, capacity=0, isResidual=False):
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.capacity = capacity
        self.flow = flow
        self.isResidual = isResidual

    def __str__(self):
        return f'[{self.vertex2}:{self.capacity}]'


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

    def insertEdge(self, vertex1_idx, vertex2_idx, capacity):
        node = self.list[vertex1_idx]
        dest = self.list[vertex2_idx]
        edge = Edge(node.key, dest.key, 0, capacity, False)
        edgeResidual = Edge(dest.key, node.key, capacity, 0, True)
        node.conections.append(edge)
        dest.conections.append(edgeResidual)

    def deleteVertex(self, vertex_idx):
        key = self.getVertex(vertex_idx).key
        self.list.pop(vertex_idx)
        for i in self.list:
            for j in range(len(i.conections)):
                e = i.conections[j]
                if e.vertex1 == key or e.vertex2 == key:
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
        v = self.getVertex(vertex_idx)
        key = v.key
        edges = []
        for vertex in self.list:
            if vertex == self.list[vertex_idx]:
                # continue
                for neigh in vertex.conections:
                    edges.append(neigh)
            else:
                for neigh in vertex.conections:
                    if neigh.vertex2 == key:
                        edges.append(neigh)
        return edges

    def order(self):
        return self.size

    def size(self):
        edges = self.edges()
        return len(edges)

    def edges(self):
        edges = [[] for _ in range(len(self.list))]
        for vertex in self.list:
            for edge in vertex.conections:
                idx1 = self.getVertexIdx(edge.vertex1)
                idx2 = self.getVertexIdx(edge.vertex2)
                edges[idx1].append((idx2, idx1))
        return edges

    def nodeEdges(self, vertex_idx):
        edges = []
        for neigh in self.list[vertex_idx].conections:
            edges.append(neigh)
        return edges

    def print_graph(self):
        print("==================")
        for i in range(self.size):
            temp = self.list[i]
            print("[idx: " + str(i) + "] --- " +
                  str(temp.key) + ": -> [ ", end="")
            for i in temp.conections:
                print(f"[{i.vertex2}, {i.capacity}] ", end="")
                # print("[", i.vertex2.key, ",", str(i.capacity), "],", end="")
            print("] \n")
        print("==================")

    def BFS(self, s):
        visited = [False for _ in range(self.order())]
        parent = [-1 for _ in range(self.order())]
        queue = []
        queue.append(s)
        idx = self.getVertexIdx(s)
        visited[idx] = True
        while queue:
            el = queue.pop(0)
            elidx = self.getVertexIdx(el)
            n = self.nodeEdges(elidx)
            for edge in n:
                idx1 = self.getVertexIdx(edge.vertex2)
                if not visited[idx1] and edge.capacity > 0:
                    queue.append(edge.vertex2)
                    visited[idx1] = True
                    parent[idx1] = elidx
        return parent

    def countFlow(self, s, t, parent):
        curr = s
        maxFlow = float('inf')
        idx = self.getVertexIdx(t)

        curr_idx = self.getVertexIdx(curr)
        t_idx = self.getVertexIdx(t)
        source_idx = self.getVertexIdx(s)

        visited = [curr_idx]

        if parent[idx] == -1:
            return 0

        while curr_idx != t_idx:
            size = 0
            prev_idx = curr_idx
            edges = self.nodeEdges(curr_idx)
            temp_capacity = float('inf')
            for edge in edges:
                if edge.capacity > 0 and self.getVertexIdx(edge.vertex2) not in visited:
                    if size <= edge.capacity:
                        curr_idx = self.getVertexIdx(edge.vertex2)
                        size = edge.capacity
                        temp_capacity = min(temp_capacity, size)
            maxFlow = min(temp_capacity, maxFlow)
            if curr_idx == prev_idx:
                curr_idx = visited.pop(-2)
            visited.append(curr_idx)
        return maxFlow

    def pathAugumentation(self, s, t, parent, min_cap):
        curr = s
        visited = [curr]
        idx = self.getVertexIdx(t)
        if parent[idx] == -1:
            return 0
        while curr != t:
            size = 0
            edges = self.nodeEdges(self.getVertexIdx(curr))
            curr_edge = edges[0]
            prev = curr
            temp = curr
            for edge in edges:
                if edge.capacity > 0 and edge.vertex2 not in visited:
                    if edge.capacity >= size:
                        size = edge.capacity
                        curr = edge.vertex2
                        curr_edge = edge

            if curr == prev:
                temp2 = visited[-2]
                for edge in edges:
                    if edge.vertex2 == temp2:
                        edge.capacity -= min_cap
                        edge.flow += min_cap
                        break
                curr = visited.pop(-2)
            else:
                if curr_edge.vertex2 == curr:
                    curr_edge.capacity -= min_cap
                    curr_edge.flow += min_cap
            visited.append(curr)

    def FF(self, s, t):
        parent = self.BFS(s)
        min_cap = self.countFlow(s, t, parent)
        sum = min_cap
        self.pathAugumentation(s, t, parent, min_cap)
        while min_cap != 0:
            parent = self.BFS(s)
            min_cap = self.countFlow(s, t, parent)
            sum += min_cap
            self.pathAugumentation(s, t, parent, min_cap)
        return sum


def main():
    graf_0 = [('s', 'u', 2), ('u', 't', 1), ('u', 'v', 3),
              ('s', 'v', 1), ('v', 't', 2)]
    graf_1 = [('s', 'a', 16), ('s', 'c', 13), ('a', 'c', 10), ('c', 'a', 4), ('a', 'b', 12),
              ('b', 'c', 9), ('b', 't', 20), ('c', 'd', 14), ('d', 'b', 7), ('d', 't', 4)]
    graf_2 = [('s', 'a', 3), ('s', 'c', 3), ('a', 'b', 4), ('b', 's', 3), ('b', 'c', 1),
              ('b', 'd', 2), ('c', 'e', 6), ('c', 'd', 2), ('d', 't', 1), ('e', 't', 9)]
    graf_3 = [('s', 'a', 8), ('s', 'd', 3), ('a', 'b', 9), ('b', 'd', 7),
              ('b', 't', 2), ('c', 't', 5), ('d', 'b', 7), ('d', 'c', 4)]
    graphs = [graf_0, graf_1, graf_2, graf_3]
    i = 0
    for data in graphs:
        graph = GraphList()
        for edge in data:
            graph.insertVertex(edge[0])
            graph.insertVertex(edge[1])
            idx1 = graph.getVertexIdx(edge[0])
            idx2 = graph.getVertexIdx(edge[1])
            graph.insertEdge(idx1, idx2, edge[2])
        # graph.print_graph()
        sum = graph.FF('s', 't')
        print(f"Result for graph {i}: {sum}")
        i += 1


main()
