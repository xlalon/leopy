# coding: utf-8 -*-


class Node:
    def __init__(self, data, lft=None, rgt=None):
        self.data = data
        self.lft = lft
        self.rgt = rgt


def is_search_bin_tree(tree):
    # 判定一个给定根节点的树是否是一颗搜索二叉树
    tree_data = []

    def travel(t):
        if t.lft:
            travel(t.lft)
        tree_data.append(t.data)
        if t.rgt:
            travel(t.rgt)
    travel(tree)
    print(tree_data)
    for i in range(1, len(tree_data)):
        if tree_data[i] < tree_data[i-1]:
            return False
    else:
        return True


if __name__ == '__main__':
    tree_1 = Node(10, Node(6, Node(5), Node(7)), Node(20, Node(11), Node(21)))
    tree_2 = Node(10, Node(6, Node(5), Node(7)), Node(20, Node(11), Node(19)))
    tree_3 = Node(10, Node(6, Node(5), Node(20)), Node(20, Node(11), Node(21)))
    tree_4 = Node(10, Node(6, Node(5), Node(7)), Node(7, Node(11), Node(21)))
    print(is_search_bin_tree(tree_1))
    print(is_search_bin_tree(tree_2))
    print(is_search_bin_tree(tree_2))
    print(is_search_bin_tree(tree_2))
