import bbase
from create_ladders import create_rand_ladder, listify_ladder

# Similarly to barcode test, we use function from create_ladders to create create ladders in canonical matrix form (0
# and 1 values). We then perform random basis changes and verify bbase.ladder_decomp gives the correct decomposition.
# Note that create_rand_ladder creates ladder modules as direct sums of the three type of indecomposables (Definition
# 4.2). These will most likely have nested barcodes (warnings will be raised), but the algorithm still functions due
# to their given direct sum decomposition.

l, p = 5, 17
F = bbase.Field(p)
it = 10
for k in range(it):
    A, mult = create_rand_ladder(l, listify=False)
    bbase.basis_change(A, [0] * l, F, Q='rectangle', keep=False)
    ans = bbase.ladder_decomp(listify_ladder(A, l), l, F)
    for indec in ans:
        if mult[indec]!=0:
            if mult[indec] != ans[indec]:
                raise TypeError('Multiplicties at', indec, 'do not match')
print('All multiplicties matched')


