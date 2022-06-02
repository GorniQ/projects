from typing import List, Any, Dict, Callable, Tuple, Union
import numpy as np
import networkx as nx
from mieszkania import B, weight, v, przedz
import matplotlib.pyplot as plt
from fuzzy_topsis import fuzzy_topsis
from UTA import UTA_v2
from RSM import RSM_v2


# Funkcja zwracająca wektor n elementowy, gdzie: n - liczba porównywanych mieszkań.
# Indeks w wektorze odpowiada numerowi punktu, wartość znajdująca się pod tym indeksem jest pozycją w rankingu
def convert(B: Dict[str, Union[int, float, bool]], ranking: List[Tuple[str, float]]) -> List[int]:
    vect = list()
    prev = list()
    for el in B.keys():
        for ob in ranking:
            if ob[0] == el:
                if ob[1] not in prev:
                    vect.append(1 + ranking.index(ob))
                    prev.append(ob[1])
                else:
                    vect.append(ranking.index(ob))

    return vect


# Funkcja zwracająca odległość pomiędzy dwoma zadanymi rankingami.
# Do obliczenia odległości zastosowano metrykę euklidesową.
def compare_rankings_1(B, rank1, rank2):
    rank1_ = convert(B, rank1)
    rank2_ = convert(B, rank2)
    if len(rank1_) == len(rank2_):
        distance = 0
        sum_ = 0
        for i in range(len(rank1_)):
            if rank1[i][1] != 0 and rank2[i][1] != 0:
                sum_ += (rank1_[i] - rank2_[i]) ** 2
        distance += sum_ ** (1 / 2)
    else:
        raise ValueError
    return int(distance)


# Funkcja zwracająca odległość pomiędzy dwoma zadanymi rankingami.
# Dodano wagi pozwlające określić jakie miejsce w rankingu zajmują punkty.
# Waga jest maksymalną różnicą pomiędzy zajmowanymi miejscami w rankingu przez punktu, a ilością punktów w rankingu.
# Do obliczenia odległości zastosowano metrykę euklidesową.
def compare_rankings_2(B, rank1, rank2):
    rank1_ = convert(B, rank1)
    rank2_ = convert(B, rank2)
    if len(rank1_) == len(rank2_):
        length = len(rank1_)
        distance = 0
        sum_ = []
        for i in range(len(rank1_)):
            if rank1[i][1] != 0 and rank2[i][1] != 0:
                sum_.append((rank1_[i] - rank2_[i]) ** 2)

        for i in range(len(rank1_)):
            if rank1[i][1] != 0 and rank2[i][1] != 0:
                distance += max(length - rank1_[i], length - rank2_[i]) * sum_[i]
    else:
        raise ValueError

    return int(distance ** (1 / 2))


# Funkcja tworząca na podstawie listy rankingów macierz sąsiedztwa, która zawiera informacje o odległości
# pomiędzy każdą parą rankingów. Wkorzystywana jest do wizualizacji odległości pomiędzy rankingami.
def matrix_of_rank_value(B: Dict[str, Union[int, float, bool]], rankings: List[List[Tuple[str, float]]], weight: bool) -> np.ndarray:
    matrix = np.zeros((len(rankings), len(rankings)))

    for row in range(len(rankings)):
        for col in range(len(rankings)):
            if row == col:
                matrix[row][col] = 0
            else:
                if weight:
                    matrix[row][col] = compare_rankings_2(B, rankings[row], rankings[col])
                else:
                    matrix[row][col] = compare_rankings_1(B, rankings[row], rankings[col])

    return matrix.astype(int)


