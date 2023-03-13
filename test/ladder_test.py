import bbase
from create_ladders import create_rand_ladder, listify_ladder

# Similarly to barcode test, we use function from create_ladders to create create ladders in canonical matrix form (0
# and 1 values). We then perform random basis changes and verify bbase.ladder_decomp gives the correct decomposition.
# Note that we consider the case l=2 to ensure all ladders are well-behaved.

l, p = 2, 17
F = bbase.Field(p)
it = 10
for k in range(it):
    A, mult = create_rand_ladder(l, listify=False)
    bbase.basis_change(A, [0] * l, F, Q='rectangle', keep=False)
    ans = bbase.ladder_decomp(listify_ladder(A, l), l, F)
    for indec in ans:
        if mult[indec] != ans[indec]:
            raise TypeError('Multiplicties at', indec, 'do not match')
print('All multiplicties matched')
