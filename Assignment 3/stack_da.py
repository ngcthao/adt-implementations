# Name: Ngoc-Thao Ly
# OSU Email: lyng@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 3
# Due Date: 07/24/2023
# Description: This file contains a Stack class that uses a Dynamic Array data structure as a base to implement
# the functionalities of a stack ADT, such as the ability to push and pop values.


from dynamic_array import *


class StackException(Exception):
    """
    Custom exception to be used by Stack class
    DO NOT CHANGE THIS METHOD IN ANY WAY
    """
    pass


class Stack:
    def __init__(self):
        """
        Init new stack based on Dynamic Array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._da = DynamicArray()

    def __str__(self) -> str:
        """
        Return content of stack in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "STACK: " + str(self._da.length()) + " elements. ["
        out += ', '.join([str(self._da[i]) for i in range(self._da.length())])
        return out + ']'

    def is_empty(self) -> bool:
        """
        Return True is the stack is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._da.is_empty()

    def size(self) -> int:
        """
        Return number of elements currently in the stack
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._da.length()

    # -----------------------------------------------------------------------

    def push(self, value: object) -> None:
        """
        Adds a new element to the top of the stack
        :param value: the value to be added
        """
        self._da.append(value)

    def pop(self) -> object:
        """
        Removes the top element from the stack and returns its value
        :return: the top element from the stack
        """
        idx = self._da.length() - 1
        pop_val = self.top()
        self._da.remove_at_index(idx)
        return pop_val

    def top(self) -> object:
        """
        Returns the value of the top element from the stack
        :return: the top element from the stack
        """
        idx = self._da.length() - 1
        if idx < 0:
            raise StackException
        return self._da.get_at_index(idx)

