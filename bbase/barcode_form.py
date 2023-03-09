import numpy as np
import copy
from bbase.elementary import *
from bbase.basis_change import dim_vect


def initialise_basis(X, t):
    v = dim_vect(X, t)
    return [np.identity(n) for n in v]


def barcode_form(V, t, F, basis=False, ladder=None):
    if basis:
        B = initialise_basis(V, t)
        V = copy.deepcopy(V)
    else:
        B = [None for k in range(len(V) + 1)]
    for l in range(len(V)):
        local_reduce(V, t, F, l, B=B, ladder=ladder)
    if basis:
        return V, B


def bform(V, t, F, basis=True):
    if basis:
        return barcode_form(V, t, F, basis)
    else:
        barcode_form(V, t, F, basis)


def local_reduce(V, t, F, l, B=None, ladder=None):
    if t[l] == 0:
        if l == len(V) - 1:
            if ladder:
                if ladder[1] == 'top':
                    piv = row_reduce(V[l], F, B[l + 1], {0: [ladder[0][l + 1]]})
                elif ladder[1] == 'bot':
                    piv = row_reduce(V[l], F, B[l + 1], {1: [ladder[0][l + 1]]})
            else:
                piv = row_reduce(V[l], F, B[l + 1])
        else:
            if ladder is not None:
                if ladder[1] == 'top':
                    piv = row_reduce(V[l], F, B[l + 1], {0: [V[l + 1], ladder[0][l + 1]]})
                elif ladder[1] == 'bot':
                    piv = row_reduce(V[l], F, B[l + 1], {0: [V[l + 1]], 1: [ladder[0][l + 1]]})
            else:
                piv = row_reduce(V[l], F, B[l + 1], {t[l + 1]: [V[l + 1]]})
        for r, q in piv:
            for p in range(q + 1, V[l].shape[1]):
                if V[l][r, p] != 0:
                    zero_out(V, F, r, q, p, t, l, 'col', B=B, ladder=ladder)
    if t[l] == 1:
        if l == len(V) - 1:
            piv = col_reduce(V[l], F, B[l + 1])
        else:
            piv = col_reduce(V[l], F, B[l + 1], {t[l + 1]: [V[l + 1]]})

        for r, q in piv:
            for p in range(r):
                if V[l][p, q] != 0:
                    zero_out(V, F, r, q, p, t, l, 'row', B)


def zero_out(V, F, r, q, p, t, k, op_type, B, ladder=None):
    if op_type == 'col':
        x = V[k][r, p]
        add_col(V[k], q, p, -x, F, B[k])
        if ladder:
            if ladder[1] == 'top':
                add_col(ladder[0][k], q, p, -x, F)
            elif ladder[1] == 'bot':
                add_row(ladder[0][k], p, q, x, F)

        if k == 0:
            return

        elif t[k - 1] == 0:
            add_row(V[k - 1], p, q, x, F)
            if (V[k - 1][p, :] == np.zeros(V[k - 1].shape[1])).all():
                return V, B
            for i in range(V[k - 1].shape[1]):
                if V[k - 1][q, i] != 0:
                    c = i
                    break
            for i in range(c + 1, V[k - 1].shape[1]):
                if V[k - 1][p, i] != 0:
                    d = i
                    break
            zero_out(V, F, q, c, d, t, k - 1, 'col', B, ladder)

        elif t[k - 1] == 1:
            add_col(V[k - 1], q, p, -x, F)
            if (V[k - 1][:, q] == np.zeros((V[k - 1].shape[0], 1))).all():
                return V, B
            for i in range(V[k - 1].shape[0]):
                if V[k - 1][i, p] != 0:
                    d = i
                    break
            for i in range(d + 1, V[k - 1].shape[0]):
                if V[k - 1][i, p] != 0:
                    c = i
                    break
            zero_out(V, F, c, p, d, t, k - 1, 'row', B)

    if op_type == 'row':
        x = V[k][p, q]
        add_row(V[k], r, p, -x, F, B[k])

        if k == 0:
            return
        elif t[k - 1] == 0:
            add_row(V[k - 1], r, p, -x, F)
            if (V[k - 1][r, :] == np.zeros(V[k - 1].shape[1])).all():
                return V, B
            for i in range(V[k - 1].shape[1]):
                if V[k - 1][p, i] != 0:
                    c = i
                    break
            for i in range(c + 1, V[k - 1].shape[1]):
                if V[k - 1][p, i] != 0:
                    d = i
                    break
            zero_out(V, F, p, c, d, t, k - 1, 'col', B)

        elif t[k - 1] == 1:
            add_col(V[k - 1], p, r, x, F)
            if (V[k - 1][:, p] == np.zeros((V[k - 1].shape[0], 1))).all():
                return V, B
            for i in range(V[k - 1].shape[0]):
                if V[k - 1][i, r] != 0:
                    d = i
                    break
            for i in range(d + 1, V[k - 1].shape[0]):
                if V[k - 1][i, r] != 0:
                    c = i
                    break
            zero_out(V, F, c, r, d, t, k - 1, 'row', B)
