from bbase.barcode_form import barcode_form
from bbase.barcode_extraction import extract_barcode, partial, lex_list
from bbase.elementary import *
import numpy as np
import copy


def is_nested(bar, l):
    for a in range(l - 1):
        for b in range(a + 2, l + 1):
            for c in range(a + 1, b - 1):
                for d in range(c, b - 1):
                    if bar[(a, b)][0] > 0 and bar[(c, d)][0] > 0:
                        return True
    return False


def create_mat(V, l, F, keep=False, bars=True, single=True):
    if keep:
        V = copy.deepcopy(V)

    t, V1, V2 = [0] * l, [V[(k, k + 1)] for k in range(l)], [(V[(k, k + 1)]) for k in range(l + 1, 2 * l + 1)]
    ladder = [V[(k, k + l + 1)] for k in range(l + 1)]

    barcode_form(V1, t, F, ladder=[ladder, 'top'])
    barcode_form(V2, t, F, ladder=[ladder, 'bot'])
    d1, d2 = extract_barcode(V1, t, True), extract_barcode(V2, t, True)

    if is_nested(d1, l):
        raise TypeError('Top barcode is nested')
    if is_nested(d2, l):
        raise TypeError('Bottom barcode is nested')

    order, col, row = lex_list(l), {}, {}
    M, N = 0, 0
    for b in order:
        if d1[b][0] > 0:
            col[b] = N
            N += d1[b][0]
        if d2[b][0] > 0:
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
                    X[row[c, d]:d2[c, d][0] + row[c, d], col[a, b]:d1[a, b][0] + col[a, b]] = ladder[a][
                        np.ix_(bot, top)]
                    M += d2[c, d][0]
                else:
                    X[a, b, c, d] = ladder[a][np.ix_(bot, top)]
        if single:
            N += d1[a, b][0]

    if bars:
        return X, {x: d1[x][0] for x in d1 if d1[x][0] > 0}, {x: d2[x][0] for x in reversed(list(d2.keys())) if
                                                              d2[x][0]}, indices
    else:
        return X


def reduce_mat(X, d1, d2, I, F):
    ans = {}
    for a, b in d1:
        ans[a, b, '+'] = d1[a, b]
    for c, d in d2:
        ans[c, d, '-'] = d2[c, d]

    for a, b in d1:
        for c, d in d2:
            if partial((c, d), (a, b)):
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


def ladder_decomp(V, l, F, keep=False):
    X, d1, d2, indices = create_mat(V, l, F, keep=keep)
    return reduce_mat(X, d1, d2, indices, F)


def extract_mult(V, d1, d2, I, l):
    ans = {}
    d1 = copy.deepcopy(d1)
    d2 = copy.deepcopy(d2)
    for a, b, c, d in I:
        row, col = I[a, b, c, d][0], I[a, b, c, d][1]
        ans[a, b, c, d] = np.linalg.matrix_rank(V[row[0]:row[1], col[0]:col[1]])
        d1[a, b] -= ans[a, b, c, d]
        d2[c, d] -= ans[a, b, c, d]
    for a, b in lex_list(l):
        if (a, b) in d1:
            ans[a, b, '+'] = d1[a, b]
        if (a, b) in d2:
            ans[a, b, '-'] = d2[a, b]
    return ans
