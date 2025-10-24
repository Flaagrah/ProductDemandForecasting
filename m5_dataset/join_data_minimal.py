import pandas as pd
import numpy as np
import os

def join_m5_data_minimal(output_file='joined_data_minimal.csv', max_weeks=2):
    """
    Minimal join that processes only a few weeks to avoid memory issues.
    """
    
    print("Loading calendar and prices data...")
    calendar = pd.read_csv('calendar.csv')
    prices = pd.read_csv('sell_prices.csv')
    
    # Join calendar with prices
    calendar_prices = calendar.merge(prices, on='wm_yr_wk', how='left')
    print(f"Calendar-prices shape: {calendar_prices.shape}")
    
    # Process sales data
    print("Loading sales subset...")
    sales = pd.read_csv('sales_train_validation_subset.csv')
    print(f"Sales shape: {sales.shape}")
    
    # Get only first few weekly columns to limit data size
    w_columns = [f'w_{i}' for i in range(1, max_weeks + 1)]
    id_columns = ['id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id']
    
    print(f"Processing only {len(w_columns)} weeks: {w_columns}")
    
    # Melt the sales data
    melted_sales = pd.melt(
        sales, 
        id_vars=id_columns,
        value_vars=w_columns,
        var_name='week',
        value_name='weekly_sales'
    )
    
    # Convert week to integer
    melted_sales['week'] = melted_sales['week'].str.replace('w_', '').astype(int)
    
    # Create week mapping from calendar data
    calendar_prices['week'] = ((calendar_prices['d'].str.replace('d_', '').astype(int) - 1) // 7) + 1
    
    print(f"Melted sales shape: {melted_sales.shape}")
    
    # Join with calendar_prices
    print("Joining data...")
    joined_data = melted_sales.merge(
        calendar_prices, 
        left_on=['store_id', 'item_id', 'week'], 
        right_on=['store_id', 'item_id', 'week'], 
        how='left'
    )
    
    # Add features
    joined_data['day_of_week'] = joined_data['wday']
    joined_data['month'] = joined_data['month']
    joined_data['year'] = joined_data['year']
    
    print(f"Final joined data shape: {joined_data.shape}")
    
    # Save to CSV
    print(f"Saving to {output_file}...")
    joined_data.to_csv(output_file, index=False)
    
    print(f"Processing complete! Total rows: {len(joined_data)}")
    return output_file

if __name__ == "__main__":
    output_file = join_m5_data_minimal(max_weeks=2)  # Only 2 weeks
    print(f"Data saved to: {output_file}")
    
    # Show sample of results
    if os.path.exists(output_file):
        sample = pd.read_csv(output_file, nrows=10)
        print("\nSample of joined data:")
        print(sample.head())
        print(f"\nColumns: {sample.columns.tolist()}")
        print(f"\nTotal rows: {len(pd.read_csv(output_file))}")
