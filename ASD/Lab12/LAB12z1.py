#Skończone
import time


def naive_search(S: str, W: str):
    start_time = time.time()
    N = len(W)
    M = len(S)
    if N > M:
        print("--- %s seconds ---" % (time.time() - start_time))
        print("Pattern is longer than checked text")
        return
    count = 0
    idxlst = []
    i = W[0]
    for m in range(M):
        if S[m] == i:
            isDiff = False
            for ch in range(N):
                if W[ch] != S[m+ch]:
                    isDiff = True
                    break
            if not isDiff:
                count += 1
                idxlst.append(m)
    print("--- %s seconds ---" % (time.time() - start_time))
    if count < 0:
        print("No matching word found")
        return count, idxlst
    return count, idxlst


def rk_search(S: str, W: str):
    start_time = time.time()
    N = len(W)
    M = len(S)
    if N > M:
        print("--- %s seconds ---" % (time.time() - start_time))
        print("Pattern is longer than checked text")
        return

    count = 0
    idxlst = []
    d = 256
    q = 101
    s = 0
    w = 0
    h = 1

    for i in range(N-1):
        h = (h*d) % q
    for i in range(N):
        w = (d*w + ord(W[i])) % q
        s = (d*s + ord(S[i])) % q

    for m in range(M-N+1):
        if s == w:
            isDiff = False
            for i in range(N):
                if S[m+i] != W[i]:
                    isDiff = True
                    break

            if not isDiff:
                count += 1
                idxlst.append(m)
        if m < M - N:
            s = (d*(s - ord(S[m])*h) + ord(S[m+len(W)])) % q
            if s < 0:
                s += q

    print("--- %s seconds ---" % (time.time() - start_time))
    if count < 0:
        print("No matching word found")
        return count, idxlst
    return count, idxlst


def kmp_search(S: str, W: str):
    start_time = time.time()
    N = len(W)
    M = len(S)
    if N > M:
        print("--- %s seconds ---" % (time.time() - start_time))
        print("Pattern is longer than checked text")
        return
    P = []
    nP = 0
    m = 0
    i = 0
    T = kmp_table(W)
    while m < M:
        if W[i] == S[m]:
            m += 1
            i += 1
            if i == N:
                P.append(m-i)
                nP += 1
                i = T[i-1]
        else:
            i = T[i]
            if i < 0:
                m += 1
                i += 1
    print("--- %s seconds ---" % (time.time() - start_time))
    if nP < 0:
        print("No matching word found")
        return nP, P
    return nP, P


def kmp_table(W):
    N = len(W)
    T = [0 for _ in range(N)]
    pos = 1
    cnd = 0
    T[0] = -1
    while pos < N:
        if W[pos] == W[cnd]:
            T[pos] = T[cnd]
        else:
            T[pos] = cnd
            while cnd >= 0 and W[pos] != W[cnd]:
                cnd = T[cnd]
        pos += 1
        cnd += 1
    return T


def main():
    with open('lotr.txt', encoding='utf-8') as f:
        text = f.readlines()
    S = ' '.join(text).lower()

    tekst = "they ran around the corner to find that they had traveled back in time"
    wzor = "they"

    print("=================================")
    print("Prosty tekst (Naive search):\n")
    print(naive_search(tekst, wzor))
    print("=================================")
    print("Slowo 'laugh' w lotr.txt (Naive search):\n")
    print(naive_search(S, "laugh"))
    print("=================================")
    print("Slowo 'laugh' w lotr.txt (Rabin-Karp search):\n")
    print(rk_search(S, "laugh"))
    print("=================================")
    print("Slowo 'laugh' w lotr.txt (Knuth-Morris-Pratt search):\n")
    print(kmp_search(S, "laugh"))


main()
