import pandas as pd


# Data Loading and Initial Inspection
def load_and_initial_inspection_data(f_path):
    df = pd.read_csv(f_path)
    print_dataframe_info(df, message='Initial Inspection:')
    return df


def print_dataframe_info(df, message=''):
    if message:
        print(f'\n***************************************')
        print(f'\n{message}\n')
    print(df.info())
    print(f'\n')
    print(df.head())  # first 5 rows
    print(f'\n')
    count_missing_values(df)


def count_missing_values(df):
    missing_values = df.isnull().sum()
    print(f'Missing values in columns:\n{missing_values[missing_values > 0]}')


# Handling Missing Values
def handle_missing_values(df):
    count_missing_values(df)
    df['name'] = df['name'].fillna('Unknown')
    df['host_name'] = df['host_name'].fillna('Unknown')
    df['last_review'] = df['last_review'].fillna(pd.NaT)
    print_dataframe_info(df, 'After handling missing values:')


# Data Transformation
def transform_data(df):
    price_bins = [0, 100, 300, float('inf')]
    price_labels = ['Low', 'Medium', 'High']
    df['price_category'] = pd.cut(df['price'], bins=price_bins, labels=price_labels, right=False)

    minimum_nights_bins = [0, 4, 15, float('inf')]
    minimum_nights_labels = ['Short-term', 'Medium-term', 'Long-term']
    df['stay_category'] = pd.cut(df['minimum_nights'], bins=minimum_nights_bins, labels=minimum_nights_labels,
                                 right=False)

    print_dataframe_info(df, 'After data transformation:')


# Data Validation
def validate_data(df):
    print_dataframe_info(df, 'Data validation:')

    # NaN values in the column last_review excluding NaT

    if df[['name', 'host_name']].isnull().sum().sum() == 0:
        print('No missing values in critical columns.')
    else:
        raise AssertionError('Missing values in critical columns')

    if (df['price'] > 0).all():
        print('All price values are greater than 0.')
    else:
        df = df[df['price'] > 0]
        print('Removed rows with price equal to 0.')

    return df


if __name__ == '__main__':
    file_path = 'AB_NYC_2019.csv'
    dataf = load_and_initial_inspection_data(file_path)
    handle_missing_values(dataf)
    transform_data(dataf)
    dataf = validate_data(dataf)

    dataf.to_csv('cleaned_airbnb_data.csv', index=False)
    print("Cleaned dataset saved as 'cleaned_airbnb_data.csv'.")
