import random


class DictHash:
    def __init__(self, size):
        self.table = {}
    def store(self, key, value):
        self.table[key] = value
    def search(self, key):
        if key in self.table:
            return self.table[key]
        raise KeyError
    def __getitem__(self, key):
        return self.table[key]
    def __contains__(self, key):
        return key in self.table

class Node:
    """Noder till klassen Hashtable """
    def __init__(self, key = "", data = None):
        """key: nyckeln som anvands vid hashningen
        data: det objekt som ska hashas in"""
        self.key = key
        self.data = data

class HashtableAbstract: # abstract
    primes = [53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869, 3145739, 6291469, 12582917, 25165843, 50331653, 100663319, 201326611, 402653189, 805306457, 1610612741]
    def __init__(self, size):
        """size: hashtabellens storlek"""
        self.size = size if size > 0 else 1
        self.table = [None] * size
        self.prime = next(p for p in self.primes if p > size * 2) # first prime > 2*size
        self.a = random.randrange(1, self.prime)
        self.b = random.randrange(0, self.prime)
    
    def store(self, key, data):
        pass
    
    def search(self, key):
        pass
        
    def hashfunction(self, key):
        """key: nyckeln
        Beräknar hashfunktionen för key"""
        hash_int = 0
        if type(key) != str:
            key = str(key)
        for c in key:
            hash_int = hash_int * 32 + ord(c)
        return (self.a * hash_int + self.b) % self.prime % self.size
    
    def __getitem__(self, key):
        return self.search(key)
    
    def __setitem__(self, key, data):
        self.store(key, data)
    
    def __contains__(self, key):
        try:
            self.search(key)
            return True
        except KeyError:
            return False

class Hashtable(HashtableAbstract): # linear probing
    def store(self, key, data):
        """key: nyckeln
        data: objektet som ska lagras
        Stoppar in "data" med nyckeln "key" i tabellen."""
        hash_code = self.hashfunction(key)
        if self.table[hash_code] == None:
            self.table[hash_code] = Node(key, data)
        elif self.table[hash_code].key == key:
            self.table[hash_code].data = data
        else:
            for _ in range(self.size):
                hash_code = (hash_code + 1) % self.size
                if self.table[hash_code] == None:
                    self.table[hash_code] = Node(key, data)
                    return
                elif self.table[hash_code].key == key:
                    self.table[hash_code].data = data
                    return
            raise Exception("Hashtable full")
                    
    def search(self, key):
        """key: nyckeln
        Hamtar det objekt som finns lagrat med nyckeln "key" och returnerar det.
        Om "key" inte finns ska vi få en Exception, KeyError """
        hash_code = self.hashfunction(key)
        if self.table[hash_code] == None:
            raise KeyError
        elif self.table[hash_code].key == key:
            return self.table[hash_code].data
        else:
            for _ in range(self.size):
                hash_code = (hash_code + 1) % self.size
                if self.table[hash_code] == None:
                    raise KeyError
                elif self.table[hash_code].key == key:
                    return self.table[hash_code].data
            raise KeyError
        
class LinkedNode:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.next = None
    
class HashtableChaining(HashtableAbstract): # chaining
    def store(self, key, data):
        """key: nyckeln
        data: objektet som ska lagras
        Stoppar in "data" med nyckeln "key" i tabellen."""
        hash_code = self.hashfunction(key)
        current_node: LinkedNode = self.table[hash_code]
        if current_node is None:
            self.table[hash_code] = LinkedNode(key, data)
            return
        while True:
            if current_node.key == key:
                current_node.data = data
                return
            if current_node.next is None:
                current_node.next = LinkedNode(key, data)
                return
            current_node = current_node.next
            
    def search(self, key):
        """key: nyckeln
        Hamtar det objekt som finns lagrat med nyckeln "key" och returnerar det.
        Om "key" inte finns ska vi få en Exception, KeyError """
        hash_code = self.hashfunction(key)
        current_node: LinkedNode = self.table[hash_code]
        while current_node is not None:
            if current_node.key == key:
                return current_node.data
            current_node = current_node.next
        raise KeyError