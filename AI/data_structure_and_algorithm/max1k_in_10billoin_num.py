# -*- coding: utf-8 -*-

from random import randint
from heapq import heapify, heappushpop


def ccc(max_1q_lst, num, rand_num):
    j = 1
    for x in range(num):
        # 运行了10000000次后打印一下XXX, 打印前10个数字
        if x % 10 ** 8 == 0:
            print('Round {}, nums: '.format(j), max_1q_lst[:10])
            j += 1
        # 随机数字
        y = randint(1, rand_num)
        # 如果比最小的数字大，插入数字Y，删除最小的数字
        if y > max_1q_lst[0]:
            heappushpop(max_1q_lst, y)


if __name__ == '__main__':
    lst = [float('-inf')] * 1000
    print('length_a_begin: ', len(lst))
    heapify(lst)
    num_n, rand_m = 10**12, 10**13

    ccc(lst, num_n, rand_m)
    print('length_a_end: ', len(lst))
