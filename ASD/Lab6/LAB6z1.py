class Element:
    def __init__(self, data, priority):
        self.data = data
        self.priority = priority

    def __str__(self):
        return f'data:\t {self.data}\npriority:{self.priority}'

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
            self.tab[0] = self.tab[self.size]
            self.tab[self.size] = None
            self.size -= 1
            curr = 0
            while True:
                if not self.tab[curr] or self.left_idx(curr) > self.initsize or not self.tab[self.left_idx(curr)]:
                    break
                if not self.tab[curr] or self.right_idx(curr) > self.initsize or not self.tab[self.right_idx(curr)]:
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
                temp.append(i.data)
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


def main():
    tab = MaxHeap()
    print(tab.is_empty())
    string = 'algorytm'
    prior = [4, 8, 3, 5, 7, 6, 2, 1]
    j = []
    for i in range(len(prior)):
        tab.enqueue(string[i], prior[i])
    print("===Kopiec===")
    tab.print_heap()
    print("============")
    print("\nDequeue: ")
    print(tab.dequeue())
    print("\nPeek: ")
    print(tab.peek())
    print("\n\n===Tablica===")
    tab.print_tab()
    print("=============")
    print("\n\n===Usuwanie kopca===\n")
    while True:
        if not tab.tab[0]:
            break
        print(f"\tUsuwanie...\n{tab.dequeue()}")

    print("===Kopiec po usunięciu kolejki===")
    tab.print_heap()
    print("============")


if __name__ == '__main__':
    main()
