import numpy as np


def create_array(rows, columns):
    return np.random.randint(0, 100, (rows, columns))


def transpose_array(array):
    return np.transpose(array)


def reshape_array(array, new_shape):
    return np.reshape(array, new_shape)


def split_array(array, num_splits2, axis=0):
    return np.split(array, num_splits2, axis)


def combine_arrays(arrays, axis=0):
    return np.concatenate(arrays, axis)


def print_array(array, message=""):
    print(f"{message}\n{array}\n")


if __name__ == "__main__":
    rows_val = 6
    columns_val = 6
    initial_array = create_array(rows_val, columns_val)
    print_array(initial_array, f"Initial array size {rows_val}x{columns_val}:")

    transposed_array = transpose_array(initial_array)
    print_array(transposed_array, "Transposed array:")
    assert transposed_array.shape == (rows_val, columns_val), "Error: Incorrect shape after transposition"

    resh_rows = 3
    resh_columns = 12
    reshaped_array = reshape_array(transposed_array, (resh_rows, resh_columns))
    print_array(reshaped_array, f"Reshaped array ({resh_rows}x{resh_columns}):")
    assert reshaped_array.shape == (resh_rows, resh_columns), "Error: Invalid form after changing form"

    num_splits = 2
    assert resh_rows % num_splits == 0, "Error: The array cannot be evenly divided into the specified number of subarrays"

    axis_data = 0
    subarray_rows = resh_rows // num_splits
    subarray_cols = resh_columns

    split_arrays = split_array(reshaped_array, num_splits, axis=axis_data)
    for i, sub_array in enumerate(split_arrays):
        print_array(sub_array, f"Subarray {i+1}:")
        assert sub_array.shape == (subarray_rows, subarray_cols), f"Error: Invalid subarray shape {i+1}"

    combined_array = combine_arrays(split_arrays, axis=axis_data)
    print_array(combined_array, "Recombined array:")
    assert combined_array.shape == reshaped_array.shape, "Error: Incorrect form after merging"
