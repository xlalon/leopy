# coding: utf-8 -*-


def bubble_sort(lst):
    for i in range(len(lst)):
        max_i = i
        for j in range(i, len(lst)):
            if lst[max_i] < lst[j]:
                max_i = j
        lst[i], lst[max_i] = lst[max_i], lst[i]
    return lst


def merge_sort(lst):
    if len(lst) <= 1:
        return lst
    mid = len(lst)//2
    lft = merge_sort(lst[:mid])
    rgt = merge_sort(lst[mid:])
    result = []
    while lft and rgt:
        if lft[0] <= rgt[0]:
            result.append(lft.pop(0))
        else:
            result.append(rgt.pop(0))
    if lft or rgt:
        result.extend(lft or rgt)
    return result


def quick_sort(lst):
    if len(lst) <= 1:
        return lst
    lft = [x for x in lst[1:] if x <= lst[0]]
    rgt = [x for x in lst[1:] if x > lst[0]]
    return quick_sort(lft) + lst[:1] + quick_sort(rgt)


def max_heap(data, i):
    data_len = len(data)
    lft = 2 * i + 1
    rgt = lft + 1
    max_idx = i
    if lft < data_len and data[i] < data[lft]:
        max_idx = lft
    if rgt < data_len and data[max_idx] < data[rgt]:
        max_idx = rgt
    if max_idx != i:
        data[i], data[max_idx] = data[max_idx], data[i]
        max_heap(data, max_idx)


def heap_fy(data):
    data_len = len(data)
    for i in range(data_len//2, -1, -1):
        # print(data, i, data[i])
        max_heap(data, i)


def pop_max(data):
    data_len = len(data)
    data[0], data[data_len-1] = data[data_len-1], data[0]
    max_data = data.pop()
    heap_fy(data)
    return max_data


def heap_ins(data, d):
    data.insert(0, d)
    heap_fy(data)
    return data


def head_sort(data):
    data_len = len(data)
    data_sort = []
    for _ in range(data_len):
        data_sort.append(pop_max(data))
    return data_sort


if __name__ == '__main__':
    pass
