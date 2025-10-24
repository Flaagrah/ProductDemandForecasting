import pandas as pd
import numpy as np

def create_sales_subset_streaming(input_file='sales_train_validation.csv', 
                                  output_file='sales_train_validation_subset.csv', 
                                  subset_ratio=0.1,
                                  chunk_size=1000):
    """
    Create a subset of the sales data by sampling items from each category/store/state.
    Uses streaming approach to avoid memory issues.
    
    Args:
        input_file (str): Input sales file
        output_file (str): Output subset file
        subset_ratio (float): Fraction of data to keep (0.1 = 10%)
        chunk_size (int): Number of rows to process at a time
    """
    
    print(f"Creating {subset_ratio*100}% subset of sales data...")
    
    # First pass: analyze data structure without loading everything
    print("Analyzing data structure...")
    
    # Read just the header to get column names
    header_chunk = pd.read_csv(input_file, nrows=1)
    id_columns = ['id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id']
    d_columns = [col for col in header_chunk.columns if col.startswith('d_')]
    
    print(f"Found {len(d_columns)} daily columns")
    
    # Count total rows
    print("Counting total rows...")
    total_rows = sum(1 for _ in open(input_file)) - 1  # Subtract header
    print(f"Total rows: {total_rows}")
    
    # Initialize tracking variables
    category_store_counts = {}
    sampled_items = []
    processed_rows = 0
    
    print("First pass: counting items per category-store combination...")
    
    # First pass: count items per category-store combination
    for chunk in pd.read_csv(input_file, chunksize=chunk_size):
        for _, row in chunk.iterrows():
            key = (row['cat_id'], row['store_id'])
            category_store_counts[key] = category_store_counts.get(key, 0) + 1
        
        processed_rows += len(chunk)
        if processed_rows % 10000 == 0:
            print(f"Processed {processed_rows}/{total_rows} rows...")
    
    print(f"Found {len(category_store_counts)} category-store combinations")
    
    # Calculate how many items to sample from each combination
    sampling_targets = {}
    for (cat, store), count in category_store_counts.items():
        n_sample = max(1, int(count * subset_ratio))
        sampling_targets[(cat, store)] = n_sample
        print(f"Category {cat}, Store {store}: {count} items -> will sample {n_sample}")
    
    # Second pass: sample items
    print("\nSecond pass: sampling items...")
    category_store_sampled = {key: 0 for key in sampling_targets.keys()}
    processed_rows = 0
    
    for chunk in pd.read_csv(input_file, chunksize=chunk_size):
        chunk_sampled = []
        
        for _, row in chunk.iterrows():
            key = (row['cat_id'], row['store_id'])
            
            if key in sampling_targets:
                # Use random sampling with probability proportional to subset_ratio
                if np.random.random() < subset_ratio:
                    chunk_sampled.append(row)
                    category_store_sampled[key] += 1
        
        if chunk_sampled:
            sampled_items.extend(chunk_sampled)
        
        processed_rows += len(chunk)
        if processed_rows % 10000 == 0:
            print(f"Processed {processed_rows}/{total_rows} rows...")
    
    # Convert to DataFrame
    print("Converting to DataFrame...")
    sales_subset = pd.DataFrame(sampled_items)
    
    # Sort by id for consistency
    sales_subset = sales_subset.sort_values('id').reset_index(drop=True)
    
    print(f"Subset shape: {sales_subset.shape}")
    print(f"Reduction: {len(sales_subset)} / {total_rows} = {len(sales_subset)/total_rows:.1%}")
    print(f"Daily columns: {len([col for col in sales_subset.columns if col.startswith('d_')])}")
    
    # Save subset
    print(f"Saving subset to {output_file}...")
    sales_subset.to_csv(output_file, index=False)
    
    # Melt the subset data and save to intermediate file
    print("Melting subset data...")
    d_columns = [col for col in sales_subset.columns if col.startswith('d_')]
    id_columns = ['id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id']
    
    melted_subset = pd.melt(
        sales_subset, 
        id_vars=id_columns,
        value_vars=d_columns,
        var_name='d',
        value_name='sales'
    )
    
    # Convert d to integer
    melted_subset['d'] = melted_subset['d'].str.replace('d_', '').astype(int)
    
    # Save melted subset
    melted_output_file = 'sales_train_validation_subset_melted.csv'
    print(f"Saving melted subset to {melted_output_file}...")
    melted_subset.to_csv(melted_output_file, index=False)
    
    print(f"Melted subset shape: {melted_subset.shape}")
    
    # Show summary statistics
    print("\nSubset summary:")
    print(f"Categories: {sales_subset['cat_id'].value_counts().to_dict()}")
    print(f"States: {sales_subset['state_id'].value_counts().to_dict()}")
    print(f"Stores: {sales_subset['store_id'].value_counts().to_dict()}")
    
    return output_file, melted_output_file

