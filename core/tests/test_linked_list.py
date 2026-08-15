"""
Unit tests for LinkedList class.
"""

import pytest
from core.blockchain.linked_list import Node, LinkedList
from core.blockchain.block import Block
from core.blockchain.transaction import Transaction


class TestLinkedListNodeCreation:
    """Tests for LinkedList Node class."""

    def test_create_node(self):
        """Test creating a node."""
        node = Node()
        assert node.block is None
        assert node.next is None

    def test_node_can_hold_block(self):
        """Test that node can hold a block."""
        node = Node()
        block = Block(0, "0" * 64, [])
        node.block = block
        assert node.block == block


class TestLinkedListCreation:
    """Tests for LinkedList creation."""

    def test_create_empty_linked_list(self):
        """Test creating an empty linked list."""
        ll = LinkedList()
        assert ll.head is None
        assert ll.tail is None
        assert ll.length == 0

    def test_append_first_node(self):
        """Test appending the first node to an empty list."""
        ll = LinkedList()
        node = Node()
        node.block = Block(0, "0" * 64, [])
        
        ll.append(node)
        
        assert ll.head == node
        assert ll.tail == node
        assert ll.length == 1

    def test_append_multiple_nodes(self):
        """Test appending multiple nodes."""
        ll = LinkedList()
        nodes = []
        
        for i in range(3):
            node = Node()
            node.block = Block(i, "0" * 64, [])
            nodes.append(node)
            ll.append(node)
        
        assert ll.length == 3
        assert ll.head == nodes[0]
        assert ll.tail == nodes[2]

    def test_nodes_are_linked(self):
        """Test that nodes are properly linked in the list."""
        ll = LinkedList()
        node1 = Node()
        node2 = Node()
        node3 = Node()
        
        ll.append(node1)
        ll.append(node2)
        ll.append(node3)
        
        assert node1.next == node2
        assert node2.next == node3
        assert node3.next is None


class TestLinkedListRemoval:
    """Tests for LinkedList node removal."""

    def test_remove_node_from_middle(self):
        """Test removing a node from the middle of the list."""
        ll = LinkedList()
        node1 = Node()
        node2 = Node()
        node3 = Node()
        
        ll.append(node1)
        ll.append(node2)
        ll.append(node3)
        
        ll.remove(node2)
        
        assert ll.length == 2
        assert node1.next == node3
        assert ll.tail == node3

    def test_remove_head_node(self):
        """Test removing the head node."""
        ll = LinkedList()
        node1 = Node()
        node2 = Node()
        
        ll.append(node1)
        ll.append(node2)
        
        ll.remove(node1)
        
        assert ll.head == node2
        assert ll.length == 1

    def test_remove_tail_node(self):
        """Test removing the tail node."""
        ll = LinkedList()
        node1 = Node()
        node2 = Node()
        
        ll.append(node1)
        ll.append(node2)
        
        ll.remove(node2)
        
        assert ll.tail == node1
        assert ll.length == 1

    def test_remove_only_node(self):
        """Test removing the only node in the list."""
        ll = LinkedList()
        node = Node()
        ll.append(node)
        
        ll.remove(node)
        
        assert ll.head is None
        assert ll.tail is None
        assert ll.length == 0

    def test_remove_from_empty_list(self):
        """Test removing a node from an empty list does nothing."""
        ll = LinkedList()
        node = Node()
        
        ll.remove(node)
        
        assert ll.length == 0


class TestLinkedListFind:
    """Tests for LinkedList node finding."""

    def test_find_existing_node(self):
        """Test finding an existing node in the list."""
        ll = LinkedList()
        node1 = Node()
        node2 = Node()
        
        ll.append(node1)
        ll.append(node2)
        
        assert ll.find(node2) is True

    def test_find_nonexistent_node(self):
        """Test finding a node that's not in the list."""
        ll = LinkedList()
        node1 = Node()
        node2 = Node()
        node_not_in_list = Node()
        
        ll.append(node1)
        ll.append(node2)
        
        assert ll.find(node_not_in_list) is False

    def test_find_in_empty_list(self):
        """Test finding a node in an empty list."""
        ll = LinkedList()
        node = Node()
        
        assert ll.find(node) is False
