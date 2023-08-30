# Name: Ngoc-Thao Ly
# OSU Email: lyng@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 2
# Due Date: 07/17/2023
# Description: File contains implemented Bag methods that make use of DynamicArray methods to create an ADT class
# that may be used for unordered lists.


from dynamic_array import *


class Bag:
    def __init__(self, start_bag=None):
        """
        Init new bag based on Dynamic Array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._da = DynamicArray()

        # populate bag with initial values (if provided)
        # before using this feature, implement add() method
        if start_bag is not None:
            for value in start_bag:
                self.add(value)

    def __str__(self) -> str:
        """
        Return content of stack in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "BAG: " + str(self._da.length()) + " elements. ["
        out += ', '.join([str(self._da.get_at_index(_))
                          for _ in range(self._da.length())])
        return out + ']'

    def size(self) -> int:
        """
        Return total number of items currently in the bag
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._da.length()

    # -----------------------------------------------------------------------

    def add(self, value: object) -> None:
        """
        Adds a new element to the Bag.
        :param value: an object value to be added to the Bag object
        :return: None
        """
        self._da.append(value)

    def remove(self, value: object) -> bool:
        """
        Removes a single instance of the object, value, from the Bag.
        :param value: an object value to be removed from the Bag object
        :return: returns True if an object was removed and False otherwise
        """
        for idx in range(self._da.length()):
            if self._da.get_at_index(idx) == value:
                self._da.remove_at_index(idx)
                return True
        return False

    def count(self, value: object) -> int:
        """
        Counts the number of elements in the Bag that match the value parameter.
        :param value: an object to be found and counted in Bag
        :return: returns the number of times value is found in the Bag
        """
        count = 0
        for idx in range(self._da.length()):
            if self._da.get_at_index(idx) == value:
                count += 1
        return count

    def clear(self) -> None:
        """
        Empties the bag of all elements
        :return: None
        """
        self._da = DynamicArray()

    def equal(self, second_bag: "Bag") -> bool:
        """
        Compares the elements of two Bag objects without regard to order
        :param second_bag: a Bag object to compare with
        :return: returns True if the bags contain the same number of elements and contain the same elements
        """
        if self._da.length() != second_bag._da.length():
            return False
        for idx in range(self._da.length()):
            curr = self._da.get_at_index(idx)
            if self.count(curr) != second_bag.count(curr):
                return False
            curr = second_bag._da.get_at_index(idx)
            if self.count(curr) != second_bag.count(curr):
                return False
        return True

    def __iter__(self):
        """
        Creates an iterator for loops
        :return: returns the object
        """
        self.index = 0
        return self

    def __next__(self):
        """
        Obtains the next value in the Bag and increments the iterator
        :return: returns the next object or element
        """
        try:
            val = self._da.get_at_index(self.index)
        except DynamicArrayException:
            raise StopIteration
        self.index += 1
        return val