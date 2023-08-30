# Name: Ngoc-Thao Ly
# OSU Email: lyng@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 5
# Due Date: 08/07/2023
# Description: File contains a class that implements a heap data structure using dynamic arrays as a base. The first
# value in the heap should always be the minimum. There is also a function in this file that takes a dynamic array,
# reorganizes it like a heap data structure and uses the heapsort algorithm to sort the dynamic array in descending
# order.

from dynamic_array import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initialize a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._heap = DynamicArray()

        # populate MH with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MH content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        heap_data = [self._heap[i] for i in range(self._heap.length())]
        return 'HEAP ' + str(heap_data)

    @staticmethod
    def _find_parent(node_idx) -> int:
        """Returns the index of node_idx's parent
        :param node_idx: index of a node
        :return: index of desired node
        """
        return (node_idx - 1) // 2

    def add(self, node: object) -> None:
        """
        Adds a new object to the heap and maintains heap property
        :param node: object to be added to the heap
        """
        self._heap.append(node)
        node_idx = self._heap.length() - 1
        par_idx = self._find_parent(node_idx)

        while par_idx >= 0:
            node_val = self._heap.get_at_index(node_idx)
            par_val = self._heap.get_at_index(par_idx)
            if par_val > node_val:
                self._heap.set_at_index(node_idx, par_val)
                self._heap.set_at_index(par_idx, node_val)
            node_idx, par_idx = par_idx, self._find_parent(par_idx)

    def is_empty(self) -> bool:
        """
        Determines whether the heap is empty
        :return: returns True if the heap is empty; otherwise, returns False
        """
        return self._heap.is_empty()

    def get_min(self) -> object:
        """
        Returns the object with the minimum key from the heap without removing it
        :return: object from heap
        """
        if self.is_empty():
            raise MinHeapException
        return self._heap.get_at_index(0)

    @staticmethod
    def _obtain_children(idx) -> tuple:
        """
        Returns the index value of the left and right child, given a parent index
        :param idx: index of parent object
        :return: a tuple containing the left and right child's indices
        """
        return 2 * idx + 1, 2 * idx + 2

    def _smallest_child(self, left_idx, right_idx, length):
        """
        Returns the index of the smaller object of two children
        :param left_idx: the index of the left child
        :param right_idx: the index of the right child
        :param length: the domain to be considered in the heap
        :return:
        """
        if left_idx < length and right_idx < length:
            child_1 = self._heap.get_at_index(left_idx)
            child_2 = self._heap.get_at_index(right_idx)
            if child_1 <= child_2:
                return left_idx
            return right_idx
        if left_idx < length:
            return left_idx
        if right_idx < length:
            return right_idx

    def percolate_down(self, parent_idx=0, length=None) -> None:
        """
        Percolates down the heap starting at the parent index
        :param parent_idx: starting index
        :param length: size of the heap
        :return:
        """
        if self.is_empty():
            return
        if length is None:
            length = self._heap.length()
        parent_val = self._heap.get_at_index(parent_idx)
        child_1, child_2 = self._obtain_children(parent_idx)

        while child_1 < length or child_2 < length:
            child_idx = self._smallest_child(child_1, child_2, length)
            child_val = self._heap.get_at_index(child_idx)
            if parent_val > child_val:
                self._heap.set_at_index(parent_idx, child_val)
                self._heap.set_at_index(child_idx, parent_val)
            parent_idx = child_idx
            child_1, child_2 = self._obtain_children(parent_idx)
            parent_val = self._heap.get_at_index(parent_idx)

    def remove_min(self) -> object:
        """
        Returns the object with the minimum key and removes it from the heap.
        :return: returns object with the minimum key
        """
        min_val = self.get_min()
        length = self._heap.length() - 1
        last_idx = length

        # swap the first and last values
        parent_val = self._heap.get_at_index(last_idx)
        self._heap.set_at_index(0, parent_val)
        self._heap.remove_at_index(last_idx)

        self.percolate_down()
        return min_val

    def build_heap(self, da: DynamicArray) -> None:
        """
        Builds a proper minheap given a dynamic array of objects
        :param da: dynamic array of objects in any order
        """
        self._heap = DynamicArray()
        if da:
            for node in da:
                self._heap.append(node)
        heap_length = self._heap.length()
        idx = heap_length // 2 - 1
        while idx >= 0:
            self.percolate_down(idx)
            idx -= 1

    def size(self) -> int:
        """
        Returns the number of items currently stored in the heap
        :return: number of items in the heap
        """
        return self._heap.length()

    def clear(self) -> None:
        """
        Clears the contents of the heap
        """
        self._heap = DynamicArray()


def da_smallest_child(da: DynamicArray, left_idx: int, right_idx: int, length: int) -> int:
    """
    Returns the index of the smaller object of two children
    :param da: dynamic array of objects representing a heap
    :param left_idx: the index of the left child
    :param right_idx: the index of the right child
    :param length: the domain to be considered in the dynamic array
    :return:
    """
    if left_idx < length and right_idx < length:
        child_1 = da.get_at_index(left_idx)
        child_2 = da.get_at_index(right_idx)
        if child_1 <= child_2:
            return left_idx
        return right_idx
    if left_idx < length:
        return left_idx
    if right_idx < length:
        return right_idx


def heapsort(da: DynamicArray) -> None:
    """
    Sorts a dynamic array in descending order using the heapsort algorithm
    :param da: dynamic array to be sorted
    """
    da_length = da.length()
    idx = da_length // 2 - 1
    # Sort the DA in MinHeap order
    while idx >= 0:

        # Percolate
        parent_idx = idx
        parent_val = da.get_at_index(parent_idx)
        child_1 = 2 * parent_idx + 1
        child_2 = child_1 + 1
        while child_1 < da_length or child_2 < da_length:
            child_idx = da_smallest_child(da, child_1, child_2, da_length)
            child_val = da.get_at_index(child_idx)
            if parent_val > child_val:
                da.set_at_index(parent_idx, child_val)
                da.set_at_index(child_idx, parent_val)
            parent_idx = child_idx
            child_1 = 2 * parent_idx + 1
            child_2 = child_1 + 1
            parent_val = da.get_at_index(parent_idx)
        idx -= 1

    # Sort the dynamic array in descending order
    last_idx = da.length() - 1

    while last_idx > 0:
        first_val = da.get_at_index(0)
        last_val = da.get_at_index(last_idx)
        da.set_at_index(0, last_val)
        da.set_at_index(last_idx, first_val)

        # Percolate
        parent_idx = 0
        parent_val = da.get_at_index(parent_idx)
        child_1 = 1
        child_2 = 2
        while child_1 < last_idx or child_2 < last_idx:
            child_idx = da_smallest_child(da, child_1, child_2, last_idx)
            child_val = da.get_at_index(child_idx)
            if parent_val > child_val:
                da.set_at_index(parent_idx, child_val)
                da.set_at_index(child_idx, parent_val)
            parent_idx = child_idx
            child_1 = 2 * parent_idx + 1
            child_2 = child_1 + 1
            parent_val = da.get_at_index(parent_idx)
        last_idx -= 1

