import merge_sort, insertion_sort

def hybrid_sort(arr, S):
    """Sort arr in place using merge sort, switching to insertion sort
    once a subarray's size drops to or below the threshold S.
    """
    aux = [0] * len(arr)
    _hybrid_sort(arr, 0, len(arr) - 1, S, aux)


def _hybrid_sort(arr, low, high, S, aux):
    # Base case: subarray is small enough that insertion sort's lower
    # overhead outperforms further merge-sort recursion.
    if high - low + 1 <= S:
        insertion_sort.insertion_sort(arr, low, high)
        return
    mid = (low + high) // 2
    _hybrid_sort(arr, low, mid, S, aux)
    _hybrid_sort(arr, mid + 1, high, S, aux)
    merge_sort.merge(arr, low, mid, high, aux)