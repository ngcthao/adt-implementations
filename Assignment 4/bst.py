# Name: Ngoc-Thao Ly
# OSU Email: lyng@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 4
# Due Date: 07/31/2023
# Description: This file contains a class that implements the functionality of a BST tree with various methods to
# edit the tree if desired.


import random
from typing import Tuple

from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value   # to store node's data
        self.left = None     # pointer to root of left subtree
        self.right = None    # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """
    Binary Search Tree class
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Perform pre-order traversal of the tree.
        Return False if nodes don't adhere to the bst ordering property.

        This is intended to be a troubleshooting method to help find any
        inconsistencies in the tree after the add() or remove() operations.
        A return of True from this method doesn't guarantee that your tree
        is the 'correct' result, just that it satisfies bst ordering.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                if node.left and node.left.value >= node.value:
                    return False
                if node.right and node.right.value < node.value:
                    return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Adds a new value to the tree.
        :param value: value to be added to the tree
        """
        if self._root is None:
            self._root = BSTNode(value)
        else:
            self._add_helper(self._root, value)

    def _add_helper(self, node: BSTNode, value: object) -> None:
        """
        Recursively traverses the tree for the correct placement of the value object and adds it to the tree.
        :param node: current node
        :param value: value to be added to the tree
        """
        if value < node.value:
            if node.left is None:
                node.left = BSTNode(value)
            else:
                self._add_helper(node.left, value)
        else:
            if node.right is None:
                node.right = BSTNode(value)
            else:
                self._add_helper(node.right, value)

    def remove(self, value: object) -> bool:
        """
        Removes a value from the tree
        :param value: value to be removed from the tree
        :return: returns True if the value is found and removed; returns False otherwise
        """
        if self._root is None:
            return False
        else:
            result = self._search_rec(self._root, None, value)
            if result is not None:
                node, p_node = result
                self._remove_node(node, p_node)
                return True
            return False

    def _search_rec(self, node: BSTNode, p_node: BSTNode, value: object) -> tuple:
        """
        Recursively search for the value parameter
        :param node: current node
        :param p_node: parent of current node
        :param value: value to be found
        :return: returns the parent of the matching node and the matching node, if they exist
        """
        if value == node.value:
            return node, p_node

        if value < node.value:
            if node.left is None:
                return
            return self._search_rec(node.left, node, value)
        else:
            if node.right is None:
                return
            return self._search_rec(node.right, node, value)

    def _remove_node(self, node, p_node) -> None:
        """
        Removes the node parameter from the binary search tree
        :param node: node to be removed
        :param p_node: parent of the node to be removed
        """
        if node.left is None and node.right is None:
            self._remove_no_subtrees(node, p_node)
        elif node.left and node.right:
            self._remove_two_subtrees(node, p_node)
        else:
            self._remove_one_subtree(node, p_node)

    def _remove_no_subtrees(self, node: BSTNode, p_node: BSTNode) -> None:
        """
        Remove a node that has no subtrees
        :param node: node to be removed
        :param p_node: parent of the node to be removed
        """
        if p_node is None:
            self._root = None
        elif p_node.left == node:
            p_node.left = None
        else:
            p_node.right = None

    def _remove_one_subtree(self, node: BSTNode, p_node: BSTNode) -> None:
        """
        Remove a node that has only one subtree
        :param node: node to be removed
        :param p_node: parent of the node to be removed
        """
        if node.left:
            if p_node is None:
                self._root = node.left
            elif p_node.left == node:
                p_node.left = node.left
            else:
                p_node.right = node.left
        else:
            if p_node is None:
                self._root = node.right
            elif p_node.left == node:
                p_node.left = node.right
            else:
                p_node.right = node.right

    def _remove_two_subtrees(self, node: BSTNode, p_node: BSTNode) -> None:
        """
        Remove a node that has two subtrees
        :param node: node to be removed
        :param p_node: parent of the node to be removed
        """
        new_node, new_p_node = BST._inorder_successor(node)
        new_node.left = node.left
        if new_node is not node.right:
            new_p_node.left = new_node.right
            new_node.right = node.right

        if p_node is None:
            self._root = new_node
        elif p_node.left == node:
            p_node.left = new_node
        else:
            p_node.right = new_node

    @staticmethod
    def _inorder_successor(node: BSTNode) -> tuple:
        """
        Finds the inorder successor and its parent based on the node parameter from a Binary Search Tree
        :param node: root node of subtree
        :return: returns tuple containing the inorder successor of the node parameter and its parent
        """
        orig_node = node
        node = node.right
        if node.left is not None:
            # Search for the parent of the leftmost node
            while node.left.left:
                node = node.left
            return node.left, node
        return node, orig_node

    def contains(self, value: object) -> bool:
        """
        Checks if the binary search tree contains the value parameter
        :param value: value to be found
        :return: returns True is the value is in the tree and False otherwise
        """
        if self._root is None:
            return False

        res = self._search_rec(self._root, None, value)
        if res is not None:
            return True
        return False

    def inorder_traversal(self) -> Queue:
        """
        Performs an inorder traversal on the BST
        :return: returns a queue with values in the aforementioned order
        """
        path = Queue()
        self.inorder_traversal_rec(self._root, path)
        return path

    def inorder_traversal_rec(self, node, path) -> BSTNode:
        """
        Recursively stores node values for inorder_traversal
        :param node: current node
        :param path: queue containing the stored node values
        :return: returns the current node
        """
        if node is None:
            return
        # Keeps traversing the left path until a leaf is reached
        left = self.inorder_traversal_rec(node.left, path)
        if left is not None:
            path.enqueue(left.value)
        # After each time a left node is queued, its parent is queued
        path.enqueue(node.value)
        # After each time a parent node is queued, its right node is queued
        right = self.inorder_traversal_rec(node.right, path)
        if right is not None:
            path.enqueue(right.value)

    def find_min(self) -> object:
        """
        Return the lowest value in the tree
        :return: value of lowest object
        """
        if self._root is None:
            return
        node = self._root
        while node.left is not None:
            node = node.left
        return node.value

    def find_max(self) -> object:
        """
        Return the highest value in the tree
        :return: value of the highest object
        """
        if self._root is None:
            return
        node = self._root
        while node.right is not None:
            node = node.right
        return node.value

    def is_empty(self) -> bool:
        """
        Checks if the tree is empty
        :return: returns True if the tree is empty and False otherwise
        """
        if self._root is None:
            return True
        return False

    def make_empty(self) -> None:
        """
        Empties the BST
        """
        self._root = None

    def set_root_with_node(self, node) -> None:
        """
        Sets a new root for the BST
        :param node: new root node
        """
        self._root = node

