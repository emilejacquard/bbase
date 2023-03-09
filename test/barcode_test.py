import bbase
from create_ints import create_rand_int
import timeit
import numpy as np

A, t = [np.array([[6,2,5],[1,2,3]]), np.array([[0,0,3,2],[1,2,6,4]]), np.array([[1,5,3,6],[1,2,0,4]])], [0,1,0]
F=bbase.Field(7)
X,B=bbase.bform(A,t,F)
Y=bbase.basis_change(X,t,F,B)
for k in range(3):
    if (A[k]==Y[k]).all():
        print('Correct change of basis !')

barcode=bbase.barcode(X,t)

print(ans)
