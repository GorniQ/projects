import random


class Element:
    def __init__(self, key, value, lvl):
        self.key = key
        self.value = value
        self.headstab = [None] * (lvl + 1)


class SkipList:
    def __init__(self, size=5):
        self.size = size
        self.head = Element(None, None, size)
        self.level = 0

    def randomLevel(self, p=0.5):
        lvl = 1
        while random.random() < p and lvl < self.size:
            lvl = lvl + 1
        return lvl

    def search(self, key):
        current = self.head

        for i in range(self.level, -1, -1):
            while current.headstab[i] and current.headstab[i].key < key:
                current = current.headstab[i]
        current = current.headstab[0]

        if current and current.key == key:
            return current.value
        return None

    def insert(self, key, value):
        update = [None] * (self.size + 1)
        current = self.head

        for i in range(self.level, -1, -1):
            while current.headstab[i] and current.headstab[i].key < key:
                current = current.headstab[i]
            update[i] = current
        current = current.headstab[0]

        if not current or current.key != key:
            rl = self.randomLevel()
            if rl > self.level:
                for i in range(self.level + 1, rl + 1):
                    update[i] = self.head
                self.level = rl
            elem = Element(key, value, rl)
            for i in range(rl + 1):
                elem.headstab[i] = update[i].headstab[i]
                update[i].headstab[i] = elem
        elif current and current.key == key:
            current.value = value

    def remove(self, key):
        update = [None] * (self.size + 1)
        current = self.head

        for i in range(self.level, -1, -1):
            while current.headstab[i] and current.headstab[i].key < key:
                current = current.headstab[i]
            update[i] = current
        current = current.headstab[0]

        if current and current.key == key:
            for i in range(self.level + 1):
                if update[i].headstab[i] != current:
                    break
                update[i].headstab[i] = current.headstab[i]
            while self.level > 0 and not self.head.headstab[self.level]:
                self.level -= 1

    def displayList(self):
        node = self.head.headstab[0]
        keys = []
        while node:
            keys.append(node.key)
            node = node.headstab[0]
        for lvl in range(self.size - 1, -1, -1):
            print("{}: ".format(lvl), end=" ")
            node = self.head.headstab[lvl]
            idx = 0
            while node:
                while node.key > keys[idx]:
                    print("  ", end=" ")
                    idx += 1
                idx += 1
                print("{:2d}".format(node.key), end=" ")
                node = node.headstab[lvl]
            print("")

    def __str__(self):
        s = ""
        node = self.head.headstab[0]
        while node:
            s += f"({node.key} : {node.value}) "
            node = node.headstab[0]
        return s


def main():
    skipList = SkipList()
    for i in range(1, 16):
        skipList.insert(i, chr(96 + i))

    print("Lista po wstawieniu elemnetów:")
    skipList.displayList()
    print("\nLista w postaci par:")
    print(skipList)
    print("\nDana znajdująca się pod kluczem '2': ", skipList.search(2))
    print("Nadpisanie wartości pod kluczem '2' wartością 'nadpisanie'...")
    skipList.insert(2, 'nadpisanie')
    print("Dana znajdująca się pod kluczem '2': ", skipList.search(2))
    print("\nUsuniecie danych o kluczach 5, 6, 7...")
    skipList.remove(5)
    skipList.remove(6)
    skipList.remove(7)
    print(skipList)
    print("Wstawienie danej pod klucz 6...")
    skipList.insert(6, 'dana')
    print(skipList)


if __name__ == "__main__":
    main()
