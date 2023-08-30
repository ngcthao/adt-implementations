# Name: Ngoc-Thao Ly
# OSU Email: lyng@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 3
# Due Date: 07/24/2023
# Description: This file contains a LinkedList data structure that allows the user to manipulate the data nodes with
# a variety of methods such as insertion at any index and slicing.


from SLNode import *


class SLLException(Exception):
    """
    Custom exception class to be used by Singly Linked List
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class LinkedList:
    def __init__(self, start_list=None) -> None:
        """
        Initialize new linked list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._head = SLNode(None)

        # populate SLL with initial values (if provided)
        # before using this feature, implement insert_back() method
        if start_list is not None:
            for value in start_list:
                self.insert_back(value)

    def __str__(self) -> str:
        """
        Return content of singly linked list in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = 'SLL ['
        node = self._head.next
        while node:
            out += str(node.value)
            if node.next:
                out += ' -> '
            node = node.next
        out += ']'
        return out

    def length(self) -> int:
        """
        Return the length of the linked list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        length = 0
        node = self._head.next
        while node:
            length += 1
            node = node.next
        return length

    def is_empty(self) -> bool:
        """
        Return True is list is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return not self._head.next

    # ------------------------------------------------------------------ #

    def insert_front(self, value: object) -> None:
        """
        Adds a new node at the beginning of the list
        :param value: new object to be inserted
        """
        new_node = SLNode(value, self._head.next)
        self._head.next = new_node

    def insert_back(self, value: object) -> None:
        """
        Adds a new node at the end of the list
        :param value: new object to be inserted
        """
        new_node = SLNode(value)
        node = self._head
        cont_iter = True  # continue iterating
        while cont_iter:
            if node.next is None:
                node.next = new_node
                cont_iter = False
            node = node.next

    def idx_search(self, index) -> tuple:
        """
        Helper function used to obtain the node right before the desired index
        :index: the index of the desired node
        :return: returns a tuple containin a boolean based on whether the search was successful and the node, if found
        """
        node = self._head

        while index > 0 and node.next is not None:
            node = node.next
            index -= 1

        if index == 0:
            return True, node

        return False, None

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Insert a new node at the specified index position in the linked list
        :param index: index of desired position
        :param value: value to be inserted
        """
        val_found, node = self.idx_search(index)
        if not val_found:
            raise SLLException

        new_node = SLNode(value)
        if node.next is None:
            node.next = new_node
        else:
            new_node.next = node.next
            node.next = new_node

    def remove_at_index(self, index: int) -> None:
        """
        Removes the node at the desired index position in the linked list
        :param index: index of the node to be removed
        """
        val_found, node = self.idx_search(index)

        if not val_found or node.next is None:
            raise SLLException

        node.next = node.next.next

    def remove(self, value: object) -> bool:
        """
        Removes the first node that matches the value parameter
        :param value: value of the node to be removed, if it exists
        :return: returns True if a node was removed and False otherwise
        """
        node = self._head
        if node.next is None:
            return False

        while node.next.value != value:
            node = node.next
            if node.next is None:
                return False

        node.next = node.next.next
        return True

    def count(self, value: object) -> int:
        """
        Counts the number of elements in the list that match the value parameter
        :param value: value to be searched for
        :return: the number of times the value param appears in the list
        """
        node = self._head
        count = 0

        while node.next is not None:
            node = node.next
            if node.value == value:
                count += 1
        return count

    def find(self, value: object) -> bool:
        """
        Returns a boolean based on whether the value parameter exists in the list
        :param value: value to be searched for
        :return: boolean based on the existence of the value parameter in the list
        """
        if self.count(value) > 0:
            return True
        return False

    def slice(self, start_index: int, size: int) -> "LinkedList":
        """
        Creates a new LinkedList containing a slice of the requested nodes from the original list
        :param start_index: the index of the first desired node
        :param size: the size of the desired slice
        :return: the slice of desired nodes as a linked list
        """
        if size < 0:
            raise SLLException

        # Obtain the node located at the desired indices
        start_found, start_node = self.idx_search(start_index)
        end_found, end_node = self.idx_search(start_index + size - 1)

        if not start_found or start_node.next is None:
            raise SLLException
        if size == 0:   # Edge case: valid index, but size of 0
            return LinkedList()
        if not end_found or end_node.next is None:
            raise SLLException

        # Create new Linked List containing the desired elements
        start_node = start_node.next
        sliced_list = LinkedList()
        orig_node = start_node
        sliced_node = sliced_list._head

        while size > 0:
            new_node = SLNode(orig_node.value)
            sliced_node.next = new_node
            orig_node = orig_node.next
            sliced_node = sliced_node.next
            size -= 1

        return sliced_list

