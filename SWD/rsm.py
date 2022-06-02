import numpy as np
from matplotlib import pyplot as plt


# Kod sprawdzający czy punk u jest w prostokącie zawartym miedzy dwoma punktami
def sprawdz(p1, u, p2):
    x1, y1 = p1
    xu, yu = u
    x2, y2 = p2
    isInside = False
    if (x1 <= xu <= x2 or x1 >= xu >= x2) and (y1 <= yu <= y2 or y1 >= yu >= y2):
        isInside = True
    return isInside

# Kod obliczjący pole prostokata miedzy dwoma punktami


def calculate_area(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    a = np.abs(x2-x1)
    b = np.abs(y2-y1)
    pole = a*b
    return pole

# Kod obliczjący wspólczynnik odleglosci wykorzystany do skoringu


def wsp_skor_odl(p1, u, p2):
    odl1 = np.sqrt((u[0] - p1[0])**2 + (u[1] - p1[1])**2)
    odl2 = np.sqrt((u[0] - p2[0])**2 + (u[1] - p2[1])**2)
    wsp = odl1/(odl1+odl2)
    return wsp

# Funkcja obliczjaca skoring dla jednego punktu u


def skoring(A1, u, A2):
    # Suma pól
    S = 0
    # Lista ktotek pol i wsp odl
    pola = []
    for a1 in A1:
        for a2 in A2:
            if sprawdz(a1, u, a2):
                P_i = calculate_area(a1, a2)
                S += P_i
                f_i = wsp_skor_odl(a1, u, a2)
                pola.append((P_i, f_i))

    # Skoring
    F = sum([(Pi/S)*wsp for Pi, wsp in pola])
    return F

# Funkcja wyznaczająca ranking


def ranking(A1, U, A2):
    ranking = [(u, skoring(A1, u, A2)) for u in U]
    ranking.sort(key=lambda x: x[1])
    print("Rank\t: Point \t Skoring")
    for i in range(len(ranking)):
        print(f'{i+1}\t: {ranking[i][0]}\t {round(ranking[i][1], 2)}')
    return ranking


if __name__ == '__main__':

    A1 = [(1, 6), (2, 5), (4, 4), (5, 3), (8, 2)]
    U = [(1, 13), (2, 10), (3, 8), (4, 5), (8, 3)]
    A2 = [(3, 13), (9, 8), (7, 11), (6, 6), (11, 9)]
    klasy = [[(1, 6), (2, 5), (4, 4), (5, 3), (8, 2)],
             [(1, 13), (2, 10), (3, 8), (4, 5), (8, 3)],
             [(3, 13), (9, 8), (7, 11), (6, 6), (11, 9)]]

    ranking(A1, U, A2)

    plt.axis([0, 15, 0, 15])
    # for lst in klasy:
    #     x, y = zip(*lst)
    #     plt.plot(x, y, 'o')
    #     plt.grid()

    style = ['sg', 'ob', '*r']
    for i in range(len(klasy)):
        lst = klasy[i]
        x, y = zip(*lst)
        plt.plot(x, y, style[i])
        plt.grid()

    plt.show()


# Fu.sort(key=lambda tup: tup[0])
# print(Fu)
# while len(Fu) > 0:
#     niezdom = []
#     el0 = Fu[0]
#     niezdom.append(el0)
#     for el in range(1, len(Fu)):
#         el1 = Fu[el]
#         if el0[0] <= el1[0] and el0[1] <= el1[1]:
#             continue
#         elif el0[1] >= el1[1]:
#             isUndominated = True
#             for (a, b) in niezdom:
#                 if a <= el1[0] and b <= el1[1]:
#                     isUndominated = False
#             if isUndominated:
#                 niezdom.append(el1)
#         else:
#             niezdom.clear()
#             el0 = el1
#             niezdom.append(el0)

#     # print(niezdom)
#     # jeżeli mają byc grupowane min po 3 to odkomentowac do ---- i zakomentowac reszte
#     # if klasy and len(klasy[-1]) < 3:
#     #     for el in niezdom:
#     #         klasy[-1].append(el)
#     # else:
#     #     klasy.append(niezdom)
#     # ----
#     klasy.append(niezdom)
#     # ----

#     for i in niezdom:
#         Fu.remove(i)
