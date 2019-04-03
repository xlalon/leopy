# -*- coding: utf-8 -*-
def dict2_hds(src):
	if isinstance(src, dict):
		for k, v in src.items():
			print('{}: {}'.format(k, v))


def bubble_sort(lst):
	for i in range(len(lst)):
		max_i = i
		for j in range(i, len(lst)):
			if lst[max_i] < lst[j]:
				max_i = j
		lst[i], lst[max_i] = lst[max_i], lst[i]
	return lst


def quick_sort(lst):
	if len(lst) <= 1:
		return lst 
	lft = [x for x in lst[1:] if x <=lst[0]]
	rgt = [x for x in lst[1:] if x >lst[0]]
	return quick_sort(lft) + lst[:1] + quick_sort(rgt)


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


def worm():
	from requests import get
	import re
	from lxml.html import etree
	from lxml.cssselect import CSSSelector

	def get_book(url):
		return get(url, headers=headers()).content.decode('utf8')
	xuan_huan_qidian = 'https://www.qidian.com/xuanhuan'
	r = get_book(xuan_huan_qidian)
	e_string = etree.fromstring(r)
	print(dir(e_string))
	# book_domain = 'book.qidian.com'
	# a_href = r'< href="//{}(.*?)" '.format(book_domain)
	# infos = re.findall(a_href, r)
	# books = ['https://' + book_domain + info + '#Catalog' for info in infos]
	# books_1 = books[:1]
	# lable_a = r'<a href="//{}(.*?)'.format(book_domain)
	# for book in books_1:
	# 	print(book)
	# 	book_cate = get(book, headers=headers()).content.decode()
	# 	print(book_cate)


def user_agent():
	from fake_useragent import UserAgent
	return UserAgent().chrome


def headers():
	random_user_agent = user_agent()
	return {'User-Agent': random_user_agent}


class Node:
	def __init__(self, data, lft=None, rgt=None):
		self.data = data
		self.lft = lft
		self.rgt = rgt


def is_search_bin_tree(tree):
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
	print(a)
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
	a = [1, 6, 9, 14, 6, 18, 20, 50, 3, 9, 8]
	heap_fy(a)
	# print(pop_max(a))
	# print(pop_max(a))
	# print(pop_max(a))
	# print(head_sort(a))
	print(heap_ins(a, 10))

	# tree_1 = Node(10, Node(6, Node(5), Node(7)), Node(20, Node(11), Node(21)))
	# tree_2 = Node(10, Node(6, Node(5), Node(7)), Node(20, Node(11), Node(19)))
	# tree_3 = Node(10, Node(6, Node(5), Node(20)), Node(20, Node(11), Node(21)))
	# tree_4 = Node(10, Node(6, Node(5), Node(7)), Node(7, Node(11), Node(21)))
	# print(is_search_bin_tree(tree_1))
	# print(is_search_bin_tree(tree_2))
	# print(is_search_bin_tree(tree_2))
	# print(is_search_bin_tree(tree_2))
	# worm()
#	from xmlrpc.server import SimpleXMLRPCServer
#	rpc_s = SimpleXMLRPCServer(('localhost', 8000))
#	rpc_s.register_function(quick_sort)
#	rpc_s.serve_forever()
 
