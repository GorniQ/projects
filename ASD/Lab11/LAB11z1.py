# Poprawione
import numpy as np


class GraphMatrix:
    def __init__(self):
        self.size = 0
        self.matrix = np.zeros((self.size, self.size))
        self.vertices = []

    def insertVertex(self, data):
        if self.vertices.count(data) > 0:
            return
        else:
            col = np.zeros((len(self.matrix), 1))
            row = np.zeros((1, len(self.matrix)+1))
            self.matrix = np.c_[self.matrix, col]
            self.matrix = np.r_[self.matrix, row]
            self.size += 1
            self.vertices.append(data)

    def insertEdge(self, vertex1_idx, vertex2_idx):
        self.matrix[vertex1_idx][vertex2_idx] = 1
        self.matrix[vertex2_idx][vertex1_idx] = 1

    def deleteVertex(self, vertex_idx):
        self.matrix = np.delete(self.matrix, vertex_idx, 0)
        self.matrix = np.delete(self.matrix, vertex_idx, 1)
        self.size -= 1
        self.vertices.pop(vertex_idx)

    def deleteEdge(self, vertex1_idx, vertex2_idx):
        self.matrix[vertex1_idx][vertex2_idx] = 0
        self.matrix[vertex2_idx][vertex1_idx] = 0

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
            # if self.matrix[vertex_idx][i] == 1:
            #     neigh.append(self.vertices[i])

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
        string = '_| '
        for i in self.vertices:
            string += i + "  "
        string += "\n"
        for row in range(len(self.matrix)):
            string += self.vertices[row] + "| "
            for col in range(len(self.matrix[row])):
                string += str(int(self.matrix[row][col])) + "  "
            string += "\n"
        print(string)
        print("==================")


def initializeM0(graphP, graphG):
    P = graphP.matrix
    G = graphG.matrix
    M0 = np.zeros((len(P), len(G)))
    for i in range(len(M0)):
        for j in range(len(M0[i])):
            degP = np.count_nonzero(P[i] == 1)
            degG = np.count_nonzero(G[j] == 1)
            # print(degG,degP)
            if degP <= degG:
                M0[i][j] = 1
    return M0


def ullman(used_columns, curr_row, G, P, M, fst_recursion=True):
    global no_recursion
    global tab
    if fst_recursion:
        no_recursion = 0
        tab = []
    if curr_row == len(M):
        if (P == M @ (M @ G).T).all():
            return M, True, no_recursion
        return M, False, no_recursion

    Mcopy = M.copy()
    Mcopy = prune(G, P, Mcopy)
    for c in range(len(M[curr_row])):
        if c not in used_columns:
            Mcopy[curr_row] = 0
            Mcopy[curr_row][c] = 1
            used_columns.append(c)
            no_recursion += 1
            u = ullman(used_columns, curr_row+1, G, P, Mcopy, False)
            if u[1]:
                tab.append(u)
                no_recursion = 0
            used_columns.remove(c)
    return tab, False, no_recursion


def prune(G, P, M):
    while True:
        Mcopy = M.copy()
        for i in range(len(M)):
            for j in range(len(M[0])):
                if M[i][j] == 1:
                    temp = 0
                    for x in range(len(M)):
                        for y in range(len(M[0])):
                            if P[i, x] == 1 and G[j, y] == 1:
                                if M[x, y] == 1:
                                    temp += 1
                    if temp == 0:
                        M[i, j] = 0
                        return M
        if np.array_equal(M, Mcopy):
            return M


def main():
    graphP = GraphMatrix()
    graphG = GraphMatrix()
    graph_G = [('A', 'B', 1), ('B', 'F', 1), ('B', 'C', 1),
               ('C', 'D', 1), ('C', 'E', 1), ('D', 'E', 1)]
    graph_P = [('A', 'B', 1), ('B', 'C', 1), ('A', 'C', 1)]

    for edge in graph_G:
        graphG.insertVertex(edge[0])
        graphG.insertVertex(edge[1])
        idx1 = graphG.getVertexIdx(edge[0])
        idx2 = graphG.getVertexIdx(edge[1])
        graphG.insertEdge(idx1, idx2)

    for edge in graph_P:
        graphP.insertVertex(edge[0])
        graphP.insertVertex(edge[1])
        idx1 = graphP.getVertexIdx(edge[0])
        idx2 = graphP.getVertexIdx(edge[1])
        graphP.insertEdge(idx1, idx2)

    P = graphP.matrix
    G = graphG.matrix
    M0 = initializeM0(graphP, graphG)

    print("Matrix M0:")
    print("================")
    print(M0)
    print("================")
    print("Matrix G:")
    graphG.print_graph()
    print("Matrix P:")
    graphP.print_graph()

    print("Results:")
    out1 = ullman([], 0, G, P, M0)
    for out in out1[0]:
        print("================")
        print(f'M:\n{out[0]}\nisIsomorphic: {out[1]}\nno_recursion: {out[2]}')
        print("================")


main()
