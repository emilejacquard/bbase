err = 10 ** -10


# The main function is bbase.barcode, which outputs the barcode of a given matrix sequence in barcode form (the
# orientation t of the quiver should also be given). If the parameter list is set to True (by default False) the
# output is given as a list of bars (with repeated bars if multiplicities are >1). Otherwise, the output is a
# dictionary with keys potential bars (i,j) and values the associated multiplicities.


def list_to_persim(l):
    persim = {}
    for i in range(len(l)):
        persim[(i, i + 1)] = l[i]
    return persim


def barcode(V, t, list=False):
    ans = extract_barcode(V, t)
    if list:
        barcode = []
    else:
        return ans
    for i, j in ans:
        for k in range(ans[(i, j)]):
            barcode.append([i, j])
    return barcode


def extract_barcode(V, t, vectors=False):
    l = len(V)
    if vectors:
        d = {(i, j): [0, []] for i in range(l + 1) for j in range(i, l + 1)}
    else:
        d = {(i, j): 0 for i in range(l + 1) for j in range(i, l + 1)}
    seq = []
    for i in range(l):
        seq, d = extend_sequence(V[i], t[i], seq, d, i, vectors)

    if t[-1] == 0:
        seen = {i: False for i in range(V[-1].shape[0])}
        for s in seq:
            if s[-1] != -1:
                seen[s[-1]] = True
                if vectors:
                    d[l - len(s) + 1, l][0] += 1
                    d[l - len(s) + 1, l][1].append(s[:])
                else:
                    d[l - len(s) + 1, l] += 1
        for i in range(V[-1].shape[0]):
            if not seen[i]:
                if vectors:
                    d[l, l][0] += 1
                    d[l, l][1].append([i])
                else:
                    d[l, l] += 1
    if t[-1] == 1:
        seen = {j: False for j in range(V[-1].shape[1])}
        for s in seq:
            if s[-1] != -1:
                seen[s[-1]] = True
                if vectors:
                    d[l - len(s) + 1, l][0] += 1
                    d[l - len(s) + 1, l][1].append(s[:])
                else:
                    d[l - len(s) + 1, l] += 1

        for j in range(V[-1].shape[1]):
            if not seen[j]:
                if vectors:
                    d[l, l][0] += 1
                    d[l, l][1].append([j])
                else:
                    d[l, l] += 1

    return d


def extend_sequence(A, a, seq, d, k, vectors=False):
    if a == 0:
        seen = {j: False for j in range(A.shape[1])}
        if seq:
            for s in seq:
                if s[-1] == -1:
                    continue
                else:
                    seen[s[-1]] = True
                stops = True
                for i in range(A.shape[0]):
                    if -err < A[i][s[-1]] - 1 < err:
                        s.append(i)
                        stops = False
                        break
                if stops:
                    if vectors:
                        d[k - len(s) + 1, k][0] += 1
                        d[k - len(s) + 1, k][1].append(s[:])
                    else:
                        d[k - len(s) + 1, k] += 1
                    s.append(-1)

        for j in seen:
            if not seen[j]:
                stops = True
                for i in range(A.shape[0]):
                    if -err < A[i][j] - 1 < err:
                        seq.append([j, i])
                        stops = False
                        break
                if stops:
                    if vectors:
                        d[k, k][0] += 1
                        d[k, k][1].append([j])
                    else:
                        d[k, k] += 1
                    seq.append([j, -1])

    if a == 1:
        seen = {i: False for i in range(A.shape[0])}
        if seq:
            for s in seq:
                if s[-1] == -1:
                    continue
                else:
                    seen[s[-1]] = True
                stops = True
                for j in range(A.shape[1]):
                    if -err < A[s[-1]][j] - 1 < err:
                        s.append(j)
                        stops = False
                        break
                if stops:
                    if vectors:
                        d[k - len(s) + 1, k][0] += 1
                        d[k - len(s) + 1, k][1].append(s[:])
                    else:
                        d[k - len(s) + 1, k] += 1
                    s.append(-1)

        for i in seen:
            if not seen[i]:
                stops = True
                for j in range(A.shape[1]):
                    if -err < A[i][j] - 1 < err:
                        seq.append([i, j])
                        stops = False
                        break
                if stops:
                    if vectors:
                        d[k, k][0] += 1
                        d[k, k][1].append([i])
                    else:
                        d[k, k] += 1
                    seq.append([i, -1])

    return seq, d


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


def reorder(V, bar, ladder=None, indices=False):
    l = len(V)
    new_col = {k: [] for k in range(l + 1)}
    if indices:
        ans = {}
    order = lex_list(l)
    for i, j in order:
        for k in range(i, j + 1):
            for b in bar[i, j][1]:
                new_col[k].append(b[k - i])
    for k in range(l):
        V[k] = V[k][:, new_col[k]]
        V[k] = V[k][new_col[k + 1], :]
    if ladder is not None:
        if ladder[1] == 'top':
            for k in range(l + 1):
                ladder[0][k] = ladder[0][k][:, new_col[k]]
        if ladder[1] == 'bot':
            for k in range(l + 1):
                ladder[0][k] = ladder[0][k][new_col[k], :]
