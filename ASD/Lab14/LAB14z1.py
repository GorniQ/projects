import numpy as np
import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def Jarvis(pts):
    # Wyszykiwanie najbardziej wysuniętego w
    # lewo puntu i najniżej połozonego puntku
    lp = min(pts, key=lambda p: (p.x, p.y))
    p = lp
    result = []
    # Algorytm wyznaczania otoczki
    while True:
        result.append((p.x, p.y))
        q = pts[(pts.index(p) + 1) % len(pts)]
        for r in pts:
            # Wyzanczanie orjentacji ze wzoru
            val = (r.y-p.y)*(q.x-r.x) - (r.x-p.x)*(q.y-r.y)
            # Sprawdzenie czy jest lewoskrętny
            if val < 0:
                q = r
        p = q
        # Jeżeli wrócilismy do początkowego break
        if p == lp:
            break
    return result


def Jarvis_2(pts):
    # Wyszykiwanie najbardziej wysuniętego w
    # lewo puntu i najniżej połozonego puntku
    lp = min(pts, key=lambda p: (p.x, p.y))
    p = lp
    result = []
    # Algorytm wyznaczania otoczki
    while True:
        result.append((p.x, p.y))
        q = pts[(pts.index(p) + 1) % len(pts)]
        for r in pts:
            # Wyzanczanie orjentacji ze wzoru
            val = (r.y-p.y)*(q.x-r.x) - (r.x-p.x)*(q.y-r.y)
            # Jeżeli mniejsze od zera - lewoskrętny
            if val < 0:
                q = r
            # Jeżeli równy zero - liniowy
            elif val == 0:
                # Wyznaczenie najdalszego współliniowego punktu
                if p.x < q.x < r.x or p.x > q.x > r.x or p.y < q.y < r.y or p.y > q.y > r.y:
                    q = r
        p = q
        # Jeżeli wrócilismy do początkowego break
        if p == lp:
            break
    return result

    # Oblicznie dystansu
def distance(p0, p1):
    return math.sqrt((p0.x-p1.x)**2 + (p0.y-p1.y)**2)

    # Oblicznie kąta
def angle(p1, p2):
    if p1.x != p2.x:
        return np.arctan((p1.y-p2.y)/(p1.x-p2.x))
    else:
        return np.pi/2


def Graham(pts):
    res = []

    # Wyszukiwanie namniejszego punktu p0 ze zbioru
    p0 = min(pts, key=lambda p: (p.x, p.y))
    res.append(p0)

    # Obicznie kąta dla każdego puntu
    angleslst = []
    for p in pts:
        if p != p0:
            angleslst.append((p, angle(p, p0)))

    # Sortowanie listy
    sortedlst = sorted(angleslst, key=lambda p: p[1])

    # Lista zawierające listy punktów o tym samym kącie
    new_list = []
    for point, value in sortedlst:
        if new_list and new_list[-1][0][1] == value:
            new_list[-1].append((point, value))
        else:
            new_list.append([(point, value)])

    # Dodawanie najdalszych punktów do listy
    for elem in new_list:
        if len(elem) > 1:
            maxdist = 0
            farest = p0
            for p, ang in elem:
                if distance(p0, p) > maxdist:
                    maxdist = distance(p0, p)
                    farest = p
            res.append(farest)
        else:
            res.append(elem[0][0])

    # Wyznacznie otoczki
    if len(res) < 3:
        return None
    else:
        stack = res[0:3]
        size = 3
        for i in range(3, len(res)):
            while True:
                value = (stack[-1].y-stack[-2].y)*(res[i].x-stack[-1].x) - \
                    (stack[-1].x-stack[-2].x)*(res[i].y-stack[-1].y)
                if value < 0:
                    break
                else:
                    stack.pop()
                    size -= 1
            stack.append(res[i])
            size += 1
    result = [(p.x, p.y) for p in stack]
    return result


def main():
    points1 = [(0, 3), (0, 0), (0, 1), (3, 0), (3, 3)]
    pts1 = []
    for x, y in points1:
        pts1.append(Point(x, y))

    print("===========Jarvis===========")
    print("Lista początkowa:")
    print(points1)
    print("Wynik:")
    res1 = Jarvis(pts1)
    print(res1)
    print("\n")

    points2 = [(0, 3), (0, 1), (0, 0), (3, 0), (3, 3)]
    pts2 = []
    for x, y in points2:
        pts2.append(Point(x, y))

    print("===========Jarvis===========")
    print("Lista początkowa:")
    print(points2)
    print("Wynik:")
    res2 = Jarvis(pts2)
    print(res2)
    print("\n")

    points = [(2, 2), (4, 3), (5, 4), (0, 3), (0, 2),
              (0, 0), (2, 1), (2, 0), (4, 0)]
    pts = []
    for x, y in points:
        pts.append(Point(x, y))

    print("===========Jarvis===========")
    print("Lista początkowa:")
    print(points)
    print("Wynik:")
    res = Jarvis(pts)
    print(res)
    print("\n")

    print("===========Jarvis po modyfikacji===========")
    print("Lista początkowa:")
    print(points)
    print("Wynik:")
    res = Jarvis_2(pts)
    print(res)
    print("\n")

    points = [(0, 3), (1, 1), (2, 2), (4, 4), (0, 0), (1, 2), (3, 1), (3, 3)]
    pts = []
    for x, y in points:
        pts.append(Point(x, y))

    print("===========Graham===========")
    print("Lista początkowa:")
    print(points)
    print("Wynik:")
    res = Graham(pts)
    print(res)
    print("\n")


main()