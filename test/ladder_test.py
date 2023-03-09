import bbase
import timeit
from create_ladders import create_rand_ladder
p, l = 17, 2
t = [0] * l
F = bbase.Field(p)
go = True
start = timeit.default_timer()
if go:
    for k in range(100):
        V, mult = create_rand_ladder(l)
        bbase.basis_change(V, t, F, Q='rectangle')
        test = bbase.ladder_decomp(V, l, F)
        for x in mult:
            if x in test:
                if test[x] != mult[x]:
                    print('woops')
                    break
            else:
                if mult[x] > 0:
                    print('woopsies')
                    break

stop = timeit.default_timer()
print(stop)

