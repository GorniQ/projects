class Matrix:

    def __init__(self, data, fill=0):
        if isinstance(data, tuple):
            self.A = [[fill] * data[1] for i in range(data[0])]
        else:
            self.A = data

    # Dodawanie
    def __add__(self, other):
        if len(self.A) != len(other.A) or len(self.A[0]) != len(other.A[0]):
            print("Złe wymiary macierzy")
        else:
            C = []
            # Dodawanie macierzy
            if isinstance(other, Matrix):
                for i in range(len(self.A)):
                    row = []
                    for j in range(len(self.A[0])):
                        row.append(self.A[i][j] + other.A[i][j])
                    C.append(row)

            # Dodawanie liczby do macierzy
            if isinstance(other, (int, float)):
                for i in range(len(self.A)):
                    row = []
                    for j in range(len(self.A[0])):
                        row.append(self.A[i][j] + other)
                    C.append(row)
        return Matrix(C)

    # Mnożenie macierzowe
    def __mul__(self, other):
        if len(self.A) != len(other.A[0]):
            print("Złe wymiary macierzy")
        else:
            C = []
            for i in range(len(self.A)):
                row = []
                for j in range(len(other.A[0])):
                    wynik = 0
                    for k in range(len(other.A)):
                        wynik += self.A[i][k] * other.A[k][j]
                    row.append(wynik)
                C.append(row)
            return Matrix(C)

    # Wypisywanie macierzy
    def __str__(self):
        string = ''
        for row in self.A:
            string += str(row) + '\n'
        return string

    def __getitem__(self, key):
        value = self.A[key]
        return value

# Transpozycja


def transpose(self):
    At = [[self.A[j][i] for j in range(len(self.A))]
          for i in range(len(self.A[0]))]
    return Matrix(At)


def main():
    mat1 = Matrix([[1, 0, 2],
                   [-1, 3, 1]])
    mat2 = Matrix([[-1, 3, 1],
                   [1, 0, 2]])
    mat3 = Matrix([[3, 1],
                   [2, 1],
                   [1, 0]])

    print("Macierz początkowa:\n", mat1)
    print("Transpozycja:\n", transpose(mat1))
    print("Druga macierz:\n", mat2)
    print("Suma macierzy 1 i 2:\n", mat1+mat2)
    print("Trzecia macierz:\n", mat3)
    print("Mnożenie macierzowe 1 i 3:\n", mat1*mat3)


main()
