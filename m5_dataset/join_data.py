import pandas as pd
import numpy as np
import os
import dask.dataframe as dd
from dask.diagnostics import ProgressBar

def join_m5_data_dask(output_file='joined_data_daily.csv', chunk_size='32MB'):
    """
    Joins calendar.csv, sales_train_validation_subset.csv, and sell_prices.csv data using Dask.
    
    Joins:
    1. Calendar to sell_prices based on wm_yr_wk
    2. Calendar d column to appropriate d columns in sales_train_validation_subset
    
    Args:
        output_file (str): Output CSV file name
        chunk_size (str): Chunk size for reading large files (e.g., '32MB', '64MB')
    
    Returns:
        str: Path to the output file
    """
    
    print("Loading data files with Dask...")
    
    # Load the datasets with Dask
    # Specify dtypes for calendar to avoid inference issues
    calendar_dtypes = {
        'date': 'string',
        'wm_yr_wk': 'int64',
        'weekday': 'string',
        'wday': 'int64',
        'month': 'int64',
        'year': 'int64',
        'd': 'string',
        'event_name_1': 'string',
        'event_type_1': 'string', 
        'event_name_2': 'string',
        'event_type_2': 'string',
        'snap_CA': 'int64',
        'snap_TX': 'int64',
        'snap_WI': 'int64'
    }
    calendar = dd.read_csv('calendar.csv', dtype=calendar_dtypes)
    sales = dd.read_csv('sales_train_validation_subset.csv', blocksize=chunk_size)
    prices = dd.read_csv('sell_prices_subset.csv', blocksize=chunk_size)
    
    print(f"Calendar shape: {calendar.shape}")
    print(f"Sales shape: {sales.shape}")
    print(f"Prices shape: {prices.shape}")
    
    # Step 1: Join calendar with sell_prices on wm_yr_wk
    print("Joining calendar with sell_prices on wm_yr_wk...")
    calendar_prices = calendar.merge(prices, on='wm_yr_wk', how='left')
    print(f"Calendar-prices shape: {calendar_prices.shape}")
    
    # Step 2: Melt sales data from wide to long format
    print("Melting sales data...")
    
    # Get daily columns
    d_columns = [col for col in sales.columns if col.startswith('d_')]
    id_columns = ['id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id']
    
    print(f"Found {len(d_columns)} daily columns")
    print(f"ID columns: {id_columns}")
    
    # Melt the sales data
    melted_sales = sales.melt(
        id_vars=id_columns,
        value_vars=d_columns,
        var_name='d',
        value_name='sales'
    )
    
    # Convert d to integer for joining
    melted_sales['d'] = melted_sales['d'].str.replace('d_', '').astype(int)
    
    # Ensure calendar_prices d column is also integer for consistent joining
    # Calendar d column has format 'd_8', so we need to extract the number
    calendar_prices['d'] = calendar_prices['d'].str.replace('d_', '').astype(int)
    
    print(f"Melted sales shape: {melted_sales.shape}")
    
    # Step 3: Join melted sales with calendar_prices
    print("Joining melted sales with calendar_prices...")
    final_data = melted_sales.merge(
        calendar_prices, 
        left_on=['store_id', 'item_id', 'd'], 
        right_on=['store_id', 'item_id', 'd'], 
        how='left'
    )
    
    print(f"Final joined data shape: {final_data.shape}")
    
    # Add some basic features
    final_data['day_of_week'] = final_data['wday']
    final_data['month'] = final_data['month']
    final_data['year'] = final_data['year']
    
    # Save to CSV with progress bar and minimal disk usage
    print(f"Saving joined data to {output_file}...")
    
    # Configure Dask to use less disk space
    import dask
    dask.config.set({'temporary-directory': './temp'})  # Use local temp directory
    
    with ProgressBar():
        final_data.to_csv(output_file, index=False, single_file=True)
    
    print(f"Data processing complete!")
    print(f"Output saved to: {output_file}")
    
    return output_file

def get_sample_data(n_rows=1000):
    """
    Get a sample of the joined data for inspection.
    
    Args:
        n_rows (int): Number of rows to return
    
    Returns:
        pd.DataFrame: Sample of joined data
    """
    if os.path.exists('joined_data_daily.csv'):
        return pd.read_csv('joined_data_daily.csv', nrows=n_rows)
    else:
        print("No joined data file found. Run join_m5_data_dask() first.")
        return None

if __name__ == "__main__":
    # Example usage
    print("Creating joined M5 dataset using Dask...")
    output_file = join_m5_data_dask(chunk_size='16MB')  # Smaller chunks for testing
    
    print(f"\nJoined data saved to: {output_file}")
    
    # Load a sample to show structure
    print("\nLoading sample to show data structure...")
    sample_data = get_sample_data(1000)
    
    if sample_data is not None:
        print("\nFirst few rows of joined data:")
        print(sample_data.head())
        
        print("\nColumn names:")
        print(sample_data.columns.tolist())
        
        print(f"\nSample data shape: {sample_data.shape}")
    else:
        print("No sample data available.")