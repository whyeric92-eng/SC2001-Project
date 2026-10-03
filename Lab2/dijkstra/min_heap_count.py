"""Same as min_heap.py, plus counting of comparisons in
counter.comparisons. Used by dijkstra_heap_count.py.
"""
import counter


def min_heapify(A, i):
    """Sink A[i] into place, assuming both subtrees of i are valid heaps."""
    l = 2 * i + 1
    r = 2 * i + 2
    if l >= len(A):
        return
    smallest = l
    if r < len(A):
        counter.comparisons += 1
        if A[r] < A[l]:
            smallest = r
    counter.comparisons += 1
    if A[smallest] < A[i]:
        A[smallest], A[i] = A[i], A[smallest]
        min_heapify(A, smallest)


def build_min_heap(A):
    """Turn an unsorted array into a heap: O(n)."""
    for i in range(len(A) // 2 - 1, -1, -1):
        min_heapify(A, i)


def dequeue(A):
    """Remove and return the smallest element: O(log n)."""
    smallest = A[0]
    A[0] = A[len(A) - 1]
    A.pop()
    min_heapify(A, 0)
    return smallest


def enqueue(A, k):
    """Add k to the heap: O(log n)."""
    A.append(k)
    index = len(A) - 1
    while index > 0:
        par_ind = (index - 1) // 2
        counter.comparisons += 1
        if A[par_ind] <= k:
            return
        A[par_ind], A[index] = A[index], A[par_ind]
        index = par_ind
