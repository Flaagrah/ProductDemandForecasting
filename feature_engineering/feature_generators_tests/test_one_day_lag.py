"""
Test file for the OneDayLag feature generator.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from feature_generators.one_day_lag import OneDayLag
import pandas as pd


def test_generate_features():
    """
    Test function for the OneDayLag generate_features method.
    """
    # Create sample test data
    test_data = pd.DataFrame({
        'store_id': ['CA_1', 'CA_1', 'CA_1', 'CA_1', 'TX_1', 'TX_1', 'TX_1'],
        'item_id': ['FOODS_1_001', 'FOODS_1_001', 'FOODS_1_001', 'FOODS_1_001', 'FOODS_1_002', 'FOODS_1_002', 'FOODS_1_002'],
        'date': ['2011-01-01', '2011-01-02', '2011-01-03', '2011-01-04', '2011-01-01', '2011-01-02', '2011-01-03'],
        'sales': [10, 15, 20, 25, 5, 8, 12]
    })
    
    # Create sample feature set
    feature_set = pd.DataFrame({
        'store_id': ['CA_1', 'CA_1', 'TX_1'],
        'item_id': ['FOODS_1_001', 'FOODS_1_001', 'FOODS_1_002'],
        'date': ['2011-01-02', '2011-01-03', '2011-01-02']
    })
    
    # Initialize the feature generator
    field_mapping = {
        'store_id': 'store_id',
        'item_id': 'item_id',
        'date': 'date',
        'sales': 'sales'
    }
    
    one_day_lag_gen = OneDayLag(field_name_mapping=field_mapping, data=test_data)
    
    # Test the generate_features function
    result = one_day_lag_gen.generate_features(test_data, feature_set=feature_set)
    
    # Print results for verification
    print("Test Results:")
    print("Original feature_set:")
    print(feature_set)
    print("\nResult with one_day_lag column:")
    print(result)
    
    # Verify the results
    expected_values = [10, 15, 5]  # Previous day sales for each row
    
    print("\nVerification:")
    # The base class method creates a column named '1_day_lag_sum'
    lag_column = '1_day_lag_sum'
    for i, expected in enumerate(expected_values):
        actual = result[lag_column].iloc[i]
        print(f"Row {i}: Expected {expected}, Got {actual}, Match: {actual == expected}")
    
    # Test with empty feature_set
    empty_result = one_day_lag_gen.generate_features(test_data, feature_set=None)
    print(f"\nEmpty feature_set result shape: {empty_result.shape}")
    print(f"Empty feature_set columns: {list(empty_result.columns)}")
    
    return result


if __name__ == "__main__":
    test_generate_features()
