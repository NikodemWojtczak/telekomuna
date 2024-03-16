# import numpy as np
# def dwieLiczbyLosowe() :
#     while True:
#         liczba1 = np.random.randint(0, 16)
#         liczba2 = np.random.randint(0, 16)
#         if liczba1 != liczba2:
#             break
#     return liczba1, liczba2
#
# def indeksy(dekodowanie, H):
#     for j in range(H.shape[1]):
#         for i in range(H.shape[1]):  # Iterate through columns
#             kolumna = ((H[:, j] + H[:, i]) % 2)
#             if np.array_equal(dekodowanie, kolumna):
#                 return j, i
#
# N = 8
# M = 8
# wiadomosc = np.array([1, 0, 1, 1, 1, 0, 1, 0])
#
# matrix = np.ones((M, M))
# np.fill_diagonal(matrix, 0)
# matrix = np.fliplr(matrix)
# jednostkowa = np.eye(N)
# H = np.hstack((matrix, jednostkowa))
#
# szyfr = np.dot(wiadomosc, H)
# szyfr = szyfr % 2
#
# miejsce_bledu_1, miejsce_bledu_2 = dwieLiczbyLosowe()
# tmp = szyfr.copy()
# tmp[miejsce_bledu_1] = tmp[miejsce_bledu_1]+1
# tmp[miejsce_bledu_2] = tmp[miejsce_bledu_2]+1
# blednySzyfr = tmp % 2
#
# dekodowanie = np.dot(H, blednySzyfr)
# dekodowanie = dekodowanie % 2
#
# index_1, index_2 = indeksy(dekodowanie, H)
#
# print("Macierz uzywana do szyfrow: ")
# print(H)
# print("Twoja wiadomosc:")
# print(wiadomosc)
# print("Zaszyfrowana wiadomość")
# print(szyfr)
# print(f"Bledny szyfr z bledem na pozycji: {miejsce_bledu_1}, oraz na miejscu: {miejsce_bledu_2}")
# print(blednySzyfr)
# print("Zdekodowana wiadomość z dwoma bledami")
# print(dekodowanie)
# print(f"Jest to równe sumie kolumn z indeksami: {index_2} oraz {index_1}")
# print(f"Kolumna: {index_1}")
# print(H[:,index_1])
# print(f"Kolumna: {index_2}")
# print(H[:,index_2])
#
