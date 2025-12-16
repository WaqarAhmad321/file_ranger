# Data Structures & Algorithms Project Report

## Terminal-Based File Manager with C++ Backend

---

## 1. PROJECT OVERVIEW

### 1.1 Project Description

This project implements a Terminal User Interface (TUI) based File Manager that enables fast and efficient file management directly within the terminal. The system emphasizes performance and usability by combining a structured TUI with core Data Structures and Algorithms (DSA) such as trees, traversal algorithms, stacks, and sorting techniques. The interface is built using Python, while the whole backend and performance-critical components are implemented in C++ and integrated using pybind11.

### 1.2 Core Features

The application provides terminal-based file management with the following capabilities:

- **Navigation**: Vim-like keyboard controls (`hjkl`), three-pane layout, browser-style back/forward history
- **File Operations**: Create, rename, copy, paste, delete (all recursive for directories)
- **Display**: Auto-sorted file list (directories first, alphabetical), syntax highlighting, file preview
- **DSA Features**: O(N log N) custom merge sort, O(1) dual-stack navigation, O(N) tree-based directory listing

![Application Screenshot](images/app-screenshot.png)
_Figure 1: File manager interface showing three-pane layout with navigation_

### 1.3 Technology Stack

- **Backend**: C++ (C++17) - Core DSA implementation
- **Binding**: pybind11 - C++ to Python interoperability
- **Frontend**: Python (Textual framework) - TUI layer
- **Build**: CMake

---

## 2. DATA STRUCTURES IMPLEMENTATION

### 2.1 N-ary Tree (FileNode)

**Purpose**: Represents filesystem hierarchy where directories are internal nodes and files are leaves.

**Structure**: Each `FileNode` contains name, path, type flag, size, and a vector of children (for directories).

**Key Features**:

- Uses `std::shared_ptr` for automatic memory management
- Direct mapping to OS filesystem structure
- **Complexity**: O(N) to build, O(1) to access children

![N-ary Tree Structure](images/tree-structure.png)
_Figure 2: N-ary tree representation of filesystem hierarchy_

---

### 2.2 Stack (CustomStack)

**Implementation**: Custom stack class using vector as underlying storage.

**Core Operations**: All O(1) - `push()`, `pop()`, `top()`, `empty()`, `size()`, `clear()`

**Design**: Vector provides cache efficiency and amortized O(1) insertions.

---

### 2.3 Dual Stack Architecture (HistoryManager)

**Purpose**: Browser-style navigation using two stacks (`back_stack` and `forward_stack`).

**Key Operations** (all O(1)):

1. **Push**: Adds path to back_stack, clears forward_stack (new navigation invalidates forward)
2. **Go Back**: Pops from back_stack, pushes to forward_stack, returns previous path
3. **Go Forward**: Pops from forward_stack, pushes to back_stack, returns next path

**Example**: `back=[A,B,C]` → go back → `back=[A,B]`, `forward=[C]`

**Invariant**: Current position is always `back_stack.top()`

![Dual Stack Navigation](images/dual-stack.png)
_Figure 3: Dual-stack mechanism for browser-style navigation_

---

### 2.4 Merge Sort (Manual Implementation)

**Why Merge Sort?**: Stable sort, guaranteed O(N log N), divide-and-conquer demonstration

**Key Components**:

1. **Comparator**: Two-level comparison - directories before files, then case-insensitive alphabetical
2. **Merge Function**: Combines sorted halves using temporary arrays - O(N)
3. **Recursive Divide**: Splits array, recursively sorts halves, merges back

**Complexity**: Time O(N log N), Space O(N), Recurrence: T(N) = 2T(N/2) + O(N)

**Example**: `[file.txt, Documents/, readme.MD, Pictures/]` → `[Documents/, Pictures/, file.txt, readme.MD]`

---

## 3. RECURSION IN FILE OPERATIONS

**Purpose**: Handle nested directory structures efficiently.

**Recursive Operations**:

1. **Directory Creation**: Creates parent directories automatically (e.g., `/a/b/c/d` creates all intermediate paths)
2. **Directory Removal**: Post-order traversal - deletes children before parent to prevent errors
3. **Copy Operations**: Pre-order traversal - creates parent directories before copying children

**Note**: Directory tree building uses lazy loading (iterative, one level at a time) to avoid stack overflow on deep trees.

---

## 4. FEATURES & DATA STRUCTURE MAPPING

