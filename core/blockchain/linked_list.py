class Node:
    def __init__(self):
        self.block = None
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    # Append a node to the end of the linked list
    def append(self, node: Node):
        if not self.head:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.length += 1

    # Remove a node from the linked list
    def remove(self, node: Node):
        if not self.head:
            return

        if self.head == node:
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            self.length -= 1
            return

        current = self.head
        while current.next and current.next != node:
            current = current.next

        if current.next == node:
            current.next = node.next
            if node == self.tail:
                self.tail = current
            self.length -= 1

    # Find a node in the linked list
    def find(self, node: Node):
        current = self.head
        while current:
            if current == node:
                return True
            current = current.next
        return False

    # Iterate over the nodes in the linked list
    def iterate(self):
        current = self.head
        while current:
            yield current
            current = current.next

    # Convert the linked list to a list of nodes
    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current)
            current = current.next
        return result