import copy

def swap_row(A, i, j, B=None):
    A[[i, j], :] = A[[j, i], :]
    if B is not None:
        B[:, [i, j]] = B[:, [j, i]]


def swap_col(A, i, j, B=None):
    A[:, [i, j]] = A[:, [j, i]]
    if B is not None:
        B[:, [i, j]] = B[:, [j, i]]


def add_row(A, i, j, x, F, B=None):
    for k in range(len(A[0])):
        A[j, k] = F.add(F.mult(x, A[i, k]), A[j, k])
    if B is not None:
        for k in range(len(B)):
            B[k, i] = F.add(-F.mult(x, B[k, j]), B[k, i])


def add_col(A, i, j, x, F, B=None):
    for k in range(len(A)):
        A[k, j] = F.add(F.mult(x, A[k, i]), A[k, j])
    if B is not None:
        for k in range(len(B)):
            B[k, j] = F.add(F.mult(x, B[k, i]), B[k, j])


def mult_row(A, i, x, F, B=None):
    for j in range(len(A[0])):
        A[i, j] = F.mult(x, A[i, j])
    if B is not None:
        for j in range(len(B)):
            B[j, i] = F.div(B[j, i], x)


def mult_col(A, j, x, F, B=None):
    for i in range(len(A)):
        A[i, j] = F.mult(A[i, j], x)
    if B is not None:
        for i in range(len(B)):
            B[i, j] = F.mult(B[i, j], x)


def row_reduce(A, F, B=None, neigh=None, keep=False):
    M, N = A.shape;
    lastpiv, pivots = -1, []
    if keep:
        A = copy.deepcopy(A)

    for j in range(N):
        for i in range(lastpiv + 1, M):
            if A[i, j] != 0:
                x = A[i, j]
                mult_row(A, i, F.inv(x), F, B)
                swap_row(A, i, lastpiv + 1, B)

                if neigh:
                    if 0 in neigh:
                        for X in neigh[0]:
                            mult_col(X, i, x, F)
                            swap_col(X, i, lastpiv + 1)
                    if 1 in neigh:
                        for X in neigh[1]:
                            mult_row(X, i, F.inv(x), F)
                            swap_row(X, i, lastpiv + 1)

                pivots.append((lastpiv + 1, j))
                for k in range(M):
                    if k != lastpiv + 1:
                        x = F.div(A[k, j], A[lastpiv + 1, j])
                        add_row(A, lastpiv + 1, k, -x, F, B)
                        if neigh:
                            if 0 in neigh:
                                for X in neigh[0]:
                                    add_col(X, k, lastpiv + 1, x, F)
                            if 1 in neigh:
                                for X in neigh[1]:
                                    add_row(X, lastpiv + 1, k, -x, F)
                lastpiv = lastpiv + 1
                break
    if keep:
        return A, pivots
    else:
        return pivots


def col_reduce(A, F, B=None, neigh=None, keep=False):
    M, N = A.shape;
    lastpiv, pivots = N, []

    if keep:
        A = copy.deepcopy(A)

    for i in range(M - 1, -1, -1):
        for j in range(lastpiv - 1, -1, -1):
            if A[i, j] != 0:
                x = A[i, j]
                mult_col(A, j, F.inv(x), F, B)
                swap_col(A, j, lastpiv - 1, B)
                if neigh:
                    if 0 in neigh:
                        for X in neigh[0]:
                            mult_col(X, j, F.inv(x), F)
                            swap_col(X, j, lastpiv - 1)
                    if 1 in neigh:
                        for X in neigh[1]:
                            mult_row(X, j, x, F)
                            swap_row(X, lastpiv - 1, j)

                pivots.append((i, lastpiv - 1))
                for k in range(N):
                    if k != lastpiv - 1:
                        x = F.div(A[i, k], A[i, lastpiv - 1])
                        add_col(A, lastpiv - 1, k, -x, F, B)
                        if neigh:
                            if 0 in neigh:
                                for X in neigh[0]:
                                    add_col(X, lastpiv - 1, k, -x, F)
                            if 1 in neigh:
                                for X in neigh[1]:
                                    add_row(X, k, lastpiv - 1, x, F)
                lastpiv = lastpiv - 1
                break
    if keep:
        return A, pivots
    else:
        return pivots


def smf(A, F, keep=False):
    if keep:
        A, pivots = row_reduce(A, F, keep=True)
    else:
        pivots = row_reduce(A, F)
    for p in pivots:
        for j in range(p[1] + 1, A.shape[1]):
            add_col(A, p[1], j, -A[p[0], j], F)
    for k in range(len(pivots)):
        swap_col(A, pivots[k][1], k)

    if keep:
        return A


