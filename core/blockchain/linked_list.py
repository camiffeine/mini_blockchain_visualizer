class Node:
    """
    Represents a single node in a linked list.
    
    Each node contains a reference to a Block and a reference to the next node.
    Nodes form the structural basis of the blockchain's linked list storage.
    
    Attributes:
        block: The Block object stored in this node
        next: Reference to the next Node in the chain (or None if last node)
    """
    def __init__(self):
        self.block = None
        self.next = None

class LinkedList:
    """
    Implements a singly-linked list data structure for storing blockchain blocks.
    
    The LinkedList stores blocks in sequential order, with each node pointing to
    the next block in the chain. This structure enables efficient traversal and
    maintainsthe chronological order of blocks.
    
    Attributes:
        head: The first node in the list (or None if empty)
        tail: The last node in the list (or None if empty)
        length: The number of nodes currently in the list
    """
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def append(self, node: Node):
        """
        Append a node to the end of the linked list.
        
        Updates head/tail pointers and increments length counter.
        
        Args:
            node: The Node to append
        """
        if not self.head:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.length += 1

    def remove(self, node: Node):
        """
        Remove a node from the linked list.
        
        Handles removal from head, middle, and tail positions. Updates pointers
        and decrements length counter.
        
        Args:
            node: The Node to remove
        """
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

    def find(self, node: Node):
        """
        Find a node in the linked list.
        
        Args:
            node: The Node to search for
            
        Returns:
            bool: True if node is in the list, False otherwise
        """
        current = self.head
        while current:
            if current == node:
                return True
            current = current.next
        return False

    def iterate(self):
        """
        Iterate over all nodes in the linked list.
        
        Generator method that yields nodes in sequence from head to tail.
        Can be used in for loops to traverse the list.
        
        Yields:
            Node: The next node in the chain
        """
        current = self.head
        while current:
            yield current
            current = current.next

    def to_list(self):
        """
        Convert the linked list to a Python list of nodes.
        
        Creates a snapshot of all nodes in the linked list as a standard Python list.
        Useful for bulk operations or when list-style access is needed.
        
        Returns:
            list: A list containing all nodes from head to tail
        """
        result = []
        current = self.head
        while current:
            result.append(current)
            current = current.next
        return result