# Funkcja tworząca graf z wagami, gdzie wagi reprezentują odległości pomiędzy rankingami.
# Do utworzenia grafu wykorzystano bibliotekę NetworkX - wykorzystywaną
# do rozwiązywania i wizualizacji problemów grafowych.
# Metoda RSM zwraca ranking zwierający mniejszą ilość miast
# z tego powodu porównanie rankingów w przypadku metody RSM z pozostałymi przeprowadzono
# dla miast, których wartość funkcji skoringowej była różna od zera.
def plot_graph(matrix: np.ndarray):
    labeldict = dict()
    labeldict[0] = "Fuzzy Topsis"
    labeldict[1] = "UTA"
    labeldict[2] = "RSM"
    # labeldict[0] = "Metoda 1"
    # labeldict[1] = "Metoda 2"
    # labeldict[2] = "Metoda 3"
    plt.figure(figsize=(12, 6))
    G = nx.from_numpy_matrix(np.matrix(matrix), create_using=nx.DiGraph())
    layout = nx.spring_layout(G)
    nx.draw(G, layout, node_size=400, labels=labeldict, node_color="green", with_labels=True, font_weight='bold', font_size=12, font_color="red", width=3, edge_color="tab:green")
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=labels, font_size=12)
    plt.show()


# Funkcja wykorzystywana do sortowania danych rankingów względem wartości funkcji skoringowej
# - mieszkania posortowane są od największej do najmniejszej wartości funkcji skoringowej.
def sort(rank):
    new_rank = list()
    lista = [el[1] for el in rank]
    zabr = []
    while len(lista) > len(zabr):
        wiekszy = float("-inf")
        for id in range(len(lista)):
            if id not in zabr:
                if wiekszy < lista[id]:
                    wiekszy = lista[id]

        id_max = lista.index(wiekszy)
        if id_max in zabr:
            zabr.append(id_max + 1)
            new_rank.append(rank[id_max + 1])
        else:
            zabr.append(id_max)
            new_rank.append(rank[id_max])
    return new_rank


# Funkcja zwaracjąca dwuelementową krotkę. Pierwszym elementem jest macierz nxm,
# gdzie n - liczba maieszkań, m - liczba porównywanych metod zawierająca informacje o pozycji punktów w rankingach
# Drugim element stanowi macierz nxm zawierająca informację o wartościach funkcji skoringowych
# punktów znajdujących się w pierwszej macierzy.
def convert_to_two_matrix(B, list_of_ranking):
    convert_list = list()
    for i in range(len(list_of_ranking)):
        convert_list.append(convert(B, list_of_ranking[i]))
    matrix_of_rank = np.array(convert_list)

    value_list = list()
    for i in range(len(convert_list)):
        value_list.append([list_of_ranking[i][x - 1][1] for x in convert_list[i]])
    matrix_of_value = np.array(value_list)

    return matrix_of_rank.T, matrix_of_value.T


# Główna funkcja wykorzystana do porówanania rankingów. Generuje porównanie rankingów w przestrzeni 2D oraz 3D.
# Znaczącą część ciała funkcji stanowi zobrazowanie w przestrzni trójwymiarowej punktów reprezentujących
# mieszkania rozmieszczonych w przestrzeni zgodnie z wartościami odpowiadającym imfunkcji skoringowych.
# Punkty w przestrzni zostały oznaczone kolumną zawierającą informacje o miejscach jakie zajmują w rankigach
# dla metod, zaczynając od góry: metoda pierwsza - fuzzy topsis, metoda druga - UTA, metoda trzecia - RSM.
# Dodatkowo funkcja uzupełnia ranking danej metody jeżeli jego rozmiar różni się od rozmiaru
# rankingów pozostałych metod.
def compare_rank_main_function(B, list_of_ranks, weight: bool):
    for rank in list_of_ranks:
        if len(rank) != len(list_of_ranks[0]):
            list_of_rank = [x[0] for x in rank]
            for key in B.keys():
                if key not in list_of_rank:
                    rank.append((key, 0))

    plot_graph(matrix_of_rank_value(B, list_of_ranks, weight))
    ranks, score = convert_to_two_matrix(B, list_of_ranks)

    plt.figure(figsize=(12, 6))
    ax = plt.axes(projection='3d')
    for i, point in enumerate(score[:]):
        ax.scatter(point[0], point[1], point[2])
        ax.text(point[0], point[1], point[2], f"  {ranks[i, 0]}\n  {ranks[i, 1]}\n  {ranks[i, 2]}",
                color='b', fontsize=6)
    ax.legend([f"{key} {list(ranks[i, :])}" for i, key in enumerate(B.keys())], loc='upper right',
              bbox_to_anchor=(-0.2, 0.9))
    ax.dist = 8
    ax.set_xlabel("F. Topsis - $c_i$")
    ax.set_ylabel("UTA - $c_i$")
    ax.set_zlabel("RSM - $c_i$")
    ax.set_title("Zobrazowanie położenia zadanych mieszkań w rankingach")
    #ax.set_xlim3d(0, 1)
    #ax.set_ylim3d(0, 1)
    #ax.set_zlim3d(0, 1)
    plt.show()