def filter_prices_by_subset(melted_subset_file='sales_train_validation_subset_melted.csv',
                           prices_file='sell_prices.csv',
                           output_file='sell_prices_subset.csv'):
    """
    Filter sell_prices.csv to only include items that are in the melted subset.
    
    Args:
        melted_subset_file (str): Path to the melted subset file
        prices_file (str): Path to the original sell_prices file
        output_file (str): Path to save the filtered prices file
    
    Returns:
        str: Path to the filtered prices file
    """
    
    print(f"Filtering {prices_file} to only include items from {melted_subset_file}...")
    
    # Load the melted subset to get unique items
    print("Loading melted subset...")
    melted_subset = pd.read_csv(melted_subset_file)
    print(f"Melted subset shape: {melted_subset.shape}")
    
    # Get unique items from the subset
    unique_items = melted_subset['item_id'].unique()
    print(f"Found {len(unique_items)} unique items in subset")
    
    # Load prices data in chunks and filter
    print("Filtering prices data...")
    filtered_prices = []
    chunk_size = 10000
    processed_rows = 0
    
    for chunk in pd.read_csv(prices_file, chunksize=chunk_size):
        # Filter chunk to only include items in our subset
        filtered_chunk = chunk[chunk['item_id'].isin(unique_items)]
        
        if len(filtered_chunk) > 0:
            filtered_prices.append(filtered_chunk)
        
        processed_rows += len(chunk)
        if processed_rows % 100000 == 0:
            print(f"Processed {processed_rows:,} rows...")
    
    # Combine filtered chunks
    print("Combining filtered prices...")
    prices_subset = pd.concat(filtered_prices, ignore_index=True)
    
    # Sort by item_id and wm_yr_wk for consistency
    prices_subset = prices_subset.sort_values(['item_id', 'wm_yr_wk']).reset_index(drop=True)
    
    print(f"Filtered prices shape: {prices_subset.shape}")
    print(f"Reduction: {len(prices_subset)} / {processed_rows:,} = {len(prices_subset)/processed_rows:.1%}")
    
    # Save filtered prices
    print(f"Saving filtered prices to {output_file}...")
    prices_subset.to_csv(output_file, index=False)
    
    # Show summary statistics
    print("\nFiltered prices summary:")
    print(f"Unique items: {prices_subset['item_id'].nunique()}")
    print(f"Unique stores: {prices_subset['store_id'].nunique()}")
    print(f"Unique weeks: {prices_subset['wm_yr_wk'].nunique()}")
    print(f"Price range: ${prices_subset['sell_price'].min():.2f} - ${prices_subset['sell_price'].max():.2f}")
    
    return output_file

if __name__ == "__main__":
    # Create 0.1% subset using streaming
    subset_file, melted_file = create_sales_subset_streaming(subset_ratio=0.001, chunk_size=1000)  # 0.1% subset
    print(f"\nSubset created successfully: {subset_file}")
    print(f"Melted subset created successfully: {melted_file}")
    
    # Filter prices to only include items from the subset
    print("\n" + "="*50)
    prices_file = filter_prices_by_subset(melted_file)
    print(f"Filtered prices created successfully: {prices_file}")
