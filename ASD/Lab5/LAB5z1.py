class Node:
    def __init__(self, key, value, left=None, right=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right


class BST:
    def __init__(self):
        self.root = None

    def insert(self, key, value, current=None):
        if not self.root:
            self.root = Node(key, value)
        else:
            if not current:
                current = self.root

            if key < current.key:
                if not current.left:
                    current.left = Node(key, value)
                else:
                    self.insert(key, value, current.left)
            elif key > current.key:
                if not current.right:
                    current.right = Node(key, value)
                else:
                    self.insert(key, value, current.right)
            else:
                current.value = value

    @staticmethod
    def minimum(node):
        p = node
        while p.left is not None:
            p = p.left
        return p

    @staticmethod
    def maximum(node):
        p = node
        while p.right is not None:
            p = p.right
        return p

    def delete(self, key):
        return self._delete(self.root, key) if self.search(key) else print("Nie znaleziono klucza '{}'".format(key))

    def _delete(self, currentNode, key):
        if not currentNode:
            return currentNode

        if key < currentNode.key:
            currentNode.left = self._delete(currentNode.left, key)
        elif key > currentNode.key:
            currentNode.right = self._delete(currentNode.right, key)
        else:
            if not currentNode.left:
                p = currentNode.right
                currentNode = None
                return p
            elif not currentNode.right:
                p = currentNode.left
                currentNode = None
                return p

            successor = self.minimum(currentNode.right)
            currentNode.key = successor.key
            currentNode.right = self._delete(currentNode.right, successor.key)

        return currentNode

    def search(self, key):
        temp = self._search(key, self.root)
        return temp.value if self.root and temp else print("Nie znaleziono klucza '{}'".format(key))

    def _search(self, key, node):
        if not node:
            return None
        elif node.key == key:
            return node
        elif key < node.key:
            return self._search(key, node.left)
        else:
            return self._search(key, node.right)

    def height(self, node):
        if node is None:
            return 0
        else:
            return 1 + max(self.height(node.left), self.height(node.right))

    def _print_tree(self, node, lvl):
        if node:
            self._print_tree(node.right, lvl + 10)
            print()
            for i in range(10, lvl + 10):
                print(end=" ")
            print(node.key)
            self._print_tree(node.left, lvl + 10)

    def print_tree(self):
        print("==============")
        self._print_tree(self.root, 0)
        print("==============")

    def visit(self, node):
        print(f"({node.key} : {node.value})")

    def print_inorder(self, current):
        if current:
            self.print_inorder(current.left)
            self.visit(current)
            self.print_inorder(current.right)


def main():
    bst = BST()
    bst.insert(50, 'A')
    bst.insert(15, 'B')
    bst.insert(62, 'C')
    bst.insert(5, 'D')
    bst.insert(20, 'E')
    bst.insert(58, 'F')
    bst.insert(91, 'G')
    bst.insert(3, 'H')
    bst.insert(8, 'I')
    bst.insert(37, 'J')
    bst.insert(60, 'K')
    bst.insert(24, 'L')

    bst.print_tree()
    print("\n===Struktura drzewa w kolejności rosnącej===\n")
    bst.print_inorder(bst.root)
    print("\n\nElement pod kluczem 24: ", bst.search(24))
    bst.insert(15, 'AA')
    bst.insert(6, 'M')
    bst.delete(62)
    bst.insert(59, 'N')
    bst.insert(100, 'P')
    bst.delete(8)
    bst.delete(15)
    bst.insert(55, 'R')
    bst.delete(50)
    bst.delete(5)
    bst.delete(24)

    print("\n\n=============================")
    print("===Drzewo po modyfikacjach===")
    print("=============================\n\n")
    print('Wysokosc drzewa: ', bst.height(bst.root))
    print("\n===Struktura drzewa w kolejności rosnącej===\n")
    bst.print_inorder(bst.root)
    bst.print_tree()


if __name__ == "__main__":
    main()
