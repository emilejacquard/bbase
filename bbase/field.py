import copy
import numpy as np
from bbase.elementary import *


class Field:
    def __init__(self, char):
        self.p = char

    def add(self, a, b):
        if self.p == 0:
            return a + b
        else:
            return (a + b) % self.p

    def mult(self, a, b):
        if self.p == 0:
            return a * b
        else:
            return (a * b) % self.p

    def inv(self, a):
        if self.p == 0:
            return 1 / a
        else:
            return pow(int(a), -1, self.p)

    def div(self, a, b):
        if self.p == 0:
            return a / b
        else:
            return (self.mult(a, self.inv(b)))

    def inv_mat(self, A):
        A = copy.deepcopy(A)
        if self.p == 0:
            return np.linalg.inv(A)
        else:
            n = A.shape[0]
            ans = np.identity(n)
            for j in range(n):
                found = False
                for i in range(j, n):
                    if A[i, j] != 0:
                        found = True
                        x = self.inv(A[i, j])
                        mult_row(A, i, x, self)
                        mult_row(ans, i, x, self)
                        swap_row(A, i, j)
                        swap_row(ans, i, j)
                        for k in range(n):
                            if k != j:
                                x = A[k, j]
                                add_row(A, j, k, -x, self)
                                add_row(ans, j, k, -x, self)
                        break
                if not found:
                    return np.zeros((n, n))
            return ans

    def matmul(self, A, B):
        ans = np.matmul(A, B)
        if self.p != 0:
            for i in range(ans.shape[0]):
                for j in range(ans.shape[1]):
                    ans[i, j] = ans[i, j] % self.p
        return ans
