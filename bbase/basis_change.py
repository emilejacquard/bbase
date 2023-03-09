import numpy as np
import copy


def rand_basis(X, t, F):
    G = []
    v = dim_vect(X, t)
    for i in range(len(v)):
        if F.p == 0:
            x = np.random.randint(-4, 4, (v[i], v[i])).astype('float')
            while (F.inv_mat(x) == np.zeros((v[i], v[i]))).all():
                x = np.random.randint(-4, 4, (v[i], v[i])).astype('float')
            G.append(x)

        else:
            x = np.random.randint(0, F.p, (v[i], v[i]))
            if v[i]!=0:
                while (F.inv_mat(x) == np.zeros((v[i], v[i]))).all():
                    x = np.random.randint(0, F.p - 1, (v[i], v[i]))
            G.append(x)

    return G


def basis_change(X, t, F, G=None, Q='path', keep=True):
    if keep:
        X = copy.deepcopy(X)
    if Q == 'path':
        if G is None:
            G = rand_basis(X, t, F)
        for k in range(len(X)):
            if t[k] == 0:
                X[k] = F.matmul(G[k + 1], F.matmul(X[k], F.inv_mat(G[k])))
            if t[k] == 1:
                X[k] = F.matmul(G[k], F.matmul(X[k], F.inv_mat(G[k + 1])))

    elif Q == 'rectangle':
        l = len(t)
        if G is None:
            K, H = rand_basis([X[(k, k + 1)] for k in range(l)], t, F), rand_basis(
                [(X[(k, k + 1)]) for k in range(l + 1, 2 * l + 1)], t, F)
        else:
            K, H = G[0], G[1]

        for k in range(l):
            if X[k,k+1].shape!=(0,0):
                X[k, k + 1] = F.matmul(K[k + 1], F.matmul(X[k, k + 1], F.inv_mat(K[k])))
            if X[k+l+1,k+l+2].shape!=(0,0):
                X[k + l + 1, k + l + 2] = F.matmul(H[k + 1], F.matmul(X[k + l + 1, k + l + 2], F.inv_mat(H[k])))
            if X[k,k+l+1].shape!=(0,0):
                X[k, k + l + 1] = F.matmul(H[k], F.matmul(X[k, k + l + 1], F.inv_mat(K[k])))
        if X[l,2*l+1].shape!=(0,0):
            X[l, 2 * l + 1] = F.matmul(H[l], F.matmul(X[l, 2 * l + 1], F.inv_mat(K[l])))
    if keep:
        return X


def dim_vect(V, t):
    v = []
    for k in range(len(t)):
        if t[k] == 0:
            v.append(V[k].shape[1])
        else:
            v.append(V[k].shape[0])
    if t[-1] == 0:
        v.append(V[-1].shape[0])
    else:
        v.append(V[-1].shape[1])
    return v
