import numpy as np
import copy
from bbase.elementary import *
from bbase.basis_change import dim_vect


# This is an implementation of the algorithm from Section 3 (and more generally Section 5 for zigzag modules).


def initialise_basis(A, t):
    v = dim_vect(A, t)
    return [np.identity(n) for n in v]


def bform(A, t, F, basis=True):
    if basis:
        return barcode_form(A, t, F, basis)
    else:
        barcode_form(A, t, F, basis)


# This is the main function of interest. It takes as input a matrix sequence A, the orientation t of the
# underlying quiver and the field F of computation. If basis is set to False (by default True),
# then it simply puts the underlying matrix sequence A in barcode form. Else, it outputs
# the matrix sequence X in barcode form together with the adequate change of basis B.
# ladder is a parameter used for decomposing ladder and can be safely ignored.
def barcode_form(A, t, F, basis=False, ladder=None):
    if basis:
        B = initialise_basis(A, t)
        A = copy.deepcopy(A)
    else:
        B = [None for k in range(len(A) + 1)]
    for l in range(len(A)):
        local_reduce(A, t, F, l, B=B, ladder=ladder)
    if basis:
        return A, B


# This implements the iterative process exhbited in Proposition 5.4.
def local_reduce(A, t, F, l, B=None, ladder=None):
    if t[l] == 0:
        if l == len(A) - 1:
            if ladder:
                if ladder[1] == 'top':
                    piv = row_reduce(A[l], F, B[l + 1], {0: [ladder[0][l + 1]]})
                elif ladder[1] == 'bot':
                    piv = row_reduce(A[l], F, B[l + 1], {1: [ladder[0][l + 1]]})
            else:
                piv = row_reduce(A[l], F, B[l + 1])
        else:
            if ladder is not None:
                if ladder[1] == 'top':
                    piv = row_reduce(A[l], F, B[l + 1], {0: [A[l + 1], ladder[0][l + 1]]})
                elif ladder[1] == 'bot':
                    piv = row_reduce(A[l], F, B[l + 1], {0: [A[l + 1]], 1: [ladder[0][l + 1]]})
            else:
                piv = row_reduce(A[l], F, B[l + 1], {t[l + 1]: [A[l + 1]]})
        for r, q in piv:
            for p in range(q + 1, A[l].shape[1]):
                if A[l][r, p] != 0:
                    zero_out(A, F, r, q, p, t, l, 'col', B=B, ladder=ladder)
    if t[l] == 1:
        if l == len(A) - 1:
            piv = col_reduce(A[l], F, B[l + 1])
        else:
            piv = col_reduce(A[l], F, B[l + 1], {t[l + 1]: [A[l + 1]]})

        for r, q in piv:
            for p in range(r):
                if A[l][p, q] != 0:
                    zero_out(A, F, r, q, p, t, l, 'row', B)


# This is a direct implementation of Lemma 5.3 for zeroing term in the last matrix of our matrix sequence A,
# where all previous matrices are in barcode form.
def zero_out(A, F, r, q, p, t, k, op_type, B, ladder=None):
    if op_type == 'col':
        x = A[k][r, p]
        add_col(A[k], q, p, -x, F, B[k])
        if ladder:
            if ladder[1] == 'top':
                add_col(ladder[0][k], q, p, -x, F)
            elif ladder[1] == 'bot':
                add_row(ladder[0][k], p, q, x, F)

        if k == 0:
            return

        elif t[k - 1] == 0:
            add_row(A[k - 1], p, q, x, F)
            if (A[k - 1][p, :] == np.zeros(A[k - 1].shape[1])).all():
                return A, B
            for i in range(A[k - 1].shape[1]):
                if A[k - 1][q, i] != 0:
                    c = i
                    break
            for i in range(c + 1, A[k - 1].shape[1]):
                if A[k - 1][p, i] != 0:
                    d = i
                    break
            zero_out(A, F, q, c, d, t, k - 1, 'col', B, ladder)

        elif t[k - 1] == 1:
            add_col(A[k - 1], q, p, -x, F)
            if (A[k - 1][:, q] == np.zeros((A[k - 1].shape[0], 1))).all():
                return A, B
            for i in range(A[k - 1].shape[0]):
                if A[k - 1][i, p] != 0:
                    d = i
                    break
            for i in range(d + 1, A[k - 1].shape[0]):
                if A[k - 1][i, p] != 0:
                    c = i
                    break
            zero_out(A, F, c, p, d, t, k - 1, 'row', B)

    if op_type == 'row':
        x = A[k][p, q]
        add_row(A[k], r, p, -x, F, B[k])

        if k == 0:
            return
        elif t[k - 1] == 0:
            add_row(A[k - 1], r, p, -x, F)
            if (A[k - 1][r, :] == np.zeros(A[k - 1].shape[1])).all():
                return A, B
            for i in range(A[k - 1].shape[1]):
                if A[k - 1][p, i] != 0:
                    c = i
                    break
            for i in range(c + 1, A[k - 1].shape[1]):
                if A[k - 1][p, i] != 0:
                    d = i
                    break
            zero_out(A, F, p, c, d, t, k - 1, 'col', B)

        elif t[k - 1] == 1:
            add_col(A[k - 1], p, r, x, F)
            if (A[k - 1][:, p] == np.zeros((A[k - 1].shape[0], 1))).all():
                return A, B
            for i in range(A[k - 1].shape[0]):
                if A[k - 1][i, r] != 0:
                    d = i
                    break
            for i in range(d + 1, A[k - 1].shape[0]):
                if A[k - 1][i, r] != 0:
                    c = i
                    break
            zero_out(A, F, c, r, d, t, k - 1, 'row', B)
