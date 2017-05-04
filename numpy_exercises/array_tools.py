import math
import numpy as np


def sub_array(array, shape, center, fill=None):
    """
    You can assume, that the input array is a numpy-array with arbitrary
    values. The shape parameter will be a tuple with (rows, cols), the center
    will be a tuple with the coordinates (row, col) and fill is defaulted to
    None, but can be assigned to any value that should be used for filling
    overlap. The function should return the appropriate sub-array as a
    numpy-array.
    """
    start_row = center[0] - math.ceil(shape[0] / 2) + 1
    end_row = start_row + shape[0]
    start_col = center[1] - math.ceil(shape[1] / 2) + 1
    end_col = start_col + shape[1]
    extract = array[max(start_row, 0):end_row, max(start_col, 0):end_col]

    if extract.shape == shape or fill is None:
        return extract

    pad_row_before = abs(start_row) * (start_row < 0)
    pad_col_before = abs(start_col) * (start_col < 0)
    pad_row_after = shape[0] - extract.shape[0] - pad_row_before
    pad_col_after = shape[1] - extract.shape[1] - pad_col_before

    paddings = ((pad_row_before, pad_row_after),
                (pad_col_before, pad_col_after))

    padded = np.pad(extract, paddings, 'constant', constant_values=fill)
    return padded
