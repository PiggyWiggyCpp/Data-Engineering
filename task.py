import pandas as pd
import seaborn as sns
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from matplotlib import image as mpimg


# Data Loading
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df


# Neighborhood Distribution of Listings
def neighborhood_distribution_of_listings(df, image_file):
    neighborhood_counts = df['neighbourhood_group'].value_counts().reset_index()
    neighborhood_counts.columns = ['neighbourhood_group', 'count']

    plt.figure(figsize=(10, 6))
    sns.barplot(x='neighbourhood_group', y='count', hue='neighbourhood_group', data=neighborhood_counts, dodge=False, legend=False)

    for index, row in neighborhood_counts.iterrows():
        plt.text(index, row['count'], row['count'], color='black', ha="center")

    plt.title('Neighborhood Distribution of Listings')
    plt.xlabel('Neighbourhood group')
    plt.ylabel('Number of listings')
    plt.tight_layout()
    plt.savefig(image_file)
    plt.close()


# Price Distribution Across Neighborhoods
def price_distribution_across_neighborhoods(df, image_file):
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='neighbourhood_group', y='price', hue='neighbourhood_group', data=df, showfliers=True, dodge=False)

    plt.title('Price Distribution Across Neighborhoods')
    plt.xlabel('Neighborhood group')
    plt.ylabel('Price')
    plt.tight_layout()
    plt.savefig(image_file)
    plt.close()


# Room Type vs Availability
def room_type_vs_availability(df, image_file):
    grouped_data = df.groupby(['neighbourhood_group', 'room_type'])['availability_365'].agg(['mean', 'std']).reset_index()

    plt.figure(figsize=(14, 8))
    sns.barplot(x='neighbourhood_group', y='mean', hue='room_type', data=grouped_data, palette='Paired', errorbar=None, capsize=.1, edgecolor='black', dodge=True)

    for i in range(len(grouped_data)):
        plt.errorbar(i, grouped_data['mean'][i], yerr=grouped_data['std'][i], fmt='none', c='black', capsize=5)

    plt.title('Room Type vs Availability')
    plt.xlabel('Neighbourhood group')
    plt.ylabel('Average availability (days per year)')
    plt.xticks(ticks=range(len(grouped_data['neighbourhood_group'].unique())), labels=grouped_data['neighbourhood_group'].unique(), fontsize=12, rotation=45, ha='right')
    plt.legend(title='Room type')
    plt.tight_layout()
    plt.savefig(image_file)
    plt.close()


# Correlation Between Price and Number of Reviews
def price_vs_number_of_reviews(df, image_file):
    plt.figure(figsize=(12, 8))
    sns.scatterplot(x='price', y='number_of_reviews', hue='room_type', style='room_type', data=df, palette='Dark2', s=100)

    plt.title('Correlation Between Price and Number of Reviews')
    plt.xlabel('Price')
    plt.ylabel('Number of reviews')
    plt.legend(title='Room type', loc='upper right')
    plt.tight_layout()
    plt.savefig(image_file)
    plt.close()


# Time Series Analysis of Reviews
def reviews_over_time(df, image_file):
    df['last_review'] = pd.to_datetime(df['last_review'], errors='coerce')
    df = df.dropna(subset=['last_review'])

    time_series = df.groupby(['last_review', 'neighbourhood_group'])['number_of_reviews'].sum().reset_index()
    time_series['rolling_avg'] = time_series.groupby('neighbourhood_group')['number_of_reviews'].rolling(window=30, min_periods=1).mean().reset_index(level=0, drop=True)

    plt.figure(figsize=(14, 8))
    sns.lineplot(x='last_review', y='rolling_avg', hue='neighbourhood_group', data=time_series, palette='tab10')

    plt.title('Trend of Number of Reviews by Neighborhood Group')
    plt.xlabel('Date of Last Feedback')
    plt.ylabel('Number of Reviews (Smoothed)')
    plt.legend(title='Neighborhood group')
    plt.tight_layout()
    plt.savefig(image_file)
    plt.close()


# Price and Availability Heatmap
def price_and_availability365(df, image_file):
    bins = range(0, df['price'].max() + 1, 100)
    plt.figure(figsize=(12, 8))
    labels = [f'{i}-{i + 99}' for i in bins[:-1]]
    df['price_bin'] = pd.cut(df['price'], bins=bins, labels=labels[::-1], right=False)

    pivot_table = df.pivot_table(index='price_bin', columns='neighbourhood', values='availability_365', aggfunc='mean', fill_value=0, observed=False)

    plt.imshow(pivot_table.values[::-1], cmap=mcolors.LinearSegmentedColormap.from_list("Heatmap colors", ("white", "blue", "red")), interpolation='nearest')

    plt.xticks(ticks=range(len(pivot_table.columns)), labels=pivot_table.columns, rotation=90)
    plt.yticks(ticks=range(len(pivot_table.index)), labels=pivot_table.index)

    plt.title('Heatmap')
    plt.colorbar(label='Days of Availability')
    plt.xlabel('Neighbourhood')
    plt.ylabel('Price Range')
    plt.tight_layout()
    plt.savefig(image_file)
    plt.close()


# Room Type and Review Count Analysis
def analysis_room_type_and_review_count(df, image_file):
    df_grouped = df.groupby(['neighbourhood_group', 'room_type'])['number_of_reviews'].sum().unstack()

    df_grouped.plot(kind='bar', stacked=True, figsize=(12, 8))

    plt.title('Number of Reviews by Room Type and Neighborhood Groups')
    plt.xlabel('Neighborhood Group')
    plt.ylabel('Number of Reviews')
    plt.legend(title='Room Type')
    plt.tight_layout()
    plt.savefig(image_file)
    plt.close()


# Output
def display_images_sequentially(image_paths, delay=0):
    for image_path in image_paths:
        img = mpimg.imread(image_path)
        plt.figure(figsize=(20, 10))
        plt.imshow(img)
        plt.axis('off')
        plt.pause(delay)
        plt.close()


if __name__ == '__main__':
    file_path = 'cleaned_airbnb_data.csv'
    image_files = [
        "neighborhood_distribution.png",
        "price_distribution.png",
        "room_type_vs_availability.png",
        "price_vs_number_of_reviews.png",
        'time_series_analysis_of_reviews.png',
        "price_and_availability365.png",
        "analysis_room_type_and_review_count.png"
    ]

    dataf = load_data(file_path)
    neighborhood_distribution_of_listings(dataf, image_files[0])
    price_distribution_across_neighborhoods(dataf, image_files[1])
    room_type_vs_availability(dataf, image_files[2])
    price_vs_number_of_reviews(dataf, image_files[3])
    reviews_over_time(dataf, image_files[4])
    price_and_availability365(dataf, image_files[5])
    analysis_room_type_and_review_count(dataf, image_files[6])

    display_images_sequentially(image_files, delay=1)
