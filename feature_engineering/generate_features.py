"""
Main feature engineering script that applies all feature generators to joined_data_daily.csv
and creates data_with_features.csv with all the generated features.
"""

import pandas as pd
import os
import sys
import time
from typing import Dict, List

# Add the feature_generators directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'feature_generators'))

# Import all feature generators
from feature_generators.one_day_lag import OneDayLag
from feature_generators.two_day_lag import TwoDayLag
from feature_generators.four_day_lag import FourDayLag
from feature_generators.eight_day_lag import EightDayLag
from feature_generators.one_week_lag import OneWeekLag
from feature_generators.two_week_lag import TwoWeekLag
from feature_generators.four_week_lag import FourWeekLag
from feature_generators.eight_week_lag import EightWeekLag
from feature_generators.prev_year_week import PrevYearWeek
from feature_generators.prev2_year_week import Prev2YearWeek
from feature_generators.one_month_lag import OneMonthLag
from feature_generators.two_month_lag import TwoMonthLag
from feature_generators.four_month_lag import FourMonthLag
from feature_generators.prev_year_month import PrevYearMonth
from feature_generators.prev2_year_month import Prev2YearMonth
from feature_generators.is_holiday import IsHoliday
from feature_generators.location import Location
from feature_generators.category import Category
from feature_generators.department import Department


def create_field_mapping() -> Dict[str, str]:
    """
    Create the field mapping dictionary for all feature generators.
    
    Returns:
        Dict[str, str]: Mapping of field keys to actual column names in the data
    """
    return {
        'store_id': 'store_id',
        'item_id': 'item_id',
        'date': 'date',
        'sales': 'sales',
        'department': 'dept_id',
        'category': 'cat_id',
        'location': 'state_id',
        'holiday': 'event_name_1'  # Assuming holiday info is in event_name_1 column
    }


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load the joined data from CSV file with optimized settings.
    
    Args:
        file_path (str): Path to the joined_data_daily.csv file
        
    Returns:
        pd.DataFrame: Loaded data
    """
    print(f"Loading data from {file_path}...")
    
    # Optimize data loading
    data = pd.read_csv(file_path, low_memory=False, dtype={
        'store_id': 'category',
        'item_id': 'category', 
        'dept_id': 'category',
        'cat_id': 'category',
        'state_id': 'category',
        'sales': 'float32'  # Use float32 to save memory
    })
    
    # Convert date column to datetime
    data['date'] = pd.to_datetime(data['date'])
    
    print(f"Loaded {len(data)} rows and {len(data.columns)} columns")
    print(f"Memory usage: {data.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    return data


def apply_feature_generators(data: pd.DataFrame, field_mapping: Dict[str, str]) -> pd.DataFrame:
    """
    Apply all feature generators to the data with progress tracking and error handling.
    
    Args:
        data (pd.DataFrame): Input data
        field_mapping (Dict[str, str]): Field mapping dictionary
        
    Returns:
        pd.DataFrame: Data with all features added
    """
    print("Applying feature generators...")
    
    # Start with the original data
    result_data = data.copy()
    
    # Define all feature generators with their expected processing time
    feature_generators = [
        # Categorical features (fast)
        (Department(field_mapping, data), "Department"),
        (Category(field_mapping, data), "Category"), 
        (Location(field_mapping, data), "Location"),
        (IsHoliday(field_mapping, data), "IsHoliday"),
        
        # Day-based lag features (medium)
        (OneDayLag(field_mapping, data), "OneDayLag"),
        (TwoDayLag(field_mapping, data), "TwoDayLag"),
        (FourDayLag(field_mapping, data), "FourDayLag"),
        (EightDayLag(field_mapping, data), "EightDayLag"),
        
        # Week-based lag features (slow)
        (OneWeekLag(field_mapping, data), "OneWeekLag"),
        (TwoWeekLag(field_mapping, data), "TwoWeekLag"),
        (FourWeekLag(field_mapping, data), "FourWeekLag"),
        (EightWeekLag(field_mapping, data), "EightWeekLag"),
        
        # Month-based lag features (very slow)
        (OneMonthLag(field_mapping, data), "OneMonthLag"),
        (TwoMonthLag(field_mapping, data), "TwoMonthLag"),
        (FourMonthLag(field_mapping, data), "FourMonthLag"),
        
        # Year-based features (extremely slow)
        (PrevYearWeek(field_mapping, data), "PrevYearWeek"),
        (Prev2YearWeek(field_mapping, data), "Prev2YearWeek"),
        (PrevYearMonth(field_mapping, data), "PrevYearMonth"),
        (Prev2YearMonth(field_mapping, data), "Prev2YearMonth"),
    ]
    
    # Apply each feature generator with progress tracking
    successful_features = 0
    failed_features = 0
    
    for i, (generator, generator_name) in enumerate(feature_generators):
        start_time = time.time()
        
        try:
            print(f"\n[{i+1}/{len(feature_generators)}] Applying {generator_name}...")
            
            # Generate features for the entire dataset
            result_data = generator.generate_features(data, result_data)
            
            elapsed_time = time.time() - start_time
            print(f"    ✓ {generator_name} completed successfully in {elapsed_time:.2f}s")
            successful_features += 1
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            print(f"    ✗ {generator_name} failed after {elapsed_time:.2f}s: {str(e)}")
            failed_features += 1
            # Continue with other generators even if one fails
    
    print(f"\nFeature generation summary:")
    print(f"  ✓ Successful: {successful_features}")
    print(f"  ✗ Failed: {failed_features}")
    print(f"  Total features added: {len(result_data.columns) - len(data.columns)}")
    
    return result_data


def save_features(data: pd.DataFrame, output_path: str) -> None:
    """
    Save the data with features to a CSV file with compression.
    
    Args:
        data (pd.DataFrame): Data with features
        output_path (str): Output file path
    """
    print(f"Saving data with features to {output_path}...")
    
    # Save with compression to reduce file size
    data.to_csv(output_path, index=False, compression='gzip')
    
    # Also save uncompressed version for easier access
    uncompressed_path = output_path.replace('.csv', '_uncompressed.csv')
    data.to_csv(uncompressed_path, index=False)
    
    print(f"Saved {len(data)} rows and {len(data.columns)} columns")
    print(f"Compressed file: {output_path}")
    print(f"Uncompressed file: {uncompressed_path}")


def main():
    """
    Main function to run the feature engineering pipeline.
    """
    print("=" * 60)
    print("FEATURE ENGINEERING PIPELINE")
    print("=" * 60)
    
    # Define file paths
    input_file = "../m5_dataset/joined_data_daily.csv"
    output_file = "data_with_features.csv"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found!")
        return
    
    try:
        start_time = time.time()
        
        # Step 1: Load data
        data = load_data(input_file)
        
        # Step 2: Create field mapping
        field_mapping = create_field_mapping()
        
        # Step 3: Apply feature generators
        data_with_features = apply_feature_generators(data, field_mapping)
        
        # Step 4: Save results
        save_features(data_with_features, output_file)
        
        total_time = time.time() - start_time
        
        print("=" * 60)
        print("FEATURE ENGINEERING COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"Original data: {len(data)} rows, {len(data.columns)} columns")
        print(f"With features: {len(data_with_features)} rows, {len(data_with_features.columns)} columns")
        print(f"Added {len(data_with_features.columns) - len(data.columns)} new feature columns")
        print(f"Total processing time: {total_time:.2f} seconds ({total_time/60:.2f} minutes)")
        print(f"Output saved to: {output_file}")
        
    except Exception as e:
        print(f"Error during feature engineering: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
