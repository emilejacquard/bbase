from test.create_ints import *
from bbase.reduce_ladders import lex_list, partial
import numpy as np
import random


def create_ladder(a, b, c, d, l):
    t = [0] * l
    ans = {**create_int(a, b, l, t), **create_int(c, d, l, t, True)}
    if c > 0:
        for k in range(c):
            ans[(k, k + l + 1)] = np.empty((0, 0))
    for k in range(c, a):
        ans[(k, k + l + 1)] = np.empty((1, 0))
    for k in range(a, d + 1):
        ans[(k, k + l + 1)] = np.array([[1]])
    for k in range(d + 1, b + 1):
        ans[(k, k + l + 1)] = np.empty((0, 1))
    if b < l:
        for k in range(b + 1, l + 1):
            ans[(k, k + l + 1)] = np.empty((0, 0))
    return ans


def create_ladder_int(a, b, l, shift=False):
    t = [0] * l
    ans = create_int(a, b, l, t, shift)
    for k in range(l):
        if shift:
            ans[k, k + 1] = np.empty((0, 0))
        else:
            ans[k + l + 1, k + l + 2] = np.empty((0, 0))
    if a > 0:
        for k in range(a):
            ans[k, k + l + 1] = np.empty((0, 0))
    for k in range(a, b + 1):
        if shift:
            ans[k, k + l + 1] = np.empty((1, 0))
        else:
            ans[k, k + l + 1] = np.empty((0, 1))

    if b < l:
        for k in range(b + 1, l + 1):
            ans[k, k + l + 1] = np.empty((0, 0))
    return ans


def create_rand_ladder(l, given=None, listify=True):
    L = []
    if given is None:
        mult = {}
    for a, b in lex_list(l):
        if given is None:
            n, m = random.randint(0, 1), random.randint(0, 1)
            mult[(a, b, '+')] = n
            mult[(a, b, '-')] = m
        else:
            if (a, b, '+') in given:
                n = given[(a, b, '+')]
            else:
                n = 0
            if (a, b, '-') in given:
                m = given[(a, b, '-')]
            else:
                m = 0

        for k in range(n):
            L.append(create_ladder_int(a, b, l))
        for k in range(m):
            L.append(create_ladder_int(a, b, l, True))

        for c, d in lex_list(l):
            if partial((c, d), (a, b)):
                if given is None:
                    n = random.randint(0, 1)
                    mult[(a, b, c, d)] = n
                else:
                    if (a,b,c,d) in given:
                        n = given[(a, b, c, d)]
                    else :
                        n=0
                for k in range(n):
                    L.append(create_ladder(a, b, c, d, l))
    if listify:
        if given is None:
            return listify_ladder(direct_sums(L), l), mult
        else:
            return listify_ladder(direct_sums(L), l), given

    if given is None:
        return direct_sums(L), mult
    else:
        return direct_sums(L), given


def listify_ladder(X, l):
    ans = {0: [X[(k, k + 1)] for k in range(l)], 1: [(X[(k, k + 1)]) for k in range(l + 1, 2 * l + 1)],
           (0, 1): [X[(k, k + l + 1)] for k in range(l + 1)]}
    return ans
