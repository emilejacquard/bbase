import bbase
from create_ints import create_rand_int

# Functions in the create_ints.py allow us to create persistence modules with known multiplicties of bars (for each
# bar we randomly assign a multiplicity 0,1 or 2). The given matrix sequence is in barcode form. We then perform a
# random change of basis and verify the output of bbase.barcode is correct.

l, p = 10, 17
F = bbase.Field(p)
it = 10
for k in range(it):
    A, t, mult = create_rand_int(l)
    bbase.basis_change(A, t, F, keep=False)
    bbase.bform(A, t, F, basis=False)
    ans = bbase.barcode(A, t)
    for (i, j) in mult:
        if mult[(i, j)] != ans[(i, j)]:
            raise TypeError('Multiplicties at', (i, j), 'do not match')
print('All multiplicties matched')
