# import numpy as np
#
# N = 8
# M = 8
# matrix = np.ones((M, M))
# np.fill_diagonal(matrix, 0)
# matrix = np.fliplr(matrix)
# jednostkowa = np.eye(N)
# H = np.hstack((matrix, jednostkowa))
#
# wiadomosc = np.array([1, 0, 1, 1, 1, 0, 1, 0])
#
# szyfr = np.dot(wiadomosc, H)
# szyfr = szyfr % 2
#
# miejsce_bledu = np.random.randint(0, 16)
# tmp = szyfr.copy()
# tmp[miejsce_bledu] = tmp[miejsce_bledu]+1
# blednySzyfr = tmp % 2
#
# dokodowanie = np.dot(H, blednySzyfr)
# dokodowanie = dokodowanie % 2
# pierwotna = np.dot(H, szyfr)
# pierwotna = pierwotna % 2
#
# index_of_matching_column = None
# for i in range(H.shape[1]):  # Iterate through columns
#     if np.array_equal(H[:, i], dokodowanie):
#         index_of_matching_column = i
#         break
#
# print("Macierz uzywana do szyfrow: ")
# print(H)
# print("Twoja wiadomosc:")
# print(wiadomosc)
# print("Zaszyfrowana wiadomość")
# print(szyfr)
# print("Cos")
# print(pierwotna)
# print(f"Bledny szyft z bledem na pozycji: {miejsce_bledu}")
# print(blednySzyfr)
# print("Zdekodowana wiadomość z jednym błedem")
# print(dokodowanie)
# print(f"Jest to równe kolumne z indeksem: {index_of_matching_column}")


