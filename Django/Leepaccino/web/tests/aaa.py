

def triangle(row):
    rgb = set(['R', 'G', 'B'])

    row = [str_ for str_ in row]

    def bb(row_):
        print(row_)
        aaa = []
        for i in range(len(row_) - 1):
            a = set([row_[i], row_[i + 1]])
            if len(a) == 1:
                aaa.append(row_[i])
            else:
                cc = rgb.difference(a)
                aaa.extend(c for c in cc)
        return list(aaa)

    bb_ = bb(row)
    while len(bb_) > 1:
        bb_ = bb(bb_)
    return bb_[0]


triangle('RBRGBRBGGRRRBGBBBGG')


def fib(n):
    a, b = 0, 1
    if n == 1:
        return 1
    if n == 0:
        return 0
    for i in range(n):
        # print(a)
        a, b = a+b, a
    return a
print(fib(6))
