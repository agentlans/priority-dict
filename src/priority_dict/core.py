from typing import TypeVar, Generic, Optional, Tuple, List, Dict

K = TypeVar('K')   # Key type (hashable)
P = TypeVar('P')   # Priority type (comparable, e.g., int, float)

class PriorityDict(Generic[K, P]):
    """
    A dictionary-like structure that maps unique keys to numeric priorities
    and allows efficient retrieval/removal of the key with the minimum priority.

    Invariants:
        1. Every key appears at most once.
        2. The heap array maintains the min-heap property:
           heap[i].priority <= heap[children(i)].priority.
        3. The index map (pos) always maps each key to its current index in the heap.
        4. The heap and the index map are kept consistent after every operation.

    Time Complexities (n = number of entries):
        - get, contains: O(1)
        - put, update_priority, pop_min, remove: O(log n)
        - space: O(n)
    """

    def __init__(self) -> None:
        """
        Initializes an empty PriorityDict.
        """
        # Heap stored as a list of [priority, key] pairs.
        # Using a list (mutable) allows efficient in-place priority updates.
        self.heap: List[List[P, K]] = []

        # Dictionary mapping each key to its current index in the heap.
        self.pos: Dict[K, int] = {}

    # ---------- Public API ----------

    def contains(self, key: K) -> bool:
        """
        Check whether a key exists in the structure.

        Args:
            key: The key to look up.

        Returns:
            True if the key is present, False otherwise.
        """
        return key in self.pos

    def get(self, key: K) -> Optional[P]:
        """
        Retrieve the priority associated with a key.

        Args:
            key: The key to look up.

        Returns:
            The priority of the key if it exists, otherwise None.
        """
        if key not in self.pos:
            return None
        idx = self.pos[key]
        return self.heap[idx][0]

    def put(self, key: K, priority: P) -> None:
        """
        Insert a new key with the given priority, or update an existing key's priority.

        If the key is new, it is appended to the heap and sifted up.
        If the key already exists, this is equivalent to calling update_priority.

        Args:
            key: The key to insert or update.
            priority: The numeric priority (must be comparable with other priorities).
        """
        if key in self.pos:
            self.update_priority(key, priority)
        else:
            # Append new entry and record its position
            self.heap.append([priority, key])
            idx = len(self.heap) - 1
            self.pos[key] = idx
            self._sift_up(idx)

    def update_priority(self, key: K, new_priority: P) -> None:
        """
        Change the priority of an existing key.

        The method determines whether the priority decreased or increased
        and performs a sift-up or sift-down accordingly.

        Args:
            key: The key whose priority should change.
            new_priority: The new priority value.

        Raises:
            KeyError: If the key is not present in the structure.
        """
        if key not in self.pos:
            raise KeyError(f"Key '{key}' not found in PriorityDict")

        idx = self.pos[key]
        old_priority = self.heap[idx][0]

        # No change – nothing to do
        if new_priority == old_priority:
            return

        self.heap[idx][0] = new_priority

        # Restore heap order
        if new_priority < old_priority:
            self._sift_up(idx)
        else:
            self._sift_down(idx)

    def peek_min(self) -> Tuple[K, P]:
        """
        Return the key and priority with the smallest priority without removing it.

        Returns:
            A tuple (key, priority) of the minimum element.

        Raises:
            IndexError: If the structure is empty.
        """
        if not self.heap:
            raise IndexError("peek_min from empty PriorityDict")

        priority, key = self.heap[0]
        return (key, priority)

    def pop_min(self) -> Tuple[K, P]:
        """
        Remove and return the key with the smallest priority.

        Returns:
            A tuple (key, priority) of the removed minimum element.

        Raises:
            IndexError: If the structure is empty.
        """
        if not self.heap:
            raise IndexError("pop_min from empty PriorityDict")

        # The root contains the minimum element
        min_priority, min_key = self.heap[0]

        # Remove the last element
        last = self.heap.pop()
        # Delete the minimum key from the index map
        del self.pos[min_key]

        if self.heap:
            # Move the last element to the root and update its position
            self.heap[0] = last
            self.pos[last[1]] = 0
            # Restore heap order starting from the root
            self._sift_down(0)

        # Return in the order (key, priority) as specified
        return (min_key, min_priority)

    def remove(self, key: K) -> bool:
        """
        Remove an arbitrary key from the structure (not necessarily the minimum).

        The method works by swapping the element to be removed with the last element,
        deleting it, and then restoring the heap property by sifting up or down as needed.

        Args:
            key: The key to remove.

        Returns:
            True if the key was removed, False if the key was not present.
        """
        if key not in self.pos:
            return False

        idx = self.pos[key]

        # If the element is already the last one, just pop it
        if idx == len(self.heap) - 1:
            self.heap.pop()
            del self.pos[key]
            return True

        # Swap with the last element
        self._swap(idx, len(self.heap) - 1)
        # Remove the last element (which is now the target key)
        self.heap.pop()
        del self.pos[key]

        # The element that moved to position 'idx' may need to be sifted
        # up or down to restore the heap property.
        self._sift_up(idx)
        self._sift_down(idx)

        return True

    # ---------- Dictionary-like interface ----------

    def __len__(self) -> int:
        """Return the number of entries in the PriorityDict."""
        return len(self.heap)

    def __bool__(self) -> bool:
        """Return True if the PriorityDict is non-empty."""
        return bool(self.heap)

    def __getitem__(self, key: K) -> P:
        """Return the priority associated with the key. Raises KeyError if absent."""
        if key not in self.pos:
            raise KeyError(key)
        idx = self.pos[key]
        return self.heap[idx][0]

    def __setitem__(self, key: K, priority: P) -> None:
        """Insert or update the priority for the given key."""
        self.put(key, priority)

    def __delitem__(self, key: K) -> None:
        """Remove the key from the PriorityDict. Raises KeyError if absent."""
        if not self.remove(key):
            raise KeyError(key)

    def __contains__(self, key: K) -> bool:
        """Return True if the key is present in the PriorityDict."""
        return self.contains(key)

    # ---------- Internal heap helpers ----------

    def _sift_up(self, i: int) -> None:
        """
        Move an element up the heap until the heap property is restored.

        Used when a priority has been decreased or a new element was appended.

        Args:
            i: Index of the element to sift up.
        """
        while i > 0:
            parent = (i - 1) // 2
            # If current priority >= parent priority, heap property satisfied
            if self.heap[parent][0] <= self.heap[i][0]:
                break
            self._swap(i, parent)
            i = parent

    def _sift_down(self, i: int) -> None:
        """
        Move an element down the heap until the heap property is restored.

        Used when a priority has been increased or the root was replaced.

        Args:
            i: Index of the element to sift down.
        """
        n = len(self.heap)
        while True:
            left = 2 * i + 1
            right = 2 * i + 2
            smallest = i

            if left < n and self.heap[left][0] < self.heap[smallest][0]:
                smallest = left
            if right < n and self.heap[right][0] < self.heap[smallest][0]:
                smallest = right

            if smallest == i:
                break

            self._swap(i, smallest)
            i = smallest

    def _swap(self, i: int, j: int) -> None:
        """
        Swap two heap entries and update the index map accordingly.

        Args:
            i: First index.
            j: Second index.
        """
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        # Update the positions in the index map for both keys
        self.pos[self.heap[i][1]] = i
        self.pos[self.heap[j][1]] = j

