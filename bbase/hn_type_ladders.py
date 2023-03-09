from bbase.reduce_ladders import local_snf
from bbase.barcode_form import barcode_form
from bbase.barcode_extraction import extract_barcode, reorder


def sky(V, l, F):
    t, V1, V2 = [0] * l, [V[(k, k + 1)] for k in range(l)], [(V[(k, k + 1)]) for k in range(l + 1, 2 * l + 1)]
    ladder = [V[(k, k + l + 1)] for k in range(l + 1)]
    barcode_form(V1, t, F, ladder=[ladder, 'top'])
    barcode_form(V2, t, F, ladder=[ladder, 'bot'])
    d1, d2 = extract_barcode(V1, t, True), extract_barcode(V2, t, True)
    reorder(V1, d1, ladder=[ladder, 'top'])
    reorder(V2, d2, ladder=[ladder, 'bot'])
    sky = {}
    for x in range(l):
        sky[x, '+'] = hn_type(ladder, l, F, d1, d2, x, 0)
        sky[x, '-'] = hn_type(V, l, F, x, 1)

    return sky


def hn_type(ladder, l, F, d1, d2, x, row):
    d1_loc, d2_loc = update_barcode(d1, x, l), update_barcode(d2, x, l)
    if row == 1:
        return d2_loc
    if row == 0:
        M, N = 0, 0
        for c in range(x, l+1):
            for r in reversed(range(x, c+1)):
                local_snf(ladder[x],[M,M+d2[x,r]],[N,N+d2[x,r]],F)


                return


def update_barcode(b, x, l, vectors=False):
    ans = {}
    for k in range(x, l + 1):
        if vectors:
            ans[x, k] = [0, []]
        else:
            ans[x, k] = 0
        for a in range(x + 1):
            if (a, k) in b:
                if vectors:
                    for s in range(b[a, k][0]):
                        ans[x, k][0] += 1
                        ans[x, k][1].append(b[a, k][1][s][x - a:])
                else:
                    for s in range(b[a, k]):
                        ans[x, k] += 1
    return ans
