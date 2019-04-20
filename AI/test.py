m = [1, 4, 16, 64]
buy = int(input('buy: '))
banlancy = 1024 - buy
coint = []
last = len(m)-1
while banlancy >= 0 and last > -1:
	if banlancy >= m[last]:
		banlancy -= m[last]
		coint.append(m[last])
	else:
		last -= 1
print('coint:{}, count: {}'.format(coint, len(coint)))
