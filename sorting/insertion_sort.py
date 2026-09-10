import counter

def insertion_sort(arr, low, high):
    """Sort arr[low..high] in place using insertion sort.

    Used as the base case of the hybrid sort for small subarrays
    (size <= threshold S), where insertion sort's low overhead beats
    merge sort's recursion/merging cost.
    """
    for i in range(low + 1, high + 1):
        j = i - 1
        # Shift arr[j] right while it's greater than its right neighbor,
        # inserting arr[i] into its correct position among arr[low..i-1].
        while j >= low:
            counter.comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                j -= 1
            else:
                # Already in order relative to its neighbor: the left
                # part is sorted, so we can stop early.
                break
    return arr