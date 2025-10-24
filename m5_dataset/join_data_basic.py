import pandas as pd
import numpy as np
import os

def join_m5_data_basic(output_file='joined_data_basic.csv', chunk_size=10):
    """
    Basic streaming join using pandas only - no temporary files.
    Processes data in very small chunks to avoid memory/disk issues.
    """
    
    print("Loading calendar and prices data...")
    calendar = pd.read_csv('calendar.csv')
    prices = pd.read_csv('sell_prices.csv')
    
    # Join calendar with prices
    calendar_prices = calendar.merge(prices, on='wm_yr_wk', how='left')
    print(f"Calendar-prices shape: {calendar_prices.shape}")
    
    # Process sales data in very small chunks
    print("Processing sales data in small chunks...")
    
    # Get column info
    sales_sample = pd.read_csv('sales_train_validation_subset.csv', nrows=1)
    d_columns = [col for col in sales_sample.columns if col.startswith('d_')]
    id_columns = ['id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id']
    
    print(f"Processing {len(d_columns)} d columns")
    
    first_chunk = True
    chunk_count = 0
    total_rows = 0
    
    for chunk in pd.read_csv('sales_train_validation_subset.csv', chunksize=chunk_size):
        chunk_count += 1
        print(f"Processing chunk {chunk_count}...")
        
        # Melt the chunk
        melted_chunk = pd.melt(
            chunk, 
            id_vars=id_columns,
            value_vars=d_columns,
            var_name='d',
            value_name='sales'
        )
        
        # Convert d to integer
        melted_chunk['d'] = melted_chunk['d'].str.replace('d_', '').astype(int)
        
        # Ensure calendar_prices d column is also integer
        calendar_prices['d'] = calendar_prices['d'].str.replace('d_', '').astype(int)
        
        # Join with calendar_prices
        joined_chunk = melted_chunk.merge(
            calendar_prices, 
            left_on=['store_id', 'item_id', 'd'], 
            right_on=['store_id', 'item_id', 'd'], 
            how='left'
        )
        
        # Add features
        joined_chunk['day_of_week'] = joined_chunk['wday']
        joined_chunk['month'] = joined_chunk['month']
        joined_chunk['year'] = joined_chunk['year']
        
        # Save chunk immediately
        if first_chunk:
            joined_chunk.to_csv(output_file, index=False, mode='w')
            first_chunk = False
        else:
            joined_chunk.to_csv(output_file, index=False, mode='a', header=False)
        
        total_rows += len(joined_chunk)
        print(f"Chunk {chunk_count}: {len(joined_chunk)} rows, Total: {total_rows}")
        
        # Clear memory immediately
        del chunk, melted_chunk, joined_chunk
        
        # Stop after a few chunks for testing
        if chunk_count >= 5:
            print("Stopping after 5 chunks for testing...")
            break
    
    print(f"Processing complete! Total rows: {total_rows}")
    return output_file

if __name__ == "__main__":
    output_file = join_m5_data_basic(chunk_size=5)  # Very small chunks
    print(f"Data saved to: {output_file}")
    
    # Show sample of results
    if os.path.exists(output_file):
        sample = pd.read_csv(output_file, nrows=5)
        print("\nSample of joined data:")
        print(sample.head())
        print(f"\nColumns: {sample.columns.tolist()}")
