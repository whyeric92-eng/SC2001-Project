import counter

def insertion_sort(arr, low, high):
    for i in range(low + 1, high + 1):
        j = i - 1
        while j >= low:
            counter.comparisons += 1
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                j-=1
            else:
                break
    return arr