# -*- encoding=utf-8 -*-

def cartesian(row, col, operator=None):
    """
        Create a dataframe representing the cartesian product
        of `row` and `col`.

        The index of `col` is used for the columns of the dataframe.
        Each of the columns has `len(row)` elements.

        Returns a new dataframe with the cartesian.
    """
    df = pd.DataFrame()
    if operator is None:
        for cidx, cval in col.iteritems():
            df[cidx] = row * cval
    else:
        for cidx, cval in col.iteritems():
            df[cidx] = operator(row, cval)
    return df
