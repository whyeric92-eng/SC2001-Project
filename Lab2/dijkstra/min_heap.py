def min_heapify(A, i):
    """Sink A[i] into place, assuming both subtrees of i are valid heaps."""
    l = 2 * i + 1
    r = 2 * i + 2
    if l >= len(A):
        return
    if r < len(A) and A[r] < A[l]:
        smallest = r
    else:
        smallest = l
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
        if A[par_ind] <= k:
            return
        A[par_ind], A[index] = A[index], A[par_ind]
        index = par_ind


if __name__ == "__main__":
    # Correctness check 1: the Build-Min-Heap example from the lecture
    # slides (page 13).
    A = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    build_min_heap(A)
    print("built heap:", A)
    print("matches lecture slides:", A == [0, 1, 3, 2, 5, 4, 7, 9, 6, 8])

    # Correctness check 2: enqueue random numbers, then dequeue them
    # all. They must come out in sorted order.
    import random

    random.seed(0)
    ok = True
    for _ in range(1000):
        numbers = [random.randint(0, 100) for _ in range(random.randint(1, 50))]
        A = []
        for k in numbers:
            enqueue(A, k)

        out = []
        while len(A) > 0:
            out.append(dequeue(A))

        ok = ok and out == sorted(numbers)

    print("enqueue/dequeue check passed:", ok)
