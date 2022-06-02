import numpy as np


def topsis(D, typ, waga, isMin=False):
    """
    Funkcja obliczająca metodę TOPSIS

    Inputs:
    D: Macierz decyzyjna
    typ: Wektor opisujący czy kryterium jest maksymalne czy minimalne
    waga: Wektor wag poszczególnych kryteriów
    isMin: Parametr określajacy czy macierz D jest zminimalizowana

    Outputs:
    M: Macierz znoramlizowana
    norma: Norma euklidesowa
    v_i: Punkty idealne
    v_ai: Punkty antyidealne
    d_i: odkegłosci od punktu idealnego
    d_ai: odległości od punktu antyidealnego
    ci: Skoring
    """
    # oblicznie normy euklidesowej
    norma = []
    for i in range(D.shape[1]):
        col = D[:, i]
        suma = 0
        for elem in col:
            suma += elem**2
        norma.append(np.sqrt(suma))
    # normalizowanie
    M = np.zeros((D.shape))
    for col in range(D.shape[1]):
        for row in range(D.shape[0]):
            if not isMin:
                if typ[col] == "MAX":
                    n = 1 - (D[row][col]/norma[col])*waga[col]
                    M[row][col] = n
                else:
                    n = D[row][col]/norma[col]
                    M[row][col] = n
            else:
                n = (D[row][col]/norma[col])*waga[col]
                M[row][col] = n
    # print(M)
    # punkty idealne i antyidealne
    v_i = []
    v_ai = []
    for i in range(M.shape[1]):
        col = M[:, i]
        v_i.append(np.max(col))
        v_ai.append(np.min(col))
    # print(v_i)
    # print(v_ai)

    # odległości
    d_i = []
    d_ai = []

    for row in range(M.shape[0]):
        suma1 = 0
        suma2 = 0
        for col in range(M.shape[1]):
            el1 = (M[row][col] - v_i[col])**2
            suma1 += el1
            el2 = (M[row][col] - v_ai[col])**2
            suma2 += el2
        d_i.append(suma1)
        d_ai.append(suma2)
    # print(d_i)
    # print(d_ai)

    # skoring
    ci = []
    for i in range(len(d_i)):
        el = d_i[i]/(d_i[i]+d_ai[i])
        ci.append(el)
    # print(ci)

    return (M, norma, v_i, v_ai, d_i, d_ai, ci)


def show_ranking(ci, modele):
    # krotki laptopów
    res = []
    for i in range(len(ci)):
        res.append((modele[i], ci[i]))
    res.sort(key=lambda x: x[1])
    ranking = res[::-1]

    print("RANKING:")
    for i in range(len(ranking)):
        print(f"{i+1}: {ranking[i]}")


if __name__ == '__main__':
    # Krytreria (kolejno): ilosc rdzeni, taktowanie, rozdzielczość, rozmiear SSD, ilosc RAM, czas baterii, cena, gwarancja, GPU, rozmiar ekranu
    # typ Kryteria:
    typ = ["MAX", "MAX", "MAX", "MAX", "MAX",
           "MAX", "MIN", "MAX", "MAX", "MAX"]
    waga = [0.7, 0.2, 0.1, 0.1, 0.1, 0.5, 1, 0.1, 0.5, 0.1]

    D = np.array(([[4, 3.9, 1980 * 1080, 256, 16, 13, 8299, 36, 1, 14],
                   [4, 4.2, 3000 * 2000, 256, 8, 17, 7399, 12, 4, 13],
                   [4, 3.6, 1920 * 1080, 512, 8, 13, 3200, 24, 1, 14],
                   [6, 4.5, 1920 * 1080, 256, 8, 4, 4549, 24, 6, 17],
                   [2, 3.1, 1920 * 1080, 256, 16, 17, 4049, 36, 1,	14],
                   [4, 3.7, 3000 * 2000, 256, 8, 12, 8199, 12, 2, 13],
                   [4, 3.7, 1920 * 1080, 256, 8, 9.5, 2699, 24, 2, 14],
                   [4, 3.5, 2560 * 1600, 256, 8, 11, 5399, 12, 1, 13],
                   [6, 4.5, 1920 * 1080, 512, 16, 6, 7299, 24, 7, 15.6],
                   [4, 4.6, 1920 * 1080, 512, 8, 14, 5099, 24, 2, 13.3],
                   [4, 4.6, 1920 * 1080, 960, 32, 10, 7699, 36, 1, 14],
                   [6, 4.7, 1920 * 1080, 512, 16, 10, 5099, 24, 2.5, 14],
                   [4, 4.2, 1920 * 1080, 512, 16, 14, 5099, 24, 2, 15],
                   [4, 3.7, 1920 * 1080, 256, 8, 15, 5699, 36, 2, 14],
                   [6, 5.1, 1920 * 1080, 512, 16, 20, 10499, 36, 3, 15],
                   [4, 3.6, 1920 * 1080, 512, 16, 4, 4399, 36, 1, 15]]))

    modele = ["DELL 7400",
              "MS surface book 2",
              "Acer swift 3",
              "MSI gl75",
              "Lenovo thinkpad t470",
              "MS surface book 3",
              "Huawei matebook d14",
              "Macbook Air 2017",
              "Lenovo Legion Y740-15IRHg i7",
              "Asus ZenBook ux333fn",
              "HP EliteBook 840 G6",
              "MSI Prestige 14",
              "Lenovo thinkpad l15",
              "Lenovo thinkpad t495",
              "DELL precition 3551",
              "DELL vostro 5501"]

    (M, norma, v_i, v_ai, d_i, d_ai, ci) = topsis(D, typ, waga)
    show_ranking(ci, modele)


Fu = [(4, 4),
      (5, 4),
      (-2, 0),
      (0, 1),
      (2, 1),
      (1, -3),
      (4, 1),
      (3, 2),
      (3, 3),
      (3, -1),
      (-1, 1),
      (0, -1),
      (4, -2),
      (-1, 3),
      ]
