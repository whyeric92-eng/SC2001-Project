import counter

def merge_sort(arr):
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
    for k in range(low, high + 1):
        aux[k] = arr[k]

    i, j = low, mid + 1
    for k in range(low, high + 1):
        if i > mid:
            arr[k] = aux[j]
            j += 1
        elif j > high:
            arr[k] = aux[i]
            i += 1
        else:
            counter.comparisons += 1
            if aux[i] <= aux[j]:
                arr[k] = aux[i]
                i += 1
            else:
                arr[k] = aux[j]
                j += 1