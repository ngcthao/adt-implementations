# Name: Ngoc-Thao Ly
# OSU Email: lyng@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 08/15/2023
# Description: This file contains an implementation of a Hash Map data structure that resolves collisions through
# chaining.

from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)
from timethis import timethis
import random


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def hash_ret(self, key) -> int:
        """
        Returns the hash value of the key parameter
        :param key: key of desired object
        :return: returns the hash value of the key parameter
        """
        return self._hash_function(key) % self._capacity

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hashmap if it exists.
        Adds the new key/value pair if it does not already exist in the hashmap
        :param key: key of desired entry
        :param value: desired value for the corresponding key parameter
        """
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)

        idx = self.hash_ret(key)
        link_list = self._buckets.get_at_index(idx)
        node = link_list.contains(key)
        if node:
            node.value = value
        else:
            link_list.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hashmap
        :return: returns the number of empty buckets
        """
        empty_count = 0
        for idx in range(self._buckets.length()):
            if self._buckets.get_at_index(idx).length() == 0:
                empty_count += 1
        return empty_count

    def table_load(self) -> float:
        """
        Returns the table load factor based on the table capacity
        :return: the load factor of the hashmap
        """
        element_count = 0
        bucket_count = self._capacity
        for idx in range(bucket_count):
            element_count += self._buckets.get_at_index(idx).length()
        return element_count / bucket_count

    def clear(self) -> None:
        """
        Clears the hashmap of all key/value pairs
        """
        temp_hash = HashMap(self._capacity, self._hash_function)
        self._buckets = temp_hash._buckets
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hashmap to the desired capacity if it is prime. Otherwise, resizes to the next prime value
        :param new_capacity: the desired capacity of the table
        """
        if new_capacity < 1:
            return
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        temp_table = HashMap(function=self._hash_function)
        temp_table._buckets = DynamicArray()
        temp_table._capacity = new_capacity
        for _ in range(temp_table._capacity):
            temp_table._buckets.append(LinkedList())

        while self._buckets.length() != 0:
            link_list = self._buckets.pop()
            for node in link_list:
                temp_table.put(node.key, node.value)
        self._buckets = temp_table._buckets
        self._capacity = temp_table._capacity
        self._size = temp_table._size

    def get(self, key: str):
        """
        Returns the value of the desired key, if it exists. Returns None otherwise
        :param key: key of desired entry
        """
        idx = self.hash_ret(key)
        link_list = self._buckets.get_at_index(idx)
        node = link_list.contains(key)
        if node:
            return node.value

    def contains_key(self, key: str) -> bool:
        """
        Determines whether a key exists in the hashmap
        :param key: key of desired entry
        :return: Returns True if a key exists in the hashmap and False otherwise
        """
        idx = self.hash_ret(key)
        if self._buckets.get_at_index(idx).contains(key):
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes a key/value pair from the hashmap, if it exists and decreases hashmap size
        :param key: the desired key to be removed
        """
        idx = self.hash_ret(key)
        if self._buckets.get_at_index(idx).remove(key):
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Saves all the key/value pairs in the hashmap into a dynamic array
        :return: returns a dynamic array containing all existing key/value pairs
        """
        kv_array = DynamicArray()
        for idx in range(self._buckets.length()):
            link_list = self._buckets.get_at_index(idx)
            for node in link_list:
                kv_array.append((node.key, node.value))
        return kv_array


@timethis
def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    This function finds the mode and frequency of a dynamic array
    :param da: dynamic array of values
    :return: returns a tuple containing a dynamic array of the mode(s) and the mode's frequency
    """
    table = HashMap(da.length())
    mode = DynamicArray()
    freq = 0
    # any function that iterates over the linked list has O(1) time complexity
    # because the linked lists will always have only one node in this implementation of find_mode
    for idx in range(da.length()):
        key = da.get_at_index(idx)
        value = 1
        if table.contains_key(key):
            value = table.get(key) + 1
        table.put(key, value)
    da_table = table.get_keys_and_values()
    for _ in range(da_table.length()):
        key, value = da_table.pop()
        if value >= freq:
            if value > freq:
                mode = DynamicArray()
            mode.append(key)
            freq = value
    return mode, freq

