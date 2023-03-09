import numpy as np
import random


def direct_sum(I, J):
    Z = {}
    for k in I:
        Z[k] = np.concatenate((np.concatenate((I[k], np.zeros((I[k].shape[0], J[k].shape[1]))), axis=1),
                               np.concatenate((np.zeros((J[k].shape[0], I[k].shape[1])), J[k]), axis=1))).astype('int')
    return Z


def direct_sums(L):
    V = L[0]
    for k in range(1, len(L)):
        V = direct_sum(V, L[k])
    return V


def listify(X):
    return [X[(k, k + 1)] for k in range(len(X))]


def rank(V):
    r, l = {}, len(V)
    for a in range(l + 1):
        for b in range(a + 1, l + 1):
            X = V[a]
            for k in range(a + 1, b):
                X = np.matmul(V[k], X)
            r[a, b] = np.linalg.matrix_rank(X)
    return r


def bar_to_rank(bar,l):
    r = {(i, j): 0 for i in range(l + 1) for j in range(i + 1, l + 1)}
    for a in range(l + 1):
        for b in range(a + 1, l + 1):
            for x, y in bar:
                if x <= a and y >= b:
                    r[a, b] += bar[x, y]
    return r


def create_int(a, b, l, t, shift=False):
    X = {}
    if shift:
        s = l + 1
    else:
        s = 0
    if a > 0:
        for k in range(a - 1):
            X[k + s, k + s + 1] = np.empty((0, 0))
        if t[a - 1] == 0:
            X[a - 1 + s, a + s] = np.empty((1, 0))
        if t[a - 1] == 1:
            X[a - 1 + s, a + s] = np.empty((0, 1))

    for k in range(a, b):
        X[k + s, k + s + 1] = np.array([[1]])
    if b < l:
        if t[b] == 0:
            X[b + s, b + s + 1] = np.empty((0, 1))
        if t[b] == 1:
            X[b + s, b + s + 1] = np.empty((1, 0))
        for k in range(b + 1, l):
            X[k + s, k + s + 1] = np.empty((0, 0))
    return X


def create_rand_int(l, standard=False):
    L = []
    if standard:
        t = [0] * l
    else:
        t = []
        for k in range(l):
            t.append(random.randint(0, 1))
    mult = {}
    for a in range(l + 1):
        for b in range(a, l + 1):
            n = random.randint(0, 2)
            mult[(a, b)] = n
            for k in range(n):
                L.append(create_int(a, b, l, t))
    return listify(direct_sums(L)), t, mult
