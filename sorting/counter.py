# Global counter for the number of key comparisons made by the sorting
# algorithms. Shared across insertion_sort.py and merge_sort.py so the
# experiments can measure total comparisons for a single sort call.
comparisons = 0

def reset_counter():
    global comparisons
    comparisons = 0
