def quick_sort(arr):
    yield from _quick_sort(arr, 0, len(arr) - 1)


def _quick_sort(arr, low, high):
    if low < high:
        pivot_index = yield from partition(arr, low, high)
        yield from _quick_sort(arr, low, pivot_index - 1)
        yield from _quick_sort(arr, pivot_index + 1, high)


def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        yield ("compare", j, high)
        if arr[j] <= pivot:
            i += 1
            if i != j:
                arr[i], arr[j] = arr[j], arr[i]
                yield ("swap", i, j)

    if i + 1 != high:
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        yield ("swap", i + 1, high)

    return i + 1
