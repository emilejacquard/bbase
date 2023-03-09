# bbase

# barcode-bases-and-ladders

# Overview

This is a simple package which implements two algorithms from the paper [The Space of Barcode Bases for Persistence Modules](https://link.springer.com/article/10.1007/s41468-022-00094-6).

## Barcode bases for persistence modules

A persistence module $V$ is a representation of a type $\mathbb{A}_\ell$ quiver $Q$:

$$V_0 \longleftrightarrow V_1 \longleftrightarrow \cdots V_{\ell-1} \longleftrightarrow V_{\ell} $$ with linears maps $f_{i} \colon V_i \rightarrow V_{i+1}$ or $f_{i} \colon V_{i+1} \leftarrow V_{i}$ depending on the directions of the arrows.

The given input should then be a sequence of matrices $(A_i)$ representating the linears maps in a chosen basis, and a parameter $t \in \set{0,1 }^{\ell}$ representating the directions of the arrows, with the convention that $t_i=0$ if $V_i \rightarrow V_{i+1}$ and $t_i=1$ if $V_{i+1} \leftarrow V_i$. Computations are made over a field $\mathbb{F}$ which must be specified via bbase.Field. Supported fields include finite fields $\mathbb{F}_p$ and $\mathbb{R}$, specified by the parameter $p$ (which can be 0 in the case of real number).

The function bbase.bform takes as input a matrix sequence $(A_i)$, the orientation $t$ of the underlying quiver and the field $\mathbb{F}$ over which computations are made. The field is defined via F=bbase.Field(p). The output is a matrix sequence $(X_i)$ and corresponding basis change $(B_i)$. If the default parameter basis is set to False, bbase.bform modifies the underlying matrix sequence $(A_i)$ directly and outputs nothing.

We may check the correct basis change is outputed via bbase.bform(X,t,F,B) (note that if B is not specified this performs a random basis change on X).

Finally, we may extract the barcode of matrices $(X_i)$ in barcode form via bbase.barcode(X,t). The output is a dictionnary with keys pairs $(i,j)$ of admisibble bars $0 \leq i \leq j \leq \ell$ and values the corresponding multiplicity. If the default parameter list is set to True, this output is a list of bars instead of a dictionnary.

```python
import bbase
import numpy as np

A, t = [np.array([[6,2,5],[1,2,3]]), np.array([[0,0,3,2],[1,2,6,4]]), np.array([[1,5,3,6],[1,2,0,4]])], [0,1,0]
F=bbase.Field(7)
X,B=bbase.bform(A,t,F)
Y=bbase.basis_change(X,t,F,B)

for k in range(3):
    if (A[k]==Y[k]).all():
        print('Correct change of basis !')

bbase.bform(A,t,F,basis=False)
#We now have A=X.


barcode=bbase.barcode(X,t)
barcode_as_list=bbase.barcode(X,t,list=True)
```
