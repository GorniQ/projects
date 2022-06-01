def realloc(tab, size):
    oldSize = len(tab)
    return [tab[i] if i<oldSize else None  for i in range(size)]

class Queue:
    def __init__(self,size= 5):
        self.tab = [None for i in range(size)]
        self.windex = 0
        self.rindex = 0
        self.size = size

    def is_empty(self):
        if self.windex == self.rindex:
            return True
        return False

    def peek(self):
      if self.is_empty():
        print("Kolejka jest pusta!")
      else:
        return self.tab[self.rindex]

    def dequeue(self):
      if self.is_empty():
          return None
      else:
          data = self.peek()
          self.tab[self.rindex] = None
          if self.rindex + 1 == self.size:
              self.rindex = 0
          else:
              self.rindex += 1
          return data

    def enqueue(self, data):
        #Sprawdzamy czy tablica jest pełna
        if ((self.windex + 1) % self.size == self.rindex):  

            #Realokacja tablicy
            newsize = 2 * self.size
            self.tab = realloc(self.tab, newsize)

            #Sprawdzamy czy windex przeniósł sie na początek tablicy
            #Jesli tak rozsuwamy tablicę
            if self.windex < self.rindex:
                for i in range(self.rindex,self.size):
                    self.tab[i + self.size] = self.tab[i]
                    self.tab[i] = None
                self.tab[self.windex] = data
                self.rindex += self.size
            else:
                self.tab[self.windex] = data
            
            self.size = newsize
            self.windex += 1

        else: 
            if self.windex + 1 == self.size:
                self.tab[self.windex] = data 
                self.windex = 0
            else:
                self.tab[self.windex] = data 
                self.windex += 1
    
    def show(self):
        if self.is_empty():
            print("Kolejka jest pusta")
        else:
            if self.windex > self.rindex:
                q = [i for i in self.tab if i != None] 
                print(', '.join(map(str, q)))
            else:
                l_windex = self.tab[:self.windex]
                r_rindex = self.tab[self.rindex:]
                print(', '.join(map(str, r_rindex)) +', ' + ', '.join(map(str, l_windex)))
    
    def show_tab(self): print(self.tab)
      

def main():
  queue = Queue()
  print("Dodanie 4 elementów:")
  queue.enqueue(0)
  queue.enqueue(1)
  queue.enqueue(2)
  queue.enqueue(3)
  print("\nKolejka:")
  queue.show()
  print("\nTablica:")
  queue.show_tab()
  print("\nPierwsza wpisana dana: ", queue.dequeue())
  print("\nTablica:")
  queue.show_tab()
  print("\nDruga wpisana dana: ", queue.peek())
  print("\nKolejka:")
  queue.show()
  print("\nTablica:")
  queue.show_tab()
  print("\nDodanie kojenych 4 elementów:")
  queue.enqueue(4)
  queue.enqueue(5)
  queue.enqueue(6)
  queue.enqueue(7)
  print("\nTablica:")
  queue.show_tab()
  print("\nKolejka:")
  queue.show()
  print("\nOpróżnianie kolejki...")
  while not queue.is_empty():
    print(queue.dequeue())

if __name__ == "__main__":
    main()