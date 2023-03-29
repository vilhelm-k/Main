class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedQ:
    def __init__(self):
        self.first = None
        self.last = None
        self.length = 0

    def enqueue(self, value):
        new_node = Node(value)
        if self.last is None:
            self.first = new_node
            self.last = new_node
        else:
            self.last.next = new_node
            self.last = new_node
        self.length += 1

    def dequeue(self):
        if self.is_empty():
            return None
        first_node_value = self.first.value
        if self.first.next is not None:
            self.first = self.first.next
        else:
            self.first = None
            self.last = None
        self.length -= 1
        return first_node_value

    def is_empty(self):
        return self.first is None

    def size(self):
        return self.length

    def peek(self):
        return self.first.value if not self.is_empty() else None

    def __str__(self):
        result = ""
        if not self.is_empty():
            current_node = self.first
            result += str(current_node.value)
            while current_node.next is not None:
                current_node = current_node.next
                result += str(current_node.value)
        return result
