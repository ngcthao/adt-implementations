# Name: Ngoc-Thao Ly
# OSU Email: lyng@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 4
# Due Date: 07/31/2023
# Description: This file contains a class that implements the functionality of an AVL tree using the BST class, capable
# of re-balancing as needed.


import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """
    AVL Tree class. Inherits from BST
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self._root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Adds a new node with the desired value to the AVL tree
        :param value: value to be added
        """
        # Add the value to the tree
        parent_s = Stack()
        balance_s = Stack()
        new_node = AVLNode(value)
        new_node.height = 0
        if self.get_root() is None:
            self.set_root_with_node(new_node)
        if self.contains(value):
            return
        # find the correct placement and its path
        node = self.get_root()
        while node is not None:
            parent_s.push(node)
            balance_s.push(node)
            if value < node.value:
                node = node.left
            else:
                node = node.right
        # replace the values, update the heights, and rebalance
        node = new_node
        node.parent = parent_s.top()
        if value < node.parent.value:
            node.parent.left = node
        else:
            node.parent.right = node
        parent_s.push(node)
        balance_s.push(node)
        self._update_heights_sq(parent_s)
        self._rebalance(balance_s)

    def _rebalance(self, balance_stack) -> None:
        """
        Rebalance the AVL according to the node order in the balance_stack. If balance_stack is empty,
        every value in the AVL is added to balance_stack before balancing.
        :param balance_stack: stack that stores nodes to be checked for balancing
        """
        # Obtain a stack of all the nodes in level by level order, the top of the stack is the lowest tier.
        if balance_stack is None:
            root = self.get_root()
            balance_stack = Stack()
            row_queue = Queue()
            if root:
                balance_stack.push(root)
                row_queue.enqueue(root)
            try:
                while True:
                    self._traverse_by_level(balance_stack, row_queue)
            except IndexError:
                pass
        # rebalance each node in the stack if necessary
        try:
            while True:
                self._rebalance_helper(balance_stack.pop())
        except IndexError:
            return

    def _update_heights(self) -> None:
        """
        Updates all node heights in the AVL tree
        """
        root = self.get_root()
        node_stack = Stack()
        row_queue = Queue()
        if root:
            node_stack.push(root)
            row_queue.enqueue(root)
        try:
            while True:
                self._traverse_by_level(node_stack, row_queue)
        except IndexError:
            self._update_heights_sq(node_stack)

    @staticmethod
    def _traverse_by_level(node_stack, row_queue) -> None:
        """
        Traverses the AVL tree level by level and saves the path in node_stack
        :param node_stack: stack containing the node values in the aforementioned order
        :param row_queue: queue containing the order the nodes will be checked in
        """
        if row_queue is not None:
            node = row_queue.dequeue()
            if node.left:
                node_stack.push(node.left)
                row_queue.enqueue(node.left)
            if node.right:
                node_stack.push(node.right)
                row_queue.enqueue(node.right)

    def _rebalance_helper(self, node):
        """
        Helps _rebalance method by rotating the AVL tree if the node meets requirements for a single or double rotation
        :param node: node that will be checked
        """
        balance = self._balance_test(node)
        if balance < -1:
            # Check the left side
            check_balance = self._balance_test(node.left)
            if check_balance <= 0:
                self._rotate_right(node)
            if check_balance > 0:
                self._rotate_left(node.left)
                self._rotate_right(node)
        if balance > 1:
            # Check the right side
            check_balance = self._balance_test(node.right)
            if check_balance >= 0:
                self._rotate_left(node)
            if check_balance < 0:
                self._rotate_right(node.right)
                self._rotate_left(node)

    @staticmethod
    def _balance_test(node) -> int:
        """
        Obtains the balance at a certain node in the AVL tree
        :param node: node to be checked
        :return: the balance value at the node
        """
        if node.right and node.left:
            return node.right.height - node.left.height
        elif node.right:
            return node.right.height + 1
        elif node.left:
            return (node.left.height + 1) * -1
        else:
            return 0

    @staticmethod
    def _max(node_1, node_2) -> AVLNode:
        """
        Obtains the node with the higher height attribute
        :param node_1: node to be compared
        :param node_2: node to be compared
        :return: node parameter with larger height attribute
        """
        if node_1 and node_2:
            if node_1.height > node_2.height:
                return node_1
            else:
                return node_2
        else:
            if node_1:
                return node_1
            elif node_2:
                return node_2
            else:
                return

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """
        Rotates a subtree to the left.
        :param node: node of interest
        :return: returns the root of the original subtree before rotation
        """
        p_node = node.parent
        imb_node = node.right

        node.right = imb_node.left  # Assign imb_node's old left to node.right
        if node.right is not None:
            node.right.parent = node    # Assign the above line's new parents, if it exists
        imb_node.left = node        # Assign imb_node's new left to node
        node.parent = imb_node      # Assign the above line's new parents

        if p_node is None:
            self.set_root_with_node(imb_node)
            imb_node.parent = None
        else:
            if p_node.left == node:
                p_node.left = imb_node
            else:
                p_node.right = imb_node
            imb_node.parent = p_node
        # Update heights
        update_nodes = Queue()
        update_nodes.enqueue(node)
        self._traverse_up(imb_node, update_nodes)
        self._update_heights_sq(update_nodes)
        return imb_node

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """
        Rotates a subtree to the right.
        :param node: node of interest
        :return: returns the root of the original subtree before rotation
        """
        p_node = node.parent
        imb_node = node.left

        node.left = imb_node.right  # Assign imb_node's old left to node.right
        if node.left is not None:
            node.left.parent = node     # Assign the above line's new parents, if it exists
        imb_node.right = node       # Assign imb_node's new left to node
        node.parent = imb_node      # Assign the above line's new parents

        if p_node is None:
            self.set_root_with_node(imb_node)
            imb_node.parent = None
        else:
            if p_node.left == node:
                p_node.left = imb_node
            else:
                p_node.right = imb_node
            imb_node.parent = p_node
        # Update heights
        update_nodes = Queue()
        update_nodes.enqueue(node)
        self._traverse_up(imb_node, update_nodes)
        self._update_heights_sq(update_nodes)
        return imb_node

    def _update_heights_sq(self, node_adt) -> None:
        """
        Updates the heights of all nodes in node_adt
        :param node_adt: a stack or queue containing nodes to be updated
        """
        try:
            if type(node_adt) is Stack:
                while True:
                    node = node_adt.top()
                    node.height = self._update_heights_rec(node_adt.pop())
            if type(node_adt) is Queue:
                while True:
                    node = node_adt.dequeue()
                    node.height = self._update_heights_rec(node)
        except IndexError:
            return

    def _update_heights_rec(self, node) -> int:
        """
        Recursively calculates the correct height for node paramter
        :param node: node of interest
        :return: correct height for the node parameter
        """
        if node.left is None and node.right is None:
            return 0
        return self._update_heights_rec(self._max(node.left, node.right)) + 1

    def _traverse_up(self, node, path) -> None:
        """
        Recursively obtains all parents of node until the root is reached
        :param node: current node
        :param path: queue containing the parent nodes in the order they are passed
        """
        if node:
            path.enqueue(node)
            self._traverse_up(node.parent, path)

    def remove(self, value: object) -> bool:
        """
        Removes a value from the tree
        :param value: value to be removed from the tree
        :return: returns True if the value is found and removed; returns False otherwise
        """
        root = self.get_root()
        if root is None:
            return False
        else:
            node = self._avl_search_rec(root, value)
            if node is not None:
                self._remove_node(node)
                return True
            return False

    def _avl_search_rec(self, node: AVLNode, value: object) -> AVLNode:
        """
        Recursively search for the value parameter
        :param node: current node
        :param value: value to be found
        :return: returns the parent of the matching node and the matching node, if they exist
        """
        if value == node.value:
            return node

        if value < node.value:
            if node.left is None:
                return
            return self._avl_search_rec(node.left, value)
        else:
            if node.right is None:
                return
            return self._avl_search_rec(node.right, value)

    def _remove_node(self, node) -> None:
        """
        Removes the node parameter from the binary search tree
        :param node: node to be removed
        """
        if node.left is None and node.right is None:
            self._remove_no_subtrees(node, node.parent)
        elif node.left and node.right:
            self._remove_two_subtrees(node)
        else:
            self._remove_one_subtree(node)
        self._update_heights()
        self._rebalance(None)
        self._update_heights()

    @staticmethod
    def _inorder_successor(node: AVLNode) -> AVLNode:
        """
        Finds the inorder successor and its parent based on the node parameter from an AVL
        :param node: root node of subtree
        :return: returns node of the inorder successor
        """
        node = node.right
        if node.left is not None:
            # Search for the parent of the leftmost node
            while node.left.left:
                node = node.left
            return node.left
        return node

    def _remove_one_subtree(self, node: AVLNode) -> None:
        """
        Remove a node that has only one subtree
        :param node: node to be removed
        """
        if node.left:
            if node.parent is None:
                self._root = node.left
                node.left.parent = None
            elif node.parent.left == node:
                node.parent.left = node.left
                node.left.parent = node.parent
            else:
                node.parent.right = node.left
                node.left.parent = node.parent
        else:
            if node.parent is None:
                self._root = node.right
                node.right.parent = None
            elif node.parent.left == node:
                node.parent.left = node.right
                node.right.parent = node.parent
            else:
                node.parent.right = node.right
                node.right.parent = node.parent

    def _remove_two_subtrees(self, node: AVLNode) -> None:
        """
        Remove a node with two subtrees
        :param node: node to be removed
        """
        io_successor = AVL._inorder_successor(node)
        io_p = io_successor.parent

        # print("ios", io_successor.value, io_successor.parent)
        # print("io_parent", io_p.value, io_p.parent)

        io_successor.left = node.left
        if node.left is not None:
            node.left.parent = io_successor
        if io_successor is not node.right:
            io_p.left = io_successor.right
            if io_successor.right is not None:
                io_successor.right.parent = io_p
            io_successor.right = node.right
        if io_p is not None and io_p.parent == node:
            io_p.parent = io_successor
        else:
            node.right.parent = io_successor

        if node.parent is None:
            self.set_root_with_node(io_successor)
            io_successor.parent = None
        elif node.parent.left == node:
            node.parent.left = io_successor
            io_successor.parent = node.parent
        else:
            node.parent.right = io_successor
            io_successor.parent = node.parent

