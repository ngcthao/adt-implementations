# Name: Ngoc-Thao Ly
# OSU Email: lyng@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 3
# Due Date: 07/24/2023
# Description: This file contains a Queue class that uses a Linked List data structure as a base to implement
# # the functionalities of a Queue ADT, such as the ability to enqueue and dequeue values.


from SLNode import SLNode


class QueueException(Exception):
    """
    Custom exception to be used by Queue class
    DO NOT CHANGE THIS METHOD IN ANY WAY
    """
    pass


class Queue:
    def __init__(self):
        """
        Initialize new queue with head and tail nodes
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._head = None
        self._tail = None

    def __str__(self):
        """
        Return content of queue in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = 'QUEUE ['
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
        Return True is the queue is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._head is None

    def size(self) -> int:
        """
        Return number of elements currently in the queue
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        node = self._head
        length = 0
        while node:
            length += 1
            node = node.next
        return length

    # -----------------------------------------------------------------------

    def enqueue(self, value: object) -> None:
        """
        Adds a new value to the end of the queue.
        :param value: value to be added to the queue
        """
        new_node = SLNode(value)
        if self._head is None:
            self._head = new_node
            self._tail = self._head
        else:
            self._tail.next = new_node
            self._tail = new_node

    def dequeue(self) -> object:
        """
        Removes and returns the value of the front element of the queue
        :returns: returns the value of the element at the front of the queue
        """
        if self._head is None:
            raise QueueException
        val = self._head.value
        self._head = self._head.next
        return val

    def front(self) -> object:
        """
        Returns the value of the front element of the queue
        :return: returns the value of the element at the front of the queue
        """
        if self._head is None:
            raise QueueException
        return self._head.value