| Feature                | User Action                  | Data Structure              | Algorithm                     | Complexity              |
| ---------------------- | ---------------------------- | --------------------------- | ----------------------------- | ----------------------- |
| **Directory Browsing** | Navigate folders             | N-ary Tree (FileNode)       | Tree construction & traversal | O(N) build, O(1) access |
| **File Listing**       | View folder contents         | Vector (dynamic array)      | Iteration                     | O(N)                    |
| **Sorted Display**     | Automatic alphabetical order | Vector + Comparator         | Manual merge sort             | O(N log N)              |
| **Back Navigation**    | Press `h` or `←`             | Dual Stack (HistoryManager) | Stack pop/push                | O(1)                    |
| **Forward Navigation** | Press `L`                    | Dual Stack (HistoryManager) | Stack pop/push                | O(1)                    |
| **Create File**        | Press `n`, enter name        | Filesystem API              | File creation                 | O(1)                    |
| **Create Directory**   | Press `N`, enter name        | Recursion                   | Recursive mkdir               | O(D) depth              |
| **Delete File/Dir**    | Press `d`, confirm           | Recursion                   | Post-order traversal          | O(K) items              |
| **Copy File/Dir**      | Press `c` then `p`           | Recursion                   | Pre-order traversal           | O(K) items              |
| **Rename File/Dir**    | Press `r`, enter name        | Filesystem API              | Atomic rename                 | O(1)                    |

_Where N = files in directory, K = total files in tree, D = directory depth_

---

## 5. ARCHITECTURE & PYTHON INTEGRATION

### 5.1 Three-Layer Architecture

The project follows a clean separation of concerns with three distinct layers:

**Layer 1 - C++ Backend**:

- Core DSA implementations (N-ary tree, custom stack, merge sort)
- File operations and recursion
- Performance-critical code with memory safety (smart pointers)

**Layer 2 - Binding Layer (pybind11)**:

- Exposes C++ classes and functions to Python
- Automatic type conversion: `std::string` ↔ `str`, `std::vector` ↔ `list`
- Zero-copy data sharing via `shared_ptr`

**Layer 3 - Python UI (Textual)**:

- Terminal user interface with keyboard navigation
- Event handling and user interaction
- Calls C++ backend for all data operations

### 5.2 Why This Architecture?

- **Performance**: C++ handles memory-intensive operations (tree building, sorting, recursion)
- **Productivity**: Python provides rapid UI development with the Textual framework
- **Type Safety**: C++ ensures correctness at compile-time for critical data structures
- **Maintainability**: Clear boundaries between DSA logic and presentation layer

**Example Interaction**:

```python
# Python UI calls C++ backend
history = backend.HistoryManager()      # C++ object
root = backend.list_directory("/home")  # Returns C++ FileNode tree
root.children                           # Access C++ vector as Python list
```

![Architecture Diagram](images/architecture.png)
_Figure 6: Three-layer architecture showing C++ backend, pybind11 bindings, and Python UI_

---

## 6. CHALLENGES & FUTURE WORK

### 6.1 Challenges Faced

- **Memory Management**: Ensuring proper cleanup with shared pointers across C++ and Python boundary
- **Merge Sort Stability**: Maintaining relative order for case-insensitive comparisons
- **Cross-Language Integration**: Managing data marshaling between C++ structures and Python objects
- **Lazy Loading**: Balancing tree depth versus memory usage in directory traversal

### 6.2 Future Enhancements

- **Persistent Tree**: Maintain in-memory tree with incremental updates for better performance on large directories
- **Search Algorithm**: Implement Trie or Binary Search Tree for fast file/folder search
- **Undo/Redo**: Extend stack-based history to file operations (delete, rename, move)
- **Custom Dynamic Array**: Replace `std::vector` with manual array implementation for complete DSA independence
- **Graph Traversal**: Add symbolic link support using graph algorithms to detect cycles

---

## 7. TEAM CONTRIBUTIONS

| Member       | Primary Contributions                                                           |
| ------------ | ------------------------------------------------------------------------------- |
| **Ahmad Saad Tahir** | N-ary tree structure, FileNode implementation,       |
| **Haider Farooq** | Custom stack ADT, HistoryManager, navigation logic |
| **Najmul Arifeen** | Manual merge sort, custom comparator, recursive operations, complexity analysis |
| **Waqar Ahmad** | Python UI (Textual), integration, dual-stack architecture, tree construction algorithm     |

**Collaborative**: Architecture design, code reviews, debugging, performance optimization, report writing

---

## 8. CONCLUSION

This project demonstrates practical application of DSA concepts in a file management system:

**Core Implementations**:

- Custom stack ADT with complete interface
- N-ary tree with smart pointer memory management
- Dual-stack navigation (browser-style back/forward)
- **Manual merge sort** (divide-and-conquer, no STL)
- Recursive file operations (mkdir, rm, cp)
- Two-level comparator (type priority + case-insensitive)

**Complexity Achievements**:

- O(N log N) sorting with guaranteed performance
- O(1) navigation operations
- O(N) tree construction with lazy loading

This project serves as a comprehensive demonstration of data structures course concepts applied to solve a practical problem in systems programming.

---
