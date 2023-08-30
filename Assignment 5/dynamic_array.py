# Name: Ngoc-Thao Ly
# OSU Email: lyng@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 2
# Due Date: 07/17/2023
# Description: File contains implemented DynamicArray methods that can be used to achieve a similar functionality
# to Python lists. The separate function find_mode() can also be used to find the most frequently recurring objects in
# a DynamicArray object.


from static_array import StaticArray


class DynamicArrayException(Exception):
    """
    Custom exception class to be used by Dynamic Array
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize new dynamic array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._size = 0
        self._capacity = 4
        self._data = StaticArray(self._capacity)

        # populate dynamic array with initial values (if provided)
        # before using this feature, implement append() method
        if start_array is not None:
            for value in start_array:
                self.append(value)

    def __str__(self) -> str:
        """
        Return content of dynamic array in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "DYN_ARR Size/Cap: "
        out += str(self._size) + "/" + str(self._capacity) + ' ['
        out += ', '.join([str(self._data[_]) for _ in range(self._size)])
        return out + ']'

    def __iter__(self):
        """
        Create iterator for loop
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        try:
            value = self[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return value

    def get_at_index(self, index: int) -> object:
        """
        Return value from given index position
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        return self._data[index]

    def set_at_index(self, index: int, value: object) -> None:
        """
        Store value at given index in the array
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        self._data[index] = value

    def __getitem__(self, index) -> object:
        """
        Same functionality as get_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.get_at_index(index)

    def __setitem__(self, index, value) -> None:
        """
        Same functionality as set_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.set_at_index(index, value)

    def is_empty(self) -> bool:
        """
        Return True is array is empty / False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size == 0

    def length(self) -> int:
        """
        Return number of elements stored in array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the capacity of the array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    def print_da_variables(self) -> None:
        """
        Print information contained in the dynamic array.
        Used for testing purposes.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        print(f"Length: {self._size}, Capacity: {self._capacity}, {self._data}")

    # -----------------------------------------------------------------------

    def resize(self, new_capacity: int) -> None:
        """
        Resizes the DynamicArray to new_capacity.
        :param new_capacity: an integer representing the new desired capacity
        """
        if new_capacity >= self._size > 0:
            new_array = StaticArray(new_capacity)
            # Copy old array to current array
            for idx in range(self.length()):
                if self.get_at_index(idx) is not None:
                    new_array.set(idx, self.get_at_index(idx))
            # Change capacity and replace data
            self._capacity = new_capacity
            self._data = new_array

    def append(self, value: object) -> None:
        """
        Adds a new value to the end of the DynamicArray.
        Doubles capacity before appending the new value if the internal storage capacity is already full.
        :param value: an object to be appended
        """
        if self._size == self._capacity:
            # Resize the current array, effectively erasing all data values
            self.resize(self._capacity * 2)

        self._size += 1
        self.set_at_index(self._size - 1, value)

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Insert an object value at the desired index.
        :param index: an integer value representing the desired index location
        :param value: an object to be inserted at the desired index
        """
        if index > self._size or index < 0:
            raise DynamicArrayException
        if index == self._size:
            self.append(value)
        else:  # if index is valid
            # Double the capacity if array is full
            if self._size == self._capacity:
                self.resize(self._capacity * 2)
            self._size += 1
            # Shift all values at index and onward to the right by 1
            for idx in range(self._size - 1, index, -1):
                self.set_at_index(idx, self._data.get(idx - 1))
            # Insert value at index
            self.set_at_index(index, value)

    def remove_at_index(self, index: int) -> None:
        """
        Removes the value at index and reduces the capacity of the DynamicArray if conditions are met.
        :param index: an integer representing the index location of the value to be removed
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        if self._size < 0.25 * self._capacity and self._capacity > 10:
            if self._size * 2 < 10:
                self.resize(10)
            else:
                self.resize(self._size * 2)
        # Remove value at index and replace all necessary values
        for idx in range(index, self._size):
            if idx + 1 == self._size:
                self.set_at_index(idx, None)
            else:
                self.set_at_index(idx, self.get_at_index(idx + 1))
        self._size -= 1

    def slice(self, start_index: int, size: int) -> "DynamicArray":
        """
        Returns a DynamicArray containing the desired section of data
        :param start_index: an integer representing the starting index of the slice
        :param size: an integer representing the desired size of the slice
        :return: a DynamicArray of the section of desired data
        """
        if start_index < 0 or start_index >= self._size or size < 0:
            raise DynamicArrayException
        if start_index + size > self._size:
            raise DynamicArrayException
        sliced = DynamicArray()
        for idx in range(size):
            sliced.append(self.get_at_index(idx + start_index))
        return sliced

    def merge(self, second_da: "DynamicArray") -> None:
        """
        Merges second_da to the end of the current DynamicArray one value at a time.
        :param second_da: a DynamicArray to be added to the end of the current DynamicArray
        """
        for idx in range(second_da._size):
            self.append(second_da.get_at_index(idx))

    def map(self, map_func) -> "DynamicArray":
        """
        Returns a DynamicArray with the function, map_func, applied to each value in the current DynamicArray
        :param map_func: a function to be applied to the DynamicArray
        :return: a DynamicArray containing the results of applying the function to each value
        """
        map_array = DynamicArray()
        for idx in range(self._size):
            new_val = map_func(self.get_at_index(idx))
            map_array.append(new_val)
        return map_array

    def filter(self, filter_func) -> "DynamicArray":
        """
        Returns a DynamicArray containing values from the current DynamicArray that satisfies the function, filter_func
        :param filter_func: a function that will return a boolean to filter out desired values
        :return: a DynamicArray containing only the values that satisfy filter_func
        """
        filtered_arr = DynamicArray()
        for idx in range(self._size):
            val = self.get_at_index(idx)
            if filter_func(val):
                filtered_arr.append(val)
        return filtered_arr

    def reduce(self, reduce_func, initializer=None) -> object:
        """
        Returns a result after the function, reduce_func, passes through all elements in DynamicArray
        :param reduce_func: a function that will have all elements in the DynamicArray passed through it
        :param initializer: the initial value for reduce_func
        :return: the final object after reduce_func has been applied to all elements in the DynamicArray
        """
        res = initializer
        start_idx = 0
        if res is None:
            res = self._data[0]
            start_idx = 1

        for idx in range(start_idx, self._size):
            res = reduce_func(res, self.get_at_index(idx))
        return res

