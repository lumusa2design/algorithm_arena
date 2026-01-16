def comb_sort(arr):
    gap = len(arr)
    shrink = 1.3
    sorted_flag = False

    while not sorted_flag:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted_flag = True

        i = 0
        while i + gap < len(arr):
            yield ("compare", i, i + gap)
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                yield ("swap", i, i + gap)
                sorted_flag = False
            i += 1
