import pandas as pd


# Data Loading
def load_data(f_path):
    df = pd.read_csv(f_path)
    return df


# Data Selection and Filtering
def select_and_filter_data(df):
    required_columns = ['neighbourhood_group', 'price', 'number_of_reviews', 'minimum_nights', 'price_category',
                        'availability_365']
    if not all(col in df.columns for col in required_columns):
        raise AssertionError(f'One or more required columns are missing: {required_columns}')

    filtered_df = df[df['neighbourhood_group'].isin(['Manhattan', 'Brooklyn'])]
    filtered_df = filtered_df[(filtered_df['price'] > 100) & (filtered_df['number_of_reviews'] > 10)]

    filtered_df = filtered_df[required_columns]

    return filtered_df


# Aggregation and Grouping
def aggregate_and_group_data(df):
    grouped = df.groupby(['neighbourhood_group', 'price_category'])

    aggregate_df = grouped.agg({
        'price': 'mean',
        'minimum_nights': 'mean',
        'number_of_reviews': 'mean',
        'availability_365': 'mean'
    }).reset_index()

    required_columns_after_agg = ['neighbourhood_group', 'price_category', 'price', 'minimum_nights',
                                  'number_of_reviews', 'availability_365']
    if not all(col in aggregate_df.columns for col in required_columns_after_agg):
        raise AssertionError(f'One or more columns are missing after aggregation: {required_columns_after_agg}')

    return aggregate_df


# Data Sorting and Ranking
def sort_and_rank_data(df):
    if 'price' not in df.columns or 'number_of_reviews' not in df.columns:
        raise AssertionError("Columns price or number_of_reviews are missing for sorting")

    sorted_df = df.sort_values(by=['price', 'number_of_reviews'], ascending=[False, True])

    if 'neighbourhood_group' not in df.columns:
        raise AssertionError('Column neighbourhood_group is missing for ranking')

    neighborhood_rank = df.groupby('neighbourhood_group').agg({
        'price': 'mean',
        'neighbourhood_group': 'count'
    }).rename(columns={'neighbourhood_group': 'total_listings', 'price': 'average_price'}).reset_index()

    neighborhood_rank['ranking_by_listings'] = neighborhood_rank['total_listings'].rank(ascending=False)
    neighborhood_rank['ranking_by_price'] = neighborhood_rank['average_price'].rank(ascending=False)

    neighborhood_rank['overall_ranking'] = neighborhood_rank[['ranking_by_listings', 'ranking_by_price']].mean(axis=1)

    return sorted_df, neighborhood_rank


def print_grouped_data(df, message=''):
    if message:
        print(f'\n{message}')
    print(df)


if __name__ == '__main__':
    file_path = 'cleaned_airbnb_data.csv'
    dataf = load_data(file_path)
    df_after_filters = select_and_filter_data(dataf)

    grouped_df = aggregate_and_group_data(df_after_filters)

    df_sorted, neighborhood_r = sort_and_rank_data(df_after_filters)

    print_grouped_data(grouped_df, 'Aggregated Data by Neighbourhood and Price Category:')
    print_grouped_data(df_sorted, 'Sorted Data by Price and Number of Reviews:')
    print_grouped_data(neighborhood_r, 'Neighbourhood Ranking by Listings and Average Price:')

    grouped_df.to_csv('aggregated_airbnb_data.csv', index=False)
    print('Aggregated data saved as aggregated_airbnb_data.csv.')
