import pandas as pd


# Data Loading
def load_data(file_p):
    df = pd.read_csv(file_p)
    return df


# Advanced Data Manipulation
def advanced_data_manipulation(df):
    required_columns = ['neighbourhood_group', 'room_type', 'price', 'minimum_nights', 'availability_365']
    if not all(col in df.columns for col in required_columns):
        raise AssertionError(f'One or more required columns are missing: {required_columns}')

    price_trends = df.pivot_table(index='neighbourhood_group', columns='room_type', values='price', aggfunc='mean')

    long_format = pd.melt(df, id_vars=['neighbourhood_group', 'room_type'], value_vars=['price', 'minimum_nights'])

    # Classify listings by availability
    def classify_availability(days):
        if days < 50:
            return "Rarely Available"
        elif 50 <= days <= 200:
            return "Occasionally Available"
        else:
            return "Highly Available"

    df['availability_status'] = df['availability_365'].apply(classify_availability)

    return price_trends, long_format, df


# Descriptive Statistics
def descriptive_statistics(df):
    required_columns = ['price', 'minimum_nights', 'number_of_reviews']
    if not all(col in df.columns for col in required_columns):
        raise AssertionError(f'One or more required columns are missing: {required_columns}')

    stats = df[required_columns].describe().T
    return stats


# Time Series Analysis
def time_series_analysis(df):
    if 'last_review' not in df.columns:
        raise AssertionError("Column 'last_review' is missing")

    df['last_review'] = pd.to_datetime(df['last_review'])
    df.set_index('last_review', inplace=True)

    monthly_trends = df.resample('ME').agg({
        'price': 'mean',
        'number_of_reviews': 'sum'
    })

    monthly_avg = df.groupby(df.index.month).agg({
        'price': 'mean',
        'number_of_reviews': 'mean'
    })

    return monthly_trends, monthly_avg


def print_analysis_results(data, message=''):
    if message:
        print(f'\n{message}')
    print(data)


# Main script
if __name__ == '__main__':
    file_path = 'AB_NYC_2019.csv'  # Specify the path to your CSV file

    dataf = load_data(file_path)

    price_trends, long_format, dataf = advanced_data_manipulation(dataf)
    print_analysis_results(price_trends, "Price Trends by Neighbourhood and Room Type")
    print_analysis_results(long_format.head(), "Long Format Data (First 5 Rows)")
    print_analysis_results(dataf[['availability_status']].head(), "Availability Status (First 5 Rows)")

    statist = descriptive_statistics(dataf)
    print_analysis_results(statist, "Descriptive Statistics")

    month_trends, month_avg = time_series_analysis(dataf)
    print_analysis_results(month_trends, "Monthly Trends in Price and Number of Reviews")
    print_analysis_results(month_avg, "Seasonal Patterns in Price and Number of Reviews")

    month_trends.to_csv("time_series_airbnb_data3.csv")
    print('Time series data saved as time_series_airbnb_data.csv.')
