# Name: Ngoc-Thao Ly
# OSU Email: lyng@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 3
# Due Date: 07/24/2023
# Description: This file contains a Stack class that uses a Linked List data structure as a base to implement
# the functionalities of a stack ADT, such as the ability to push and pop values.


from SLNode import SLNode


class StackException(Exception):
    """
    Custom exception to be used by Stack class
    DO NOT CHANGE THIS METHOD IN ANY WAY
    """
    pass


class Stack:
    def __init__(self) -> None:
        """
        Initialize new stack with head node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._head = None

    def __str__(self) -> str:
        """
        Return content of stack in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = 'STACK ['
        if not self.is_empty():
            node = self._head
            out = out + str(node.value)
            node = node.next
            while node:
                out = out + ' -> ' + str(node.value)
                node = node.next
        return out + ']'

    def is_empty(self) -> bool:
        """
        Return True is the stack is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._head is None

    def size(self) -> int:
        """
        Return number of elements currently in the stack
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        node = self._head
        length = 0
        while node:
            length += 1
            node = node.next
        return length

    # -----------------------------------------------------------------------

    def push(self, value: object) -> None:
        """
        Adds a new element to the top of the stack.
        :param value: object to be added to the stack
        """
        node = SLNode(value)
        node.next = self._head
        self._head = node

    def pop(self) -> object:
        """
        Returns and removes the value at the top of the stack.
        :returns: returns the value of the most recently added element
        """
        if self._head is None:
            raise StackException
        node = self._head
        self._head = self._head.next
        return node.value

    def top(self) -> object:
        """
        Returns the value of the top element of the stack.
        :returns: returns the value of the most recently added element
        """
        if self._head is None:
            raise StackException
        return self._head.value


