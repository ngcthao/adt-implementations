# Name: Ngoc-Thao Ly
# OSU Email: lyng@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 08/15/2023
# Description: This file contains an implementation of a Hash Map data structure that resolves collisions through
# open addressing.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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

    def hash_init(self, key) -> int:
        """
        Obtains the hash value of the desired key parameter
        :param key: key of desired object
        :return: returns the initial hash value of the key parameter
        """
        return self._hash_function(key) % self._capacity

    def find_entry(self, key) -> tuple:
        """
        Returns the entry with the respective key, if it exists.
        If the entry does not exist, returns None and the current index
        :param key: key of desired key/value pair
        :return: returns a tuple containing the entry and current index
        """
        init_idx = self.hash_init(key)
        idx = init_idx
        if self._size == 0:
            return None, idx
        probe = 1
        entry = self._buckets.get_at_index(idx)

        while entry:
            if entry.key == key:
                return entry, idx
            # quadratic probing for collisions
            idx = (init_idx + probe ** 2) % self._capacity
            entry = self._buckets.get_at_index(idx)
            probe += 1
        return None, idx

    def put(self, key: str, value: object) -> None:
        """
        If the key exists and is not a tombstone, the value is replaced.
        If the key exists and is a tombstone, the value is replaced and size is increased.
        If the key does not exist, it is added to the hashmap and size is increased
        :param key: key of desired entry
        :param value: desired value for the corresponding key parameter
        """
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        entry, idx = self.find_entry(key)
        if entry:
            entry.value = value
            if entry.is_tombstone:
                entry.is_tombstone = False
                self._size += 1
        else:
            new_entry = HashEntry(key, value)
            self._buckets.set_at_index(idx, new_entry)
            self._size += 1

    def table_load(self) -> float:
        """
        Returns the table load factor based on the table capacity
        :return: the load factor of the hashmap
        """
        element_count = 0
        for _ in self:
            element_count += 1
        return element_count / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hashmap
        :return: returns the number of empty buckets
        """
        element_count = 0
        for _ in self:
            element_count += 1
        return self._capacity - element_count

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hashmap to the desired capacity if it is prime. Otherwise, resizes to the next prime value.
        :param new_capacity: the desired capacity of the table
        """
        if new_capacity < self._size:
            return
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        temp_table = HashMap(0, self._hash_function)
        temp_table._buckets = DynamicArray()
        temp_table._capacity = new_capacity
        for _ in range(temp_table._capacity):
            temp_table._buckets.append(None)

        for entry in self:
            temp_table.put(entry.key, entry.value)
        self._buckets = temp_table._buckets
        self._capacity = temp_table._capacity

    def get(self, key: str) -> object:
        """
        Returns the value of the desired key, if it exists. Returns None otherwise.
        """
        entry, idx = self.find_entry(key)
        if entry and not entry.is_tombstone:
            return entry.value

    def contains_key(self, key: str) -> bool:
        """
        Determines whether a key exists in the hashmap
        :param key: the desired key
        :return: Returns True if a key exists in the hashmap and False otherwise
        """
        entry, idx = self.find_entry(key)
        if entry and not entry.is_tombstone:
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes a key/value pair from the hashmap, if it exists.
        Specifically, assigns the tombstone attribute to True and decreases hashmap size
        :param key: the desired key to be removed
        """
        entry, idx = self.find_entry(key)
        if entry and not entry.is_tombstone:
            entry.is_tombstone = True
            self._size -= 1

    def clear(self) -> None:
        """
        Clears the hashmap of all key/value pairs
        """
        temp_hash = HashMap(self._capacity, self._hash_function)
        self._buckets = temp_hash._buckets
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Saves all the key/value pairs in the hashmap into a dynamic array
        :return: returns a dynamic array containing all existing key/value pairs
        """
        kv_array = DynamicArray()
        for entry in self:
            new_tuple = entry.key, entry.value
            kv_array.append(new_tuple)
        return kv_array

    def __iter__(self):
        """
        Initializes the attribute self._index and returns the hashmap
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Allows the user to iterate through the hashmap using a for loop.
        Only returns values that exist and are not tombstones.
        """
        try:
            while True:
                val = self._buckets.get_at_index(self._index)
                self._index += 1
                if val and not val.is_tombstone:
                    return val
        except DynamicArrayException:
            raise StopIteration

