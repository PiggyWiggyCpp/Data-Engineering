import numpy as np


def create_array(rows, columns):
    return np.random.randint(0, 100, (rows, columns))


def print_array(array, message=''):
    if message:
        print(message)
    print(array)
    print('\n')


# Data I/O Functions:
def save_array(array, filename_base):
    np.savetxt(f"{filename_base}.txt", array, fmt='%d')
    np.savetxt(f"{filename_base}.csv", array, delimiter=',', fmt='%d')
    np.save(f"{filename_base}.npy", array)


def load_array(filename_base):
    array_txt = np.loadtxt(f"{filename_base}.txt", dtype=int)
    array_csv = np.loadtxt(f"{filename_base}.csv", delimiter=',', dtype=int)
    array_npy = np.load(f"{filename_base}.npy")
    return array_txt, array_csv, array_npy


# Aggregate Functions:
def sum_array(array):
    return np.sum(array)


def mean_array(array):
    return np.mean(array)


def median_array(array):
    return np.median(array)


def standard_deviation_array(array):
    return np.std(array)


def sum_axis(array, axis):
    return np.sum(array, axis=axis)


def mean_axis(array, axis):
    return np.mean(array, axis=axis)


def median_axis(array, axis):
    return np.median(array, axis=axis)


def standard_deviation__axis(array, axis):
    return np.std(array, axis=axis)


if __name__ == '__main__':
    rows_val = 10
    columns_val = 10
    initial_array = create_array(rows_val, columns_val)
    print_array(initial_array, f"Initial array size {rows_val}x{columns_val}:")

    filename = "array_file"
    save_array(initial_array, filename)

    loaded_txt, loaded_csv, loaded_npy = load_array(filename)
    print_array(loaded_txt, "Loaded array from TXT file:")
    assert np.array_equal(initial_array, loaded_txt), "Error: data in TXT does not match the original data"

    print_array(loaded_csv, "Loaded array from CSV file:")
    assert np.array_equal(initial_array, loaded_csv), "Error: CSV data does not match the original data"

    print_array(loaded_npy, "Loaded array from Binary file:")
    assert np.array_equal(initial_array, loaded_npy), "Error: Binary data does not match the original data"

    total_sum = sum_array(initial_array)
    print_array(total_sum, "Sum of all array elements:")

    mean_value = mean_array(initial_array)
    print_array(mean_value, "Array mean:")

    median_value = median_array(initial_array)
    print_array(median_value, "Median of the array:")

    std_deviation = standard_deviation_array(initial_array)
    print_array(std_deviation, "Array standard deviation:")

    row_sums = sum_axis(initial_array, axis=1)
    print_array(row_sums, "Sum of elements by row:")

    col_sums = sum_axis(initial_array, axis=0)
    print_array(col_sums, "Sum of elements by columns:")

    row_means = mean_axis(initial_array, axis=1)
    print_array(row_means, "Row average:")

    col_means = mean_axis(initial_array, axis=0)
    print_array(col_means, "Column average:")

    row_medians = median_axis(initial_array, axis=1)
    print_array(row_medians, "Median by rows:")

    col_medians = median_axis(initial_array, axis=0)
    print_array(col_medians, "Median by columns:")

    row_std_devs = standard_deviation__axis(initial_array, axis=1)
    print_array(row_std_devs, "Row standard deviation:")

    col_std_devs = standard_deviation__axis(initial_array, axis=0)
    print_array(col_std_devs, "Column standard deviation:")

    assert total_sum == np.sum(initial_array), "Error: The sum of the elements does not match"
    assert mean_value == np.mean(initial_array), "Error: Average does not match"
    assert median_value == np.median(initial_array), "Error: median does not match"
    assert std_deviation == np.std(initial_array), "Error: standard deviation does not match"
