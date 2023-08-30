# Name: Ngoc-Thao Ly
# OSU Email: lyng@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 3
# Due Date: 07/24/2023
# Description: This file contains a Queue class that uses a Static Array data structure as a base to implement
# the functionalities of a queue ADT, such as the ability to enqueue and dequeue. The class also uses a circular buffer
# to optimize memory usage.


# Note: Changing any part of the pre-implemented methods (besides adding  #
#       default parameters) will cause the Gradescope tests to fail.      #


from static_array import StaticArray


class QueueException(Exception):
    """Custom exception to be used by Queue class."""
    pass


class Queue:
    def __init__(self) -> None:
        """Initialize new queue based on Static Array."""
        self._sa = StaticArray(4)
        self._front = 0
        self._back = -1
        self._current_size = 0

    def __str__(self) -> str:
        """Override string method to provide more readable output."""

        size = self._current_size
        out = "QUEUE: " + str(size) + " element(s). ["

        front_index = self._front
        for _ in range(size - 1):
            out += str(self._sa[front_index]) + ', '
            front_index = self._increment(front_index)

        if size > 0:
            out += str(self._sa[front_index])

        return out + ']'

    def is_empty(self) -> bool:
        """Return True if the queue is empty, False otherwise."""
        return self._current_size == 0

    def size(self) -> int:
        """Return number of elements currently in the queue."""
        return self._current_size

    def print_underlying_sa(self) -> None:
        """Print underlying StaticArray. Used for testing purposes."""
        print(self._sa)

    def _increment(self, index: int) -> int:
        """Move index to next position."""

        # employ wraparound if needed
        index += 1
        if index == self._sa.length():
            index = 0

        return index

    # ---------------------------------------------------------------------- #

    def resize(self, new_capacity) -> None:
        """
        Increases the capacity of the internal static array attribute, copies over the existing queue and moves the
        start of the array to the index 0.
        :param new_capacity: the new desired capacity of the internal static array attribute
        """
        if new_capacity < self._current_size:
            raise QueueException
        new_array = StaticArray(new_capacity)
        q_idx = self._front
        # Copy values to new array
        for idx in range(self._current_size):
            if self._sa.get(q_idx) is not None:
                new_array.set(idx, self._sa.get(q_idx))
            q_idx = self._increment(q_idx)
        # Replace static array with new array and update attributes
        self._sa = new_array
        self._front = 0
        self._back = self._current_size - 1

    def enqueue(self, value: object) -> None:
        """
        Adds a new value to the end of the queue and doubles array capacity if necessary.
        :param value: value to enter queue
        """
        if self._current_size == self._sa.length():
            self.resize(self._current_size * 2)
        self._current_size += 1
        self._back = self._increment(self._back)
        self._sa.set(self._back, value)

    def dequeue(self) -> object:
        """
        Removes and returns the value at the beginning of the queue.
        :return: returns the value of the element at the front of the queue
        """
        if self._current_size == 0:
            raise QueueException
        value = self._sa.get(self._front)
        self._front = self._increment(self._front)
        self._current_size -= 1

        return value

    def front(self) -> object:
        """
        Returns the value of the front element of the queue.
        :return: returns the value of the element at the front of the queue
        """
        if self._current_size == 0:
            raise QueueException
        return self._sa.get(self._front)
