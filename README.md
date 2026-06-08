# priority_dict

A high-performance, dictionary-like structure that maps unique keys to numeric priorities. `PriorityDict` combines the fast lookup of a hash map with the efficient priority ordering of a binary min-heap, allowing you to instantly retrieve or update any item while maintaining a constantly sorted order of the lowest priority elements.

## Key Features

* **Dual-Nature Interface:** Acts like a standard Python dictionary while simultaneously behaving as a mutable min-priority queue.
* **Efficient In-Place Updates:** Change priorities or remove elements arbitrarily without rebuilding the underlying heap structure.
* **Type-Safe Generic Design:** Built using Python's `typing.Generic`, allowing clear static analysis for both key types (`K`) and priority types (`P`).
* **Optimized Performance:** All structural modifications are strictly controlled to guarantee sub-linear time complexities.

### Time & Space Complexities

Given $n$ as the number of entries in the structure:

| Operation | Time Complexity | Description |
| --- | --- | --- |
| `get` / `contains` / `__contains__` | $O(1)$ | Instant lookup via index mapping |
| `put` / `__setitem__` | $O(\log n)$ | Insertion or priority updates |
| `update_priority` | $O(\log n)$ | Dynamic adjustment of an existing key's weight |
| `pop_min` | $O(\log n)$ | Extracted root priority restoration |
| `remove` / `__delitem__` | $O(\log n)$ | Arbitrary element removal and balance restoration |
| **Space Complexity** | $O(n)$ | Linear memory footprints across the heap and index map |

## Installation

### Installing Development Version

To install the latest development branch directly from the GitHub repository, run the following command:

```bash
pip install git+https://github.com/agentlans/priority-dict.git

```

### Local Development Installation

If you are developing or contributing to the package, clone the repository and install it in editable mode alongside any project configurations found in `pyproject.toml`:

```bash
git clone https://github.com/agentlans/priority-dict.git
cd priority-dict
pip install -e .

```

## Quick Start & Usage Examples

### Basic Usage

You can use standard public methods or interface with the object exactly like a native Python dictionary.

```python
from priority_dict.core import PriorityDict

# Initialize a PriorityDict with string keys and integer priorities
pq = PriorityDict[str, int]()

# Adding or updating elements via standard dict interface
pq["task_a"] = 5
pq["task_b"] = 2
pq["task_c"] = 10

# Check presence and size
print("task_a" in pq)  # Output: True
print(len(pq))         # Output: 3

# Fetch the item with the minimum priority
min_key, min_priority = pq.pop_min()
print(f"Popped min: {min_key} with priority {min_priority}")
# Output: Popped min: task_b with priority 2

```

### Advanced Priority Updates and Removals

```python
# Insert a new key using the explicit API
pq.put("task_d", 8)

# Dynamically change the priority of an existing key
pq.update_priority("task_c", 1)  # task_c now has the lowest priority

# Arbitrary removal of an item anywhere in the queue
pq.remove("task_a")  # Returns True if found and removed

# Safely query priorities via .get()
priority = pq.get("task_c")
print(f"New priority for task_c: {priority}")  # Output: 1

```

## API Overview

### Core Class: `PriorityDict(Generic[K, P])`

#### Structural Methods

* **`put(key: K, priority: P) -> None`**
Inserts a new key with the given priority, or updates its priority if it already exists.
* **`update_priority(key: K, new_priority: P) -> None`**
Changes the priority of an existing key. Sifts up or down automatically depending on whether the priority decreased or increased. Raises `KeyError` if absent.
* **`pop_min() -> Tuple[K, P]`**
Removes and returns a `(key, priority)` tuple representing the item with the smallest priority value. Raises `IndexError` if the object is empty.
* **`remove(key: K) -> bool`**
Removes an arbitrary key from the structure. Returns `True` if successful, or `False` if the key was not found.

#### Lookup & Utility Methods

* **`get(key: K) -> Optional[P]`**
Returns the priority of the key, or `None` if the key does not exist.
* **`contains(key: K) -> bool`**
Returns `True` if the key is present in the collection.

#### Magic Methods (Dictionary-Like Interface)

* `__len__(self) -> int` — Returns total entries.
* `__bool__(self) -> bool` — Evaluates to `False` if empty, `True` otherwise.
* `__getitem__(self, key: K) -> P` — Bracket syntax access (`pq[key]`).
* `__setitem__(self, key: K, priority: P) -> None` — Bracket assignment (`pq[key] = priority`).
* `__delitem__(self, key: K) -> None` — Bracket syntax removal (`del pq[key]`).
* `__contains__(self, key: K) -> bool` — Expression inclusion testing (`key in pq`).

## Development and Testing

A `Makefile` is included to streamline local development, execution, and testing procedures.

### Running Tests

Execute the unit tests located in the `tests/` directory to verify code changes against target behavioural requirements:

```bash
make test

```

## Licence

This project is licensed under the MIT licence.
