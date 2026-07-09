import os
import pandas as pd

# define paths
DATA_DIR = "./data"
OUTPUT_FILE = "formatted_data.csv"

dataframes = []

# read all files from the data directory
print("Reading raw CSV files...")
for file in os.listdir(DATA_DIR):
    if file.endswith(".csv"):
        file_path = os.path.join(DATA_DIR, file)
        df = pd.read_csv(file_path)
        dataframes.append(df)

# combine all three dataframes into one single raw dataframe
combined_raw_df = pd.concat(dataframes, ignore_index=True)

# filter rows where product is 'Pink Morsel'
pink_morsels_df = combined_raw_df[combined_raw_df['product'].str.lower() == 'pink morsel'].copy()

# clean and convert data types
# clean the price field by stripping out '$' if it exists, then cast to float
if pink_morsels_df['price'].dtype == 'object':
    pink_morsels_df['price'] = pink_morsels_df['price'].str.replace('$', '', regex=False)

pink_morsels_df['price'] = pink_morsels_df['price'].astype(float)
pink_morsels_df['quantity'] = pink_morsels_df['quantity'].astype(int)

# calculate Sales (quantity * price)
pink_morsels_df['sales'] = pink_morsels_df['quantity'] * pink_morsels_df['price']

# keep only the requested fields: sales, date, region
final_df = pink_morsels_df[['sales', 'date', 'region']]

# sort the records chronologically by date
final_df = final_df.sort_values(by='date')

# 7. Write out to the final single CSV file without row index indices
final_df.to_csv(OUTPUT_FILE, index=False)
print(f"Success! Formatted data written to {OUTPUT_FILE}")