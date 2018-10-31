# -*- encoding=utf-8 -*-

# from scipy.special import gammainc
from scipy.stats import chi2

from . import cartesian

# this is just here for completeness
# def pdf_chi2(x, k):
#     """
#         Probability density function of the χ² distribution
#
#         `x`: the input value
#         `k`: degress of freedom for the χ² distribution
#     """
#     k2 = k / 2.0
#     return ((np.power(x, k2 - 1) * np.exp(-x / 2.0))
#             / (np.exp2(k2) * gamma(k2)
#     )


# alternative implementation of the χ² cdf.
#
# To use this instead of `scipy.stats.chi2`,
# - comment the alias for `chi2.pdf`, below
# - uncomment this function
# - uncomment the import for `scipy.special.gammainc`, above.
#
# def chi2_cdf(x, k):
#     """
#         Cumulative distibution function of the χ² distribution
#
#         `x`: the input value
#         `k`: degress of freedom for the χ² distribution
#     """
#     # scipy already provides regularized lower gamma function.
#     # Use it, but note parameter inversal
#     return gammainc(k / 2.0, x / 2.0)
cdf_chi2 = chi2.cdf


def chi_independence(data):
    """
        Determine the confidence value that the
        categories from the input data are statistically
        independent using χ² testing.

        The input is assumed to be a dataframe with columns
        and rows representing the counted samples
        for each combination of categories.

        Returns the p value from the χ² test of independence.
    """
    rowsum = data.sum(axis=0)
    colsum = data.sum(axis=1)
    # calculate the cartesian product of all row sums and
    # column sums and normalize them by the row total.
    # This yields the matrix of expected values per
    # category pair.
    expected = cartesian(colsum, rowsum) / rowsum.sum()
    # calculate the χ² measure for the expected data
    # as the sum of the relative (to the expected values)
    # square errors over all input cells.
    x_chi = ((data - expected) ** 2 / expected).sum().sum()

    # determine the degress of freedom for the
    # χ² test, which is (nrows - 1) * (ncols - 1)
    degrees_of_freedom = (data.shape[0] - 1) * (data.shape[1] - 1)

    # estimate p value, i.e. the probability that
    # the input categories are independent
    p = 1 - cdf_chi2(x_chi, degrees_of_freedom)
    return p
