from bbase.barcode_form import barcode_form
from bbase.barcode_extraction import extract_barcode
from bbase.elementary import *
import numpy as np
import copy
import warnings


def lex_list(l):
    ans = []
    for a in range(l + 1):
        for b in range(a, l + 1):
            ans.append((a, b))
    return ans


def lex(b1, b2):
    if b1 == b2:
        return False
    if b1[0] < b2[0]:
        return True
    if b1[0] == b2[0]:
        if b1[1] < b2[1]:
            return True
    return False


def partial(b1, b2):
    if b1[0] <= b2[0] <= b1[1] <= b2[1]:
        return True
    return False


def smaller_lex(i, j):
    ans = []
    for a in reversed(range(i + 1)):
        for b in reversed(range(i, j + 1)):
            ans.append((a, b))
    return ans


# Simply checks whether a barcode is nested or not.
def is_nested(bar, l):
    for a in range(l - 1):
        for b in range(a + 2, l + 1):
            for c in range(a + 1, b):
                for d in range(c, b):
                    if (a, b) in bar and (c, d) in bar:
                        # print((c, d), 'is nested in ', (a, b)) can be used to see which bars are nested
                        return True
    return False


# Given a ladder A, we create a single matrix X representing all vertical linear
# maps as in Step 1 of the proof of Theorem 4.3.

def create_mat(A, l, F, keep=False, bars=True, single=True):
    if keep:
        A = copy.deepcopy(A)

    t = [0] * l

    barcode_form(A[0], t, F, ladder=[A[0, 1], 'top'])
    barcode_form(A[1], t, F, ladder=[A[0, 1], 'bot'])
    d1, d2 = extract_barcode(A[0], t, True), extract_barcode(A[1], t, True)

    if is_nested(d1, l):
        warnings.warn('Top barcode is nested, results may be incorrect')
    if is_nested(d2, l):
        warnings.warn('Bottom barcode is nested, results may be incorrect')

    order, col, row = lex_list(l), {}, {}
    M, N = 0, 0
    for b in order:
        if b in d1:
            col[b] = N
            N += d1[b][0]
        if b in d2:
            row[b] = M
            M += d2[b][0]

    if not single:
        X = {}
    else:
        X = np.zeros((sum([d2[x][0] for x in row]), sum([d1[x][0] for x in col])))
    if bars:
        indices = {}
    for a, b in col:
        top = [x[0] for x in d1[a, b][1]]
        for c, d in row:
            if partial((c, d), (a, b)):
                bot = [x[a - c] for x in d2[c, d][1]]
                if single:
                    if bars:
                        indices[a, b, c, d] = [[row[c, d], d2[c, d][0] + row[c, d]],
                                               [col[a, b], d1[a, b][0] + col[a, b]]]
                    X[row[c, d]:d2[c, d][0] + row[c, d], col[a, b]:d1[a, b][0] + col[a, b]] = A[0, 1][a][
                        np.ix_(bot, top)]
                    M += d2[c, d][0]
                else:
                    X[a, b, c, d] = A[0, 1][a][np.ix_(bot, top)]
        if single:
            N += d1[a, b][0]

    if bars:
        return X, {x: d1[x][0] for x in d1}, {x: d2[x][0] for x in d2}, indices
    else:
        return X


# This reduces the single matrix X outputed from the above function, as in
# Step 3 of the proof of Theorem 4.3
def reduce_mat(X, l, d1, d2, I, F):
    ans = {}
    for a, b in d1:
        ans[a, b, '+'] = d1[a, b]
    for c, d in d2:
        ans[c, d, '-'] = d2[c, d]

    for (a, b) in lex_list(l):
        for (c, d) in smaller_lex(a, b):
            if (a, b) in d1 and (c, d) in d2 and partial((c, d), (a, b)):
                n = local_snf(X, I[a, b, c, d][0], I[a, b, c, d][1], F)
                ans[a, b, c, d] = n
                ans[a, b, '+'] -= n
                ans[c, d, '-'] -= n
    return ans


def local_snf(X, rows, cols, F):
    ans = 0
    for j in range(cols[0], cols[1]):
        for i in range(rows[0], rows[1]):
            if X[i, j] != 0:
                ans += 1
                x = F.inv(X[i, j])
                mult_row(X, i, x, F)
                for k in range(cols[0], X.shape[1]):
                    if k != j:
                        add_col(X, j, k, -X[i, k], F)
                for k in range(0, rows[1]):
                    if k != i:
                        add_row(X, i, k, -X[k, j], F)
    return ans


# This is the main function of interest, which takes as input a well-behaved ladder A and outputs
# the multiplicities of its indecomposables as a dictionary.
def ladder_decomp(A, l, F, keep=False):
    X, d1, d2, indices = create_mat(A, l, F, keep=keep)
    return reduce_mat(X, l, d1, d2, indices, F)


def extract_mult(A, d1, d2, I, l):
    ans = {}
    d1 = copy.deepcopy(d1)
    d2 = copy.deepcopy(d2)
    for a, b, c, d in I:
        row, col = I[a, b, c, d][0], I[a, b, c, d][1]
        ans[a, b, c, d] = np.linalg.matrix_rank(A[row[0]:row[1], col[0]:col[1]])
        d1[a, b] -= ans[a, b, c, d]
        d2[c, d] -= ans[a, b, c, d]
    for a, b in lex_list(l):
        if (a, b) in d1:
            ans[a, b, '+'] = d1[a, b]
        if (a, b) in d2:
            ans[a, b, '-'] = d2[a, b]
    return ans
