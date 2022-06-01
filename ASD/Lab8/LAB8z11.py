# Skończone
# Podpunkt 1 w pliku "LAB8z11.py"
# Podpunkt 2 w pliku "LAB8z12.py"

# Wnioski do pomiarów czasowych:
# Jak widac na wynikach czasów, dla duzych ilości danych metoda enqueue
# okazała sie dużo wolniejsza od metody heapify. Róznica ta może być równiez
# spowodowana mało zoptymailzowaną metodą enqueue.
import random
import timeit


class Element:
    def __init__(self, data, priority):
        self.data = data
        self.priority = priority

    def __str__(self):
        return f'\t {self.data}: {self.priority}'

    def __lt__(self, other):
        return self.priority < other.priority

    def __gt__(self, other):
        return self.priority > other.priority


class MaxHeap:
    def __init__(self):
        self.initsize = 1
        self.size = 0
        self.tab = [None for i in range(self.initsize)]

    def is_empty(self):
        return True if not self.tab[0] else False

    def parent_idx(self, index):
        idx = (index-1) // 2
        return idx if idx >= 0 else 0

    def left_idx(self, index):
        return 2*index + 1

    def right_idx(self, index):
        return 2*index + 2

    def peek(self):
        return self.tab[0]

    def swap(self, idx1, idx2):
        self.tab[idx1], self.tab[idx2] = self.tab[idx2], self.tab[idx1]

    def enqueue(self, data, priority):
        if self.is_empty():
            self.tab[self.size] = Element(data, priority)
            return
        if not self.tab.count(None):
            self.size += 1
            for i in range(self.initsize):
                self.tab.append(None)
            self.tab[self.size] = Element(data, priority)
            self.initsize = len(self.tab)
        else:
            self.size += 1
            self.tab[self.size] = Element(data, priority)

        curr = self.size

        while self.tab[curr] > self.tab[self.parent_idx(curr)]:
            self.swap(curr, self.parent_idx(curr))
            curr = self.parent_idx(curr)

    def dequeue(self):
        if not self.is_empty():
            dequeued = self.tab[0]
            self.size -= 1
            self.tab[0] = self.tab[self.size]
            self.tab[self.size] = None
            curr = 0
            while curr < self.size:
                if not self.tab[curr] or self.left_idx(curr) > self.size or not self.tab[self.left_idx(curr)]:
                    break
                if not self.tab[curr] or self.right_idx(curr) > self.size or not self.tab[self.right_idx(curr)]:
                    break

                if self.tab[self.left_idx(curr)] > self.tab[self.right_idx(curr)]:
                    if self.tab[curr] < self.tab[self.left_idx(curr)]:
                        self.swap(curr, self.left_idx(curr))
                        curr = self.left_idx(curr)
                    else:
                        break
                else:
                    if self.tab[curr] < self.tab[self.right_idx(curr)]:
                        self.swap(curr, self.right_idx(curr))
                        curr = self.right_idx(curr)
                    else:
                        break
            return dequeued
        return None

    def print_tab(self):
        temp = []
        for i in self.tab:
            if i:
                temp.append((i.data, i.priority))
            else:
                temp.append(None)
        print(temp)

    def print_heap(self):
        newtab = self.tab.copy()
        a = 0
        size = len(newtab)
        while True:
            n = 2**a
            if size <= 0:
                break
            temp = ''
            temp += '\n' + ' '*size
            for i in range(n):
                if newtab and newtab[0]:
                    temp += f"|{newtab[0].data}:{newtab[0].priority}|  "
                    newtab.pop(0)
                else:
                    temp += f"{'-'}  "
            print(temp)
            a += 1
            size -= n

    def heapify(self, elemIdx, size=None):
        if not size:
            s = self.size
        else:
            s = size

        largest = elemIdx
        leftChild = self.left_idx(elemIdx)
        rightChild = self.right_idx(elemIdx)

        # Check priority of children

        if leftChild <= s:
            if self.tab[leftChild] > self.tab[largest]:
                largest = leftChild

        if rightChild < s:
            if self.tab[rightChild] > self.tab[largest]:
                largest = rightChild

        # If there is children with higher priority -> swap
        # and call heapify
        if largest != elemIdx:
            self.swap(elemIdx, largest)
            self.heapify(largest, s)

    def buildHeap(self, priorities, data="a"):
        # When we append two arrays
        if isinstance(data, list):
            if len(data) != len(priorities):
                print("Size of data and priorities do not match")
                return
            else:
                for i in range(len(priorities)):
                    if self.is_empty():
                        elem = Element(data[i], priorities[i])
                        self.tab[self.size] = elem
                        self.size += 1
                    else:
                        elem = Element(data[i], priorities[i])
                        self.tab.append(elem)
                        self.size += 1
        # When we append only from one array with priority and single data
        else:
            for i in range(len(priorities)):
                if self.is_empty():
                    elem = Element(data, priorities[i])
                    self.tab[self.size] = elem
                    self.size += 1
                else:
                    elem = Element(data, priorities[i])
                    self.tab.append(elem)
                    self.size += 1
        # When we append only from one

        # Checking heap contitions for non leaf nodes
        firstNonLeaf = self.size//2 - 1
        for elemIdx in range(firstNonLeaf, -1, -1):
            self.heapify(elemIdx)

    def sort(self):
        # Sort by dequeue
        for i in range(self.size-1, 0, -1):
            dequeued = self.dequeue()
            self.tab[self.size] = dequeued


def enq_insert(list):
    heap = MaxHeap()
    for i in list:
        heap.enqueue("a", i)


def heapify_insert(list):
    heap = MaxHeap()
    heap.buildHeap(list, "a")


def main():
    queue = MaxHeap()

    wartosci = [3, 6, 1, 8, 4, 12, 7, 13, 9, 22,
                15, 5, 11, 16, 18, 20, 25, 21, 27, 30]
    data = []
    for i in range(len(wartosci)):
        data.append(f'e{wartosci[i]}')
    queue.buildHeap(wartosci, data)

    print("============ Kopiec zbudowany z tablicy ===========")
    queue.print_heap()
    print("============ Tablica przed sortowaniem ===========\n")
    queue.print_tab()
    queue.sort()
    print("============ Posortowana tablica ===========\n")
    queue.print_tab()

    num_list = [random.randrange(1, 1000, 1) for i in range(10000)]
    print("Czas tworzenia kopca metodą enqueue:")
    print(timeit.timeit(lambda: enq_insert(num_list), number=1))
    print("Czas tworzenia kopca metodą heapify:")
    print(timeit.timeit(lambda: heapify_insert(num_list), number=1))


if __name__ == '__main__':
    main()
