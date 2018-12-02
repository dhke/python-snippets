# -*- encoding=utf-8 -*-

__all__ = [
    'random_doubly_stochastic',
]

import numpy as np


def random_doubly_stochastic(size, method='sinkhorn', max_error=None):
    """
        Generate a random stochastic matrix with dimensions
        SIZE x SIZE.

        The generation method depends on the METHOD argument.
        Currently,
        - "sinkhorn" for Sinkhorn-Knopp iterative approximation, and
        - "permute" for generation as the sum of scaled permutation
          matrices
        are supported.

        Returns a SIZE x SIZE random matrix with
        all row and column sums equal to 1.
    """
    if method == 'sinkhorn':
        return random_doubly_stochastic_sinkhorn(size, max_error=max_error)
    elif method == 'permute':
        return random_doubly_stochastic_permute(size, max_error=max_error)
    else:
        raise ValueError("Unknown generation method '{}'".format(method))


def random_doubly_stochastic_sinkhorn(size, max_error=None):
    """
        Generate a random stochastic matrix with dimensions
        SIZE x SIZE using Sinkhorn-Knopp iterative approximation.

        The algorithm starts with a random matrix and
        iteratively normalizes colum and row vectors
        until the maximum residual error is below MAX_ERROR.

        If MAX_ERROR is not set, it defaults to 1024 * eps.
    """
    if max_error is None:
        max_error = 1024 * np.finfo(float).eps

    m = np.matrix(np.random.random((size, size)))
    error = float('Inf')
    while error > max_error:
        m = np.divide(m, m.sum(axis=0), order='C')
        m = np.divide(m, m.sum(axis=1), order='K')

        error = max(
            np.max(np.abs(1 - m.sum(axis=0))),
            np.max(np.abs(1 - m.sum(axis=1)))
        )
    return m


def random_doubly_stochastic_permute(size, max_error=None):
    """
        Generate a random stochastic matrix with dimensions
        SIZE x SIZE by combining SIZE permutation matrices P_k,
        such that

        M = k_0 P_0 + k_1 P_1 + ... k_{size - 1} P_{size - 1}

        with P_i being random permutation matrices and
        k_i being random real numbers such that sum(k_i) = 1

        MAX_ERROR is ignored.
    """
    m = np.zeros((size, size))
    I = np.identity(size)

    # n random coefficients
    coeffs = np.random.random(size)
    # enforce coefficient sum == 1
    coeffs /= np.sum(coeffs)

    # index array for identity permutation
    values = np.array(range(0, size))
    for c in coeffs:
        # generate new random permutation in place
        np.random.shuffle(values)
        # add scaled permutation matrix
        m += c * I[values, :]
    return m
