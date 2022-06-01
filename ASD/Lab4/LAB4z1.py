class Element:
    def __init__(self, key, value):
        self.key = key
        self.value = value

class HashTable:
    def __init__(self,size= 10):
        self.size = size
        self.tab = [None for i in range(size)]
        self.c1 = 1
        self.c2 = 0

    def key_from_string(self, key):
        if isinstance(key, str):
            sum = 0
            for char in key:
                sum += ord(char)
            return sum % self.size
        else:
            return key % self.size
        
    def search_key(self, key):
        none_found = None
        k_val = self.key_from_string(key)
        if self.tab[k_val] is not None:
            if self.tab[k_val].key == key:
                return k_val
        for i in range(self.size): 
            new_key = (k_val + self.c1*i + self.c2*i**2) % self.size 
            if self.tab[new_key] is None and none_found is None: 
                none_found = new_key
            elif self.tab[new_key] is not None:
                if self.tab[new_key].key == key: 
                    return new_key
        
        if none_found is not None:
            return none_found
        else:
            print("Tablica jest pełna")

    def search(self, key):
        k_val = self.key_from_string(key)
        if self.tab[k_val] is not None:
            if self.tab[k_val].key == key:
                return self.tab[k_val].value
        
        for i in range(self.size): 
            new_key = (self.key_from_string(key) + self.c1*i + self.c2*i**2) % self.size 
            if self.tab[new_key] is not None:
                if self.tab[new_key].key == key: 
                    #Poprawione index wczesniej [k_val] na [new_key]
                    return self.tab[new_key].value
        print("Nie znalezionno elementu z kluczem '" + str(key) +"'" )
    
    def insert(self, key, value):
        elem = Element(key,value)
        k = elem.key
        v = elem.value

        k_val = self.key_from_string(k)

        if self.tab[k_val] is None or self.tab[k_val].key == k:
            self.tab[k_val] = elem  
        else:
            k_val  = self.search_key(k)
            if k_val is not None:
                self.tab[k_val] = elem
            else:
                print("Nie udało się wstawić elementu " '({} : {})'.format(k,v))

    def remove(self,key):
        k_val = self.key_from_string(key)
        if self.tab[k_val] is not None:
            if self.tab[k_val].key == key:
                self.tab[k_val] = None
                return
        
        for i in range(self.size): 
            new_key = (self.key_from_string(key) + self.c1*i + self.c2*i**2) % self.size 
            #Dodano sprawdzenie czy nie jest Nonem
            if self.tab[new_key] is not None:
                if self.tab[new_key].key == key: 
                    self.tab[new_key] = None
                    return
        print("Nie znaleziono elementu który chcesz usunąć")
    
    def show_tab(self): 
        string = '[ '
        if self.tab.count(None) == self.size:
            print("Tablica jest pusta!")
            return
        else:
            for elem in self.tab:  
                if elem is not None:
                  string += '({} : {}) '.format(elem.key,elem.value)
                else:
                  string += '({})  '.format(None)
        string += ']'
        print(string)     

    def __str__(self):
        string = ''
        if self.tab.count(None) == self.size:
            print("Tablica jest pusta!")
            return
        else:
            for elem in self.tab:  
                if elem is not None:
                  string += '\n({} : {})'.format(elem.key,elem.value)
            return string



def main():
  print("\n\n\n-------|main1|--------\n\n\n")
  tab = HashTable(13)
  alfabet = list(map(chr, range(97, 123)))
  print("Wstawianie 15 elementow do tablicy: \n")
  for i in range(1,16):
    if i == 6:
      tab.insert(i+12,alfabet[i])
    elif i ==7:
      tab.insert(i+24,alfabet[i])
    else:
      tab.insert(i,alfabet[i])
  print(tab)
  print("\nDana znajdujaca się pod kluczem '5':", tab.search(5))
  
  print("\nDana znajdujaca się pod kluczem '14':")
  print(tab.search(14))
  print("\nNadpisanie klucza '5' wartością 'nadpisanie' ")
  tab.insert(5,"nadpisanie")
  print("Dana pod kluczem '5': ",tab.search(5))
  tab.remove(5)
  print("\nTablica po usunęciu wartości pod kluczem '5':")
  tab.show_tab()
  print("\nDana znajdujaca się pod kluczem '5':")
  tab.search(5)
  print("Wstawienie danej 'A' pod kluczem 'test'...\n")
  tab.insert('A','test')
  print("Tablica po wstawieniu wartości: ")
  print(tab)

def main2():
  print("\n\n\n-------|main2|--------\n\n\n")
  tab = HashTable(13)
  alfabet = list(map(chr, range(97, 123)))
  print("Wstawianie 15 elementow do tablicy: \n")
  for i in range(1,16):
      tab.insert(i*13,alfabet[i])
  print(tab)
  tab.show_tab()

def main3():
  print("\n\n\n-------|main3|--------\n\n\n")
  tab = HashTable(13)
  tab.c1 = 0
  tab.c2 = 1
  alfabet = list(map(chr, range(97, 123)))
  print("Wstawianie 15 elementow do tablicy: \n")
  for i in range(1,16):
      tab.insert(i*13,alfabet[i])
  print(tab)
  tab.show_tab()
  
# Po zmianie paramertów c1 i c2 tablica nie wypełniła się w pełni




if __name__ == "__main__":
    main()
    main2()
    main3()