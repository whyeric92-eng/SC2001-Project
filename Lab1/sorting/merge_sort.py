import counter

def merge_sort(arr):
    """Sort arr in place using standard top-down merge sort."""
    # Allocate one aux array up front and reuse it for every merge call,
    # instead of slicing new left/right arrays (e.g. left = arr[low:mid+1])
    # on every call. Slicing allocates two new lists per merge (O(n)
    # copies each), which adds up over the O(n log n) merge calls;
    # reusing a single aux buffer avoids that repeated allocation
    # overhead, which matters for the CPU-time measurements in the
    # experiments.
    aux = [0] * len(arr)
    _merge_sort(arr, 0, len(arr) - 1, aux)

def _merge_sort(arr, low, high, aux):
    if low >= high:
        return

    mid = (low + high) // 2
    _merge_sort(arr, low, mid, aux)
    _merge_sort(arr, mid + 1, high, aux)
    merge(arr, low, mid, high, aux)

def merge(arr, low, mid, high, aux):
    """Merge the two sorted halves arr[low..mid] and arr[mid+1..high]
    back into arr, using aux as scratch space.
    """
    # Copy the range into aux so we can compare/overwrite arr[low..high]
    # without clobbering values we still need to read.
    for k in range(low, high + 1):
        aux[k] = arr[k]

    i, j = low, mid + 1
    for k in range(low, high + 1):
        if i > mid:
            # Left half exhausted: only right half elements remain.
            arr[k] = aux[j]
            j += 1
        elif j > high:
            # Right half exhausted: only left half elements remain.
            arr[k] = aux[i]
            i += 1
        else:
            # Both halves still have elements: this is the comparison
            # that determines merge sort's key-comparison count.
            counter.comparisons += 1
            if aux[i] <= aux[j]:
                arr[k] = aux[i]
                i += 1
            else:
                arr[k] = aux[j]
                j += 1