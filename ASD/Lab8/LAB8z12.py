#Podpunkt 2
class Element:
    def __init__(self, value, data):
        self.value = value
        self.data = data

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __str__(self):
        return f'({self.value} : {self.data})'


class Sort:
    def __init__(self):
        self.size = 0
        self.tab = []

    def append(self, elem):
        if isinstance(elem, list):
            for i in elem:
                el = Element(i[0], i[1])
                self.tab.append(el)
                self.size += 1
        else:
            el = Element(i[0], i[1])
            self.tab.append(el)
            self.size += 1

    def swap(self):
        for i in range(1, self.size):
            key = self.tab[i]
            j = i-1
            while j >= 0 and key < self.tab[j]:
                self.tab[j+1] = self.tab[j]
                j -= 1
            self.tab[j+1] = key

    def shift(self):
        for i in range(self.size):
            min_idx = i
            for j in range(i+1, self.size):
                if self.tab[min_idx] > self.tab[j]:
                    min_idx = j
            self.tab[i], self.tab[min_idx] = self.tab[min_idx], self.tab[i]

    def __str__(self):
        str = ''
        for i in self.tab:
            str += f'({i.value}:{i.data}) '
        return str


def main():
    tab = Sort()
    print("\n========Swap sort======= ")
    data = [(5, 'A'), (5, 'B'), (7, 'C'), (2, 'D'), (5, 'E'),
            (1, 'F'), (7, 'G'), (5, 'H'), (1, 'I'), (2, 'J')]

    tab.append(data)
    print("\nTablica wejściowa:")
    print(tab)
    tab.swap()
    print("\nPosortowana tablica:")
    print(tab)
    print("\n========Shift sort======= ")
    data = [(5, 'A'), (5, 'B'), (7, 'C'), (2, 'D'), (5, 'E'),
            (1, 'F'), (7, 'G'), (5, 'H'), (1, 'I'), (2, 'J')]

    tab1 = Sort()
    tab1.append(data)
    print("\nTablica wejściowa:")
    print(tab1)
    tab1.shift()
    print("\nPosortowana tablica:")
    print(tab1)


main()
