

class _Node:
    __slots__ = '_element', '_prev', '_next'  # streamline memory

    def __init__(self, element, prev=None, next=None):  # initialize node’s fields
        self._element = element  # user’s element
        self._prev: _Node = prev  # previous node reference
        self._next: _Node = next  # next node reference


class Position:
    """”An abstraction representing the location of a single element."""

    def __init__(self, container, node: _Node) -> None:
        """Constructor should not be invoked by user."""
        self.container = container
        self.node = node

    def element(self):
        """Return the element stored at this Position."""
        return self.node._element

    def __eq__(self, __o) -> bool:
        """Return True if other is a Position representing the same location."""
        return type(__o) is type(self) and __o.node is self.node

    def __ne__(self, __o: object) -> bool:
        """Return True if other does not represent the same location."""
        return not (self == __o)


class DoubleLinkedBase:
    def __init__(self) -> None:
        self.header = _Node(None, None, None)
        self.trailer = _Node(None, None, None)
        self.header._next = self.trailer
        self.trailer._prev = self.header
        self.size: int = 0

    def __len__(self) -> int:
        """Return the number of elements in the list"""
        return self.size

    def is_empty(self) -> bool:
        """return true if list is empty"""
        return self.size == 0

    def insert_between(self, e, predecessor: _Node, successor: _Node):
        """Add element e between two existing nodes and return new node."""
        newest = _Node(e, prev=predecessor, next=successor)
        predecessor._next = newest
        successor._prev = newest
        self.size += 1
        return newest

    def delete_node(self, node: _Node):
        """”Delete nonsentinel node from the list and return its element."""
        predecessor = node._prev
        successor = node._next
        predecessor._next = successor
        successor._prev = predecessor
        self.size -= 1
        element = node._element
        node._prev = node._prev = node._element = None
        return element


class PositionalList(DoubleLinkedBase):
    """A sequential container of elements allowing positional access"""

    def _validate(self, p: Position):
        """Return position s node, or raise appropriate error if invalid."""

        if not isinstance(p, Position):
            raise TypeError('p must be proper Position type')
        if p.container is not self:
            raise TypeError('p does not belong to this container')
        if p.node._next is None:
            raise ValueError('p is no longer valid')

        return p.node

    def _make_position(self, node):
        """Return Position instance for given node (or None if sentinel)."""
        if node is self.header or node is self.trailer:
            return None  # boundary violation
        else:
            return Position(self, node)  # legitimate position

    def first(self):
        """Return the first Position in the list (or None if list is empty)"""
        return self._make_position(self.header._next)

    def last(self):
        """Return the last Position in the list (or None if list is empty)."""
        return self._make_position(self.trailer._prev)

    def befor(self, p):
        """Return the Position just before Position p (or None if p is first)."""
        node = self._validate(p)
        return self._make_position(node._prev)

    def after(self, p):
        """Return the Position just after Position p (or None if p is last)."""
        node = self._validate(p)
        return self._make_position(node=node._next)

    def __iter__(self):
        """Generate a forward iteration of the elements of the list."""

        cursor = self.first()
        while cursor is not None:
            yield cursor.element()
            cursor = self.after(cursor)

    def insert_between(self, e, predecessor: _Node, successor: _Node):
        """Add element between existing nodes and return new Position"""
        node = super().insert_between(e, predecessor, successor)
        return self._make_position(node)

    def add_first(self, e):
        """ Insert element e at the front of the list and return new Position."""
        return self.insert_between(e, self.header, self.header._next)

    def add_last(self, e):
        """Insert element e at the back of the list and return new Position."""
        return self.insert_between(e, self.trailer._prev, self.trailer)

    def add_befor(self, p, e):
        """Insert element e into list before Position p and return new Position."""
        original = self._validate(p)
        return self.insert_between(e, original, original._next)

    def delete(self, p):
        """Remove and return the element at Position p."""
        original = self._validate(p)
        return self.delete_node(original)  # inherited method returns element

    def replace(self, p, e):
        """
            Replace the element at Position p with e.
            Return the element formerly at Position p.
        """
        original = self._validate(p)
        old_value = original._element   # temporarily store old element
        original._element = e           # replace with new element
        return old_value                # return the old element value
