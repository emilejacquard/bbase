import bbase
from create_ladders import create_rand_ladder, listify_ladder
v=[3,2,2]
w=[2,4,3]
l=2
F=bbase.Field(11)
mult={(0,2,0,1):1, (0,1,0,1):1, (0,1,0,0):1, (1,2,'+'):1, (0,2,'-'):1}
V, mult=create_rand_ladder(l,mult,listify=False)
print(V)
Z=listify_ladder(bbase.basis_change(V,[0]*l,F,Q='rectangle',keep=True),l)
print(Z)

ans=bbase.ladder_decomp(Z,l,F)
print(ans)