'''

fuzzy_topsis_ranking = [('M4', 0.6411899055822099),
                        ('M8', 0.6343823491856333),
                        ('M20', 0.6140660324612152),
                        ('M1', 0.6037907892449208),
                        ('M19', 0.5891113347827847),
                        ('M6', 0.5798591649350768),
                        ('M5', 0.555554597980972),
                        ('M12', 0.5322243919271715),
                        ('M16', 0.5248010433165845),
                        ('M11', 0.523696373019247),
                        ('M15', 0.5136425953910934),
                        ('M10', 0.4940338765296373),
                        ('M13', 0.48613509502843194),
                        ('M17', 0.4825779202349187),
                        ('M9', 0.4794750303408368),
                        ('M14', 0.47660324513498536),
                        ('M3', 0.47147270682535775),
                        ('M2', 0.4275531270005525),
                        ('M18', 0.3547893563079826),
                        ('M7', 0.31499821402338246)]

UTA_ranking = [('M7', 0.3353169581709116),
               ('M18', 0.413482058089694),
               ('M2', 0.4524916557794571),
               ('M13', 0.4787493666529878),
               ('M9', 0.48410627708604026),
               ('M14', 0.48558716850119826),
               ('M3', 0.4952468343838902),
               ('M10', 0.5120576382457797),
               ('M15', 0.534729390070653),
               ('M11', 0.5375566335428608),
               ('M12', 0.5388893965611216),
               ('M17', 0.5523116847065979),
               ('M6', 0.5550251050711148),
               ('M16', 0.5662067768666753),
               ('M19', 0.5784761828139083),
               ('M5', 0.5840933762251673),
               ('M4', 0.5953914364272935),
               ('M20', 0.609694098907297),
               ('M1', 0.6391408743616072),
               ('M8', 0.6505751749116182)]


ranking_3 = [('M19', 0.28114017961733695),
             ('M6', 0.40609137055837563),
             ('M15', 0.4162436548223349),
             ('M18', 0.4263959390862943),
             ('M7', 0.4681331077270164),
             ('M9', 0.49238578680203043),
             ('M12', 0.5076142131979695),
             ('M17', 0.5076142131979695),
             ('M16', 0.5433814916048401),
             ('M2', 0.564503963614696),
             ('M10', 0.5647208121827412),
             ('M8', 0.5656272661348805),
             ('M4', 0.5723350253807106),
             ('M5', 0.580936266215454),
             ('M14', 0.6091370558375635),
             ('M20', 0.6140660324612152),
             ('M11', 0.6395939086294415),
             ('M3', 0.6625670775924584),
             ('M13', 0.7106598984771575),
             ('M1', 1.0800468566966028)]


RMS_ranking = [('M5', 0.4619697936387994),
               ('M14', 0.5999726465591385),
               ('M11', 0.7316617414192896),
               ('M13', 1),
               ('M8', 1)]

'''

def run_compare_1(B_, weight_, v_, przedz_):
    fuzzy_topsis_ranking = fuzzy_topsis(B_, weight_, v_)
    UTA_ranking = UTA_v2(B_, weight_, przedz_, v_)
    RMS_ranking = RSM_v2(B_)[1]
    list_of_ranks = [sort(fuzzy_topsis_ranking), sort(UTA_ranking), RMS_ranking]
    compare_rank_main_function(B_, list_of_ranks, False)


def run_compare_2(B_, weight_, v_, przedz_):
    fuzzy_topsis_ranking = fuzzy_topsis(B_, weight_, v_)
    UTA_ranking = UTA_v2(B_, weight_, przedz_, v_)
    RMS_ranking = RSM_v2(B_)[1]
    list_of_ranks = [sort(fuzzy_topsis_ranking), sort(UTA_ranking), RMS_ranking]
    compare_rank_main_function(B_, list_of_ranks, True)


#run_compare_1(B, weight, v, przedz)
