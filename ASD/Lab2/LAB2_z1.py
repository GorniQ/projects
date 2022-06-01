class Element:
    def __init__(self,data):
      self.data= data
      self.next= None

class LinkedList:
    def __init__(self):
      self.head = None

    def destroy(self):
      self.head = None

    def add(self, data):
      new_elem = Element(data)
      new_elem.next = self.head
      self.head= new_elem

    def remove(self):
      if self.head is None:
        print("Nie ma elementów do usunięcia")
        return
      self.head = self.head.next

    def is_empty(self):
      if self.head is None:
        return True
      return False
        
    def lenght(self):
      cur_el = self.head
      sum = 0
      if cur_el is not None:
        while cur_el.next is not None:
          sum += 1
          cur_el = cur_el.next
      return sum

    def get(self):
      elem = self.head
      return elem.data

    def show(self):
      if self.head is None:
        print("Lista jest pusta")
      else:
        list = []
        cur_el = self.head
        list.append(cur_el.data)
        while cur_el.next is not None:
          cur_el = cur_el.next
          list.append(cur_el.data)
        print(', \n'.join(map(str, list)))

    def add_end(self, data):
      new_elem = Element(data)
      if self.head is None:
        self.head = new_elem
      else:
        cur_el = self.head
        while cur_el.next is not None:
          cur_el = cur_el.next
        cur_el.next = new_elem

    def remove_end(self):
      if self.head is None:
        print("Nie ma elementów do usuniecia")
      else:
        cur_el = self.head
        while cur_el.next.next is not None:
          cur_el = cur_el.next
        cur_el.next = None

    def reverse(self):
      reversed_list = LinkedList()
      cur_el = self.head
      while cur_el is not None:
          reversed_list.add(cur_el.data)
          cur_el = cur_el.next
      self.head = reversed_list.head

    def take(self,n):
      if self.head is None:
        print("Lista nie ma elementów")
      elif self.lenght() <= n:
          return self.head()
      else:
        cur_el = self.head
        list = LinkedList()
        for i in range(n):
          list.add_end(cur_el.data)
          cur_el = cur_el.next
      return list

    def drop(self, n):
      list = LinkedList()
      if self.head is None:
        print("Lista nie ma elementów")
      elif self.lenght() <= n:
          return list
      else:
        cur_el = self.head
        counter = 1
        while cur_el.next is not None:
          cur_el = cur_el.next
          if counter >= n:
            list.add_end(cur_el.data)
          counter += 1
        return list

def main():

    lst = LinkedList()
    print("Sprawdzenie czy lista jest pusta:", lst.is_empty())
    print("Dodanie 4 elementów na poczetek listy:")
    lst.add(('PW', 'Warszawa', 1915))
    lst.add(('UW', 'Warszawa', 1915))
    lst.add(('UP', 'Poznań', 1919))
    lst.add(('PG', 'Gdańsk', 1945))
    lst.show()
    print("\nDodanie pozostałych elementów:")  
    lst.add_end(('UJ', 'Kraków', 1364))
    lst.add_end(('AGH', 'Kraków', 1919))
    lst.show()
    print("\nOdwrocenie listy:")
    lst.reverse()
    lst.show()
    print("\nUsuniecie pierwszego elementu:")
    lst.remove()
    lst.show()
    print("\nUsuniecie ostatniego elementu:")
    lst.remove_end()
    lst.show()
    print("\nDodanie usuniętych elementów elementu:")
    lst.add(('AGH', 'Kraków', 1919))
    lst.add_end(('PG', 'Gdańsk', 1945))
    lst.show()
    print("\nSprawdzenie czy lista jest pusta:", lst.is_empty())
    print("\nPierwszy element: ", lst.get())
    print("\nTake dla n=2:")
    lst.take(2).show()
    print("\nDrop dla n=3:")
    lst.drop(3).show()
    print("\nNiszczenie listy:")
    lst.destroy()
    lst.show()


if __name__ == "__main__":
    main()