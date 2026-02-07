from builtins import ValueError


def bitonic_sort(arr):
    n = len(arr)

    if n & (n - 1) != 0:
        raise ValueError("Bitonic Sort requiere tamaño potencia de 2")

    yield from _bitonic_sort(arr, 0, n, True)


def _bitonic_sort(arr, low, cnt, ascending):
    if cnt > 1:
        k = cnt // 2
        yield from _bitonic_sort(arr, low, k, True)
        yield from _bitonic_sort(arr, low + k, k, False)
        yield from _bitonic_merge(arr, low, cnt, ascending)


def _bitonic_merge(arr, low, cnt, ascending):
    if cnt > 1:
        k = cnt // 2
        for i in range(low, low + k):
            yield ("compare", i, i + k)
            if (arr[i] > arr[i + k]) == ascending:
                arr[i], arr[i + k] = arr[i + k], arr[i]
                yield ("swap", i, i + k)
        yield from _bitonic_merge(arr, low, k, ascending)
        yield from _bitonic_merge(arr, low + k, k, ascending)
