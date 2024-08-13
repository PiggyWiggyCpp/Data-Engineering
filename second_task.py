import numpy as np
import datetime

transaction_dtype = np.dtype([
    ('transaction_id', np.int32),
    ('user_id', np.int32),
    ('product_id', np.int32),
    ('quantity', np.int32),
    ('price', np.float64),
    ('timestamp', np.int64)
])


def create_transactions_array():
    data = np.array([
        [1, 10, 1954, 2, 15.5, int(datetime.datetime(2024, 8, 1, 10, 30).timestamp())],
        [2, 9, 2415, 1, 22.17, int(datetime.datetime(2024, 8, 2, 14, 45).timestamp())],
        [3, 2, 1954, 3, 15.5, int(datetime.datetime(2024, 8, 3, 9, 15).timestamp())],
        [4, 2, 4125, 5, 10.95, int(datetime.datetime(2024, 8, 4, 16, 0).timestamp())],
        [5, 5, 6541, 5, 54.17, int(datetime.datetime(2024, 8, 5, 11, 20).timestamp())],
        [6, 2, 6541, 4, 7.45, int(datetime.datetime(2024, 8, 6, 13, 10).timestamp())]
    ])
    return np.array(list(map(tuple, data)), dtype=transaction_dtype)


def print_array(array, message=""):
    print(message)
    print(array)
    print('\n')


# Data Analysis:
def total_revenue(transact_arr):
    return np.sum(transact_arr['quantity'] * transact_arr['price'])


def unique_users(transact_arr):
    return np.unique(transact_arr['user_id']).size


def most_purchased_product(transact_arr):
    products, quantities = np.unique(transact_arr['product_id'], return_counts=True)
    return products[np.argmax(quantities)]


def convert_price_to_int(transact_arr):
    new_dtype = np.dtype([
        ('transaction_id', np.int32),
        ('user_id', np.int32),
        ('product_id', np.int32),
        ('quantity', np.int32),
        ('price', np.int64),
        ('timestamp', np.int64)
    ])

    new_transact_arr = np.empty(transact_arr.shape, dtype=new_dtype)
    for name in transact_arr.dtype.names:
        new_transact_arr[name] = transact_arr[name] if name != 'price' else transact_arr[name].astype(np.int64)

    return new_transact_arr


def check_data_types(transact_arr):
    return [transact_arr.dtype[i].name for i in transact_arr.dtype.names]


# Array Manipulation:
def product_quantity_array(transact_arr):
    return transact_arr[['product_id', 'quantity']]


def user_transaction_count(transact_arr):
    user_ids, counts = np.unique(transact_arr['user_id'], return_counts=True)
    return np.column_stack((user_ids, counts))


def masked_array(transact_arr):
    mask = transact_arr['quantity'] > 0
    return transact_arr[mask]


# Arithmetic and Comparison:
def price_increase(transact_arr, percent):
    transact_arr['price'] = transact_arr['price'] * (1 + percent / 100)

    return transact_arr


def filter_transactions(transact_arr, min_quantity):
    return transact_arr[transact_arr['quantity'] > min_quantity]


def revenue_comparison(transact_arr, s_date1, e_date1, s_date2, e_date2):
    mask1 = (transact_arr['timestamp'] >= s_date1) & (transact_arr['timestamp'] <= e_date1)
    mask2 = (transact_arr['timestamp'] >= s_date2) & (transact_arr['timestamp'] <= e_date2)

    revenue_first = np.sum(transact_arr[mask1]['quantity'] * transact_arr[mask1]['price'])
    revenue_second = np.sum(transact_arr[mask2]['quantity'] * transact_arr[mask2]['price'])

    return revenue_first, revenue_second


# Indexing and Slicing:
def user_transactions(transact_arr, user_id):
    return transact_arr[transact_arr['user_id'] == user_id]


def date_range_slicing(transact_arr, start_date, end_date):
    return transact_arr[(transact_arr['timestamp'] >= start_date) & (transact_arr['timestamp'] <= end_date)]


def top_products(transact_arr, top_n=5):
    revenues = transact_arr['quantity'] * transact_arr['price']
    top_indices = np.argsort(revenues)[-top_n:]
    return transact_arr[top_indices]


if __name__ == "__main__":
    transactions = create_transactions_array()
    print_array(transactions, "Original transaction array:")

    revenue = total_revenue(transactions)
    print(f"Total revenue: {revenue:.2f} \n")

    unique_users_count = unique_users(transactions)
    print(f"Number of unique users: {unique_users_count} \n")

    most_purchased = most_purchased_product(transactions)
    print(f"Most purchased product: {most_purchased} \n")

    transactions_with_int_prices = convert_price_to_int(transactions)
    print_array(transactions_with_int_prices, "Prices are converted to integer type:")

    data_types = check_data_types(transactions)
    print(f"Column data types: {data_types} \n")

    product_quantities = product_quantity_array(transactions)
    print_array(product_quantities, "Array with products and their quantities:")

    user_transaction_counts = user_transaction_count(transactions)
    print_array(user_transaction_counts, "Number of transactions per user:")

    masked_transactions = masked_array(transactions)
    print_array(masked_transactions, "Masked array of transactions with count greater than 0:")

    percent_data = 5
    transactions = price_increase(transactions, percent_data)
    print_array(transactions, f"Prices increased by {percent_data}%:")

    filtered_transactions = filter_transactions(transactions, 1)
    print_array(filtered_transactions, "Transactions with quantity greater than 1:")

    start_date1 = int(datetime.datetime(2024, 8, 1, 0, 0).timestamp())
    end_date1 = int(datetime.datetime(2024, 8, 3, 23, 59).timestamp())
    start_date2 = int(datetime.datetime(2024, 8, 4, 0, 0).timestamp())
    end_date2 = int(datetime.datetime(2024, 8, 6, 23, 59).timestamp())

    revenue1, revenue2 = revenue_comparison(transactions, start_date1, end_date1, start_date2, end_date2)
    print(f"Revenue in period 1 : {revenue1:.2f} \n")
    print(f"Revenue in period 2 : {revenue2:.2f} \n")

    user_id_data = 2
    user_trans = user_transactions(transactions, user_id_data)
    print_array(user_trans, f"User ID {user_id_data} transactions:")

    sliced_transactions = date_range_slicing(transactions, start_date1, end_date2)
    print_array(sliced_transactions, f"Transactions during the period from {start_date1} to {end_date2}:")

    top_product_transactions = top_products(transactions, 5)
    print_array(top_product_transactions, "Top 5 Product Transactions by revenue:")

    assert transactions.shape[0] > 0, "The array is empty"
    assert 'transaction_id' in transactions.dtype.names, "The array must contain a field 'transaction_id'"
    assert transactions_with_int_prices['price'].dtype == np.int64, "The price column must be an integer"
    assert len(filtered_transactions) <= len(
        transactions), "The number of filtered transactions cannot exceed the total number"
