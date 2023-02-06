class Node:
    def __init__(self, value):
        self._value = value
        self._next = None

class LinkedQ:
    def __init__(self):
        self._first = None
        self._last = None
        self._size = 0

    def enqueue(self, value):
        
        # Vi behöver dela upp det i två cases:
        # 1) När det inte finns en FIRST
        # 2) När det finns en First
        self._size += 1
        tmp = Node(value)

        if self._last == None:
            self._first = tmp
            self._last = tmp
        
        else:
            self._last._next = tmp
            self._last = tmp
    
    def dequeue(self):
        self._size -= 1
        first_node_value = self._first._value
        if self._first._next != None:
            self._first = self._first._next
        else:
            self._first = None
            self._last = None
        
        return first_node_value

    def isEmpty(self):
        if self._first == None:
            return True
        else:
            return False

    def size(self):
        return self._size