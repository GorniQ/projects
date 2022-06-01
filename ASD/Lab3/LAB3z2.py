class Element:
    def __init__(self, size=5):
        self.tab = [None for i in range(size)]
        self.size = size
        self.numElements = 0
        self.next = None

    def insert_el(self, data, index):
        if self.tab[index] is None:
            self.tab[index] = data
        else:
            self.tab = self.tab[:index] + [data] + self.tab[index:]

    def pop_el(self, index):
        temp = self.tab[index]
        self.tab[index] = None
        return temp

    def append_el(self, data):
        a = 0
        for i in range(self.size):
            if a == self.numElements:
                self.tab[i+1] = data
                self.numElements += 1
                break
            elif self.tab[i] is not None:
                a += 1

    def pushNonesToEnd(self):
        k = 0

        for i in self.tab:
            if i is not None:
                self.tab[k] = i
                k += 1

        for i in range(k, self.size):
            self.tab[i] = None


class UnrolledLinkedList:
    def __init__(self, size=5):
        self.lst = Element(size)

    def get(self, index):
        lst = self.lst
        ctr = 0
        temp = index
        while lst is not None:
            ctr += lst.numElements
            if ctr >= index and temp <= lst.numElements:
                # Dla usuwania v1.0
                # a = 0
                # for i in range(lst.size):
                #     if a == temp and lst.tab[i] is not None:
                #         return lst.tab[i]
                #     elif lst.tab[i] is not None:
                #         a += 1

                # Dla usuwania v2.0
                return lst.tab[temp]

            else:
                temp -= lst.numElements
                lst = lst.next

    def insert(self, data, index):

        ctr = 0
        temp = index
        lst = self.lst
        while lst is not None:
            ctr += lst.numElements

            # Odpowiednia tablica
            if ctr >= index:
                # Jeżeli pełna -> realokacja
                if lst.numElements == lst.size:
                    newtab = Element(lst.size)
                    i = 0
                    for el in range(lst.size):
                        if el >= lst.size/2:
                            newtab.insert_el(lst.pop_el(el), i)
                            lst.insert_el(None, el)
                            newtab.numElements += 1
                            lst.numElements += -1
                            i += 1
                    newtab.next = lst.next
                    lst.next = newtab
                    self.insert(data, index)
                # Jeżeli nie wstaw element
                else:
                    lst.insert_el(data, temp)
                    lst.numElements += 1
                return
            # Zmiana tablicy
            else:
                temp -= lst.numElements
                lst = lst.next

        # Wyrzucenie błędu gdy indeks jest za duży
        print("Podano za duzy indeks, nie wstawiono elemntu")

    def delete(self, index):
        lst = self.lst
        ctr = 0
        temp = index
        while lst is not None:
            ctr += lst.numElements

            # Odpowiednia tablica
            if ctr >= index and temp <= lst.numElements:
                # Usuwanie elementu v1.0 (bez przesuwania Noneów)
                # a = 0
                # for i in range(lst.size):
                #     if a == temp and lst.tab[i] is not None:
                #         lst.tab[i] = None
                #         break
                #     elif lst.tab[i] is not None:
                #         a += 1

                # Usuwanie elementu v2.0
                lst.tab[temp] = None
                lst.pushNonesToEnd()
                lst.numElements -= 1

                # Sprawdzanie czy tablica jest zbyt pusta
                if lst.numElements < lst.size/2:
                    lst.insert_el(lst.next.pop_el(0), temp+1)
                    lst.next.numElements -= 1

                    # Sprawdzanie czy następna tablica jest zbyt pusta
                    if lst.next.numElements < lst.next.size/2:
                        lst.pushNonesToEnd()
                        lista = lst.next.tab
                        for i in range(lst.next.size):
                            if lista[i] is not None:
                                lst.append_el(lista[i])
                        lst.next = lst.next.next
                    else:
                        lst.next.pushNonesToEnd()
                break

            # Następna tablica
            else:
                temp -= lst.numElements
                lst = lst.next

    def show(self):
        n = self.lst
        string = ''
        while (n != None):
            for i in range(n.size):
                if n.tab[i] is not None:
                    string += '{}, '.format(n.tab[i])
            n = n.next
        print(string)

    def show_tab(self):
        n = self.lst
        string = ''
        while (n != None):
            string += '\nTablica:\n'
            for i in range(n.size):
                string += '{},  '.format(n.tab[i])
            n = n.next
        print(string)


def main():
    print("Tworzenie listy i dodanie 9 elementów...")
    lst = UnrolledLinkedList(6)
    for i in range(9):
        lst.insert(i, i)

    lst.show_tab()
    print("\n\nElement pod indeksem 4:")
    print(lst.get(4))
    print("\n\nDodawnie elementów:\n'dana1'-> indeks 1\n'dana2'-> indeks 8\n")
    lst.insert("dana1", 1)
    lst.insert("dana2", 8)
    lst.show_tab()
    print("\n\nUsunięcie 1 i 2 elementu...")
    lst.delete(1)
    lst.delete(2)
    print("Tablice po usunieciu:")
    lst.show_tab()
    print("\n\nTablice bez None'ów:")
    lst.show()


main()
