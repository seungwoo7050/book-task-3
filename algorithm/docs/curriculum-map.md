# Curriculum Map

## Core Sequence

| Track | Topic | CLRS | BOJ Projects |
| :--- | :--- | :--- | :--- |
| Core-00-Basics | Basic Coding Skills | Ch 1-3 | 10988, 11053, 16926 |
| Core-01-Array-List | Array & Linked List | Ch 10.2 | 10807, 5397, 1406 |
| Core-02-Stack-Queue | Stack, Queue, Deque | Ch 10.1 | 10828, 5430, 2164 |
| Core-03-BFS-DFS | BFS & DFS | Ch 22.2-22.3 | 24479, 7576, 1260 |
| Core-04-Recursion-Backtracking | Recursion & Backtracking | Ch 4 | 10872, 9663, 15649 |
| Core-05-Simulation | Simulation | Implementation discipline | 2920, 14503, 14891 |
| Core-06-Sorting | Sorting | Ch 2, 6-8 | 2750, 2170, 1181 |
| Core-07-Binary-Search-Hash | Binary Search & Hash | Ch 11, 12.3 | 1920, 2110, 10816 |
| Core-08-DP | Dynamic Programming | Ch 15 | 2748, 12865, 1149 |
| Core-09-Greedy | Greedy | Ch 16 | 11047, 1744, 1931 |
| Core-0A-Priority-Queue | Priority Queue | Ch 6, 19 | 11279, 1715, 1927 |
| Core-0B-Graph-Tree | Graph & Tree | Ch 22-24 | 11725, 1167, 1991 |
| Core-0C-Shortest-Path | Shortest Path | Ch 24 | 1916, 11657, 1753 |
| Core-0D-MST-Topo | MST & Topological Sort | Ch 23, 22.4 | 9372, 2252, 1197 |

## Advanced Sequence

| Track | Topic | CLRS | Study Projects |
| :--- | :--- | :--- | :--- |
| Advanced-CLRS | Divide and Conquer | Ch 4 | 0x10-strassen-matrix |
| Advanced-CLRS | Amortized Analysis | Ch 17 | 0x11-amortized-analysis-lab |
| Advanced-CLRS | Balanced Search Trees | Ch 13, 18 | 0x12-red-black-tree |
| Advanced-CLRS | Meldable Heaps | Ch 19 | 0x13-meldable-heap |
| Advanced-CLRS | Network Flow | Ch 26 | 0x14-network-flow |
| Advanced-CLRS | String Matching | Ch 32 | 0x15-string-matching |
| Advanced-CLRS | Computational Geometry | Ch 33 | 0x16-computational-geometry |
| Advanced-CLRS | Number Theory | Ch 31 | 0x17-number-theory-lab |
| Advanced-CLRS | NP-Completeness | Ch 34 | 0x18-np-completeness-lab |
| Advanced-CLRS | Approximation Algorithms | Ch 35 | 0x19-approximation-lab |

## Bridge Decisions

- `1717` is inserted in `Core-Bridges` to teach disjoint set union before Kruskal-heavy material in `Core-0D-MST-Topo`.
- `16926` remains in `Core-00-Basics` for provenance, but it is explicitly a simulation-flavored problem and should be revisited after `Core-05-Simulation`.
- `11053` remains in `Core-00-Basics` for provenance, but it is the first DP bridge and should be revisited before `Core-08-DP`.
- `0x12`, `0x13`, and `0x18` are intentionally redesigned into smaller runnable labs so that the advanced track stays a study repository instead of turning into a vague reading list.

## Implementation Policy

- Python is mandatory for every core and advanced project.
- C++ is retained for all gold-level legacy core projects plus BOJ `1753` and `1197`.
- Advanced topics are active study projects now; they use repo-authored specs instead of BOJ problem statements.
