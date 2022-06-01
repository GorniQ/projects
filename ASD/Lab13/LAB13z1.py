import time

MAXN = 45
UNKNOWN = -1
f = [UNKNOWN for _ in range(MAXN+1)]

##############################
# 2.1
##############################


def fib_r(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib_r(n-1) + fib_r(n-2)

##############################
# 2.2
##############################


def fib_c(n):
    if f[n] == UNKNOWN:
        f[n] = fib_c(n-1) + fib_c(n-2)
    return f[n]


def fib_c_driver(n):
    f[0] = 0
    f[1] = 1
    for i in range(2, n+1):
        f[i] = UNKNOWN
    return fib_c(n)

##############################
# 2.3
##############################


def fib_dp(n):
    f = [0, 1]
    for i in range(2, n+1):
        f.append(f[i-1] + f[i-2])
    return f[n]

##############################
# 2.4
##############################


def fib_dp_2(n):
    f = [0, 1]
    for i in range(2, n+1):
        f.append(f[1] + f[0])
        f.pop(0)
    return f[1]
##############################
# 3a
##############################


MATCH = 0
INSERT = 1
DELETE = 2


def string_compare(s, t, i, j):
    opt = [None, None, None]
    if i == 0:
        return j*indel(' ')
    if j == 0:
        return i*indel(' ')
    opt[0] = string_compare(s, t, i - 1, j - 1) + match(s[i], t[j])
    opt[1] = string_compare(s, t, i, j - 1) + indel(t[j])
    opt[2] = string_compare(s, t, j - 1, i) + indel(s[i])

    lowest_cost = opt[0]
    for k in range(1, 3):
        if opt[k] < lowest_cost:
            lowest_cost = opt[k]
    return lowest_cost


def match(c, d): return 0 if c == d else 1


def indel(c): return 1

##############################
# 3b
##############################


class Cell:
    MAXLEN = 45

    def __init__(self):
        self.cost = 0
        self.parent = -1


m = [[Cell() for x in range(Cell.MAXLEN + 1)] for y in range(Cell.MAXLEN + 1)]

MATCH = 0
INSERT = 1
DELETE = 2


def string_compare_pd(s, t, i, j):
    opt = [None, None, None]

    def row_init(i):
        m[0][i].cost = i
        if i > 0:
            m[0][i].parent = INSERT
        else:
            m[0][i].parent = -1

    def column_init(i):
        m[i][0].cost = i
        if i > 0:
            m[i][0].parent = DELETE
        else:
            m[i][0].parent = -1

    for i in range(Cell.MAXLEN):
        row_init(i)
        column_init(i)

    for i in range(1, len(s)):
        for j in range(1, len(t)):
            opt[MATCH] = m[i-1][j-1].cost + match(s[i], t[j])
            opt[INSERT] = m[i][j-1].cost + indel(s[i])
            opt[DELETE] = m[i-1][j].cost + indel(s[i])

            m[i][j].cost = opt[MATCH]
            m[i][j].parent = MATCH
            for k in range(INSERT, DELETE+1):
                if opt[k] < m[i][j].cost:
                    m[i][j].cost = opt[k]
                    m[i][j].parent = k

    return m[len(s)-1][len(t)-1].cost


##############################
# 3c
##############################

def reconstruct_patch(s, t, i, j):
    if i is None:
        i = len(s) - 1
    if j is None:
        j = len(t) - 1

    if m[i][j].parent == -1:
        return None
    if m[i][j].parent == -1:
        return
    if m[i][j].parent == MATCH:
        reconstruct_patch(s, t, i-1, j-1)
        match_out(s, t, i, j)
        return
    if m[i][j].parent == INSERT:
        reconstruct_patch(s, t, i, j-1)
        insert_out(t, j)
        return
    if m[i][j].parent == DELETE:
        reconstruct_patch(s, t, i-1, j)
        delete_out(s, i)
        return


def match_out(s, t, i, j):
    if s[i] == t[j]:
        print("M", end='')
    else:
        print("S", end='')


def insert_out(t, j):
    print("I", end='')


def delete_out(s, i):
    print("D", end='')

##############################
# 3d
##############################


def string_compare_pd_3d(s, t, i, j):
    opt = [0, 0, 0]

    def row_init(i):
        m[0][i].cost = 0
        m[0][i].parent = -1

    def column_init(i):
        m[i][0].cost = i
        if i > 0:
            m[i][0].parent = DELETE
        else:
            m[i][0].parent = -1

    for i in range(Cell.MAXLEN):
        row_init(i)
        column_init(i)

    for i in range(1, len(s)):
        for j in range(1, len(t)):
            opt[MATCH] = m[i-1][j-1].cost + match(s[i], t[j])
            opt[INSERT] = m[i][j-1].cost + indel(s[i])
            opt[DELETE] = m[i-1][j].cost + indel(s[i])

            m[i][j].cost = opt[MATCH]
            m[i][j].parent = MATCH
            for k in range(INSERT, DELETE+1):
                if opt[k] < m[i][j].cost:
                    m[i][j].cost = opt[k]
                    m[i][j].parent = k

    i = len(s) - 1
    j = 0
    for k in range(1, len(t)):
        if m[i][k].cost < m[i][j].cost:
            j = k

    return m[i][j].cost

##############################
# 3e
##############################


def string_compare_pd_3e(s, t, i, j):
    opt = [None, None, None]
    def match(c, d): return 0 if c == d else Cell.MAXLEN

    def row_init(i):
        m[0][i].cost = i
        if i > 0:
            m[0][i].parent = INSERT
        else:
            m[0][i].parent = -1

    def column_init(i):
        m[i][0].cost = i
        if i > 0:
            m[i][0].parent = DELETE
        else:
            m[i][0].parent = -1

    for i in range(Cell.MAXLEN):
        row_init(i)
        column_init(i)

    for i in range(1, len(s)):
        for j in range(1, len(t)):
            opt[MATCH] = m[i-1][j-1].cost + match(s[i], t[j])
            opt[INSERT] = m[i][j-1].cost + indel(s[i])
            opt[DELETE] = m[i-1][j].cost + indel(s[i])

            m[i][j].cost = opt[MATCH]
            m[i][j].parent = MATCH
            for k in range(INSERT, DELETE+1):
                if opt[k] < m[i][j].cost:
                    m[i][j].cost = opt[k]
                    m[i][j].parent = k

    return m[len(s)-1][len(t)-1].cost


def reconstruct_patch_3e(s, t, i, j):
    def match_out(s, t, i, j):
        if s[i] == t[j]:
            print(s[i], end='')

    if m[i][j].parent == -1:
        return None

    if m[i][j].parent == MATCH:
        reconstruct_patch_3e(s, t, i - 1, j - 1)
        match_out(s, t, i, j)
        return None

    if m[i][j].parent == INSERT:
        reconstruct_patch_3e(s, t, i, j - 1)
        return None

    if m[i][j].parent == DELETE:
        reconstruct_patch_3e(s, t, i - 1, j)
        return None


def main():

    # start = time.time()
    # res = fib_r(40)
    # print("---1 loop --- %s seconds ---" % (time.time() - start))
    # print(res)
    print("=====Podpunkt 2.2======")
    start = time.time()
    res = fib_c_driver(40)
    print("--- %s seconds ---" % (time.time() - start))
    print("Result: ", res)
    print("======================\n")

    print("=====Podpunkt 2.3======")
    start = time.time()
    res = fib_dp(40)
    print("--- %s seconds ---" % (time.time() - start))
    print("Result: ", res)
    print("======================\n")

    print("=====Podpunkt 2.4======")
    start = time.time()
    res = fib_dp_2(40)
    print("--- %s seconds ---" % (time.time() - start))
    print("Result: ", res)
    print("\n")

    print("=====Podpunkt 3b======")
    start = time.time()
    s = ' kot'
    t = ' kon'
    res = string_compare(s, t, len(s) - 1, len(t) - 1)
    print("--- %s seconds ---" % (time.time() - start))
    print("Result: ", res)
    print("======================\n")

    print("=====Podpunkt 3b======")
    start = time.time()
    s = ' kot'
    t = ' pies'
    res = string_compare(s, t, len(s) - 1, len(t) - 1)
    print("--- %s seconds ---" % (time.time() - start))
    print("Result: ", res)
    print("======================\n")

    print("=====Podpunkt 3c======")
    start = time.time()
    s = ' thou shalt not'
    t = ' you should not'
    res = string_compare_pd(s, t, len(s) - 1, len(t) - 1)
    print("--- %s seconds ---" % (time.time() - start))
    print("Result: ", res)
    reconstruct_patch(s, t, len(s) - 1, len(t) - 1)
    print("\n======================\n")

    print("=====Podpunkt 3d======")
    start = time.time()
    t = ' ban'
    s = ' mokeyssbanana'
    res = string_compare_pd_3d(s, t, len(s) - 1, len(t) - 1)
    print("--- %s seconds ---" % (time.time() - start))
    print("Result: ", res)
    reconstruct_patch(s, t, len(s) - 1, len(t) - 1)
    print("\n======================\n")

    print("=====Podpunkt 3e======")
    start = time.time()
    s = ' democrat'
    t = ' republican'
    res = string_compare_pd_3e(s, t, len(s) - 1, len(t) - 1)
    print("--- %s seconds ---" % (time.time() - start))
    print("Result: ", res)
    reconstruct_patch_3e(s, t, len(s) - 1, len(t) - 1)
    print("\n======================\n")

    print("=====Podpunkt 3f======")
    start = time.time()
    t = ' 243517698'
    s = sorted(t)
    res = string_compare_pd_3e(s, t, len(s) - 1, len(t) - 1)
    print("--- %s seconds ---" % (time.time() - start))
    print("Result: ", res)
    reconstruct_patch_3e(s, t, len(s) - 1, len(t) - 1)
    print("\n======================\n")


main()
