import numpy as np


def print_array(data, message=''):
    if message:
        print(message)
    print(data)
    print('\n')


if __name__ == '__main__':

    flat_array = np.arange(1, 11)
    print_array(flat_array, 'One dimensiomal array :')

    square_array = np.arange(1, 10).reshape(3, 3)
    print_array(square_array, 'Two dimensionals array :')

    flat_third_el = flat_array[2]
    print_array(flat_third_el, 'Third element:')

    flat_slice = square_array[:2, :2]
    print_array(flat_slice, 'First two rows and columns :')

    flat_add_five = flat_array + 5
    print_array(flat_add_five, 'After adding 5 to each element :')

    square_mult_two = square_array * 2
    print_array(square_mult_two, 'After multiply each element by 2 :')
