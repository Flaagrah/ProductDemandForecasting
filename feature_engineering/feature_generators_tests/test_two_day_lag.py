"""
Test file for the TwoDayLag feature generator.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from feature_generators.two_day_lag import TwoDayLag
import pandas as pd


def test_generate_features():
    """
    Test the generate_features function of TwoDayLag.
    """
    # Create test data
    test_data = pd.DataFrame({
        'store_id': ['CA_1', 'CA_1', 'CA_1', 'CA_1', 'CA_1'],
        'item_id': ['FOODS_1', 'FOODS_1', 'FOODS_1', 'FOODS_1', 'FOODS_1'],
        'date': ['2011-01-01', '2011-01-02', '2011-01-03', '2011-01-04', '2011-01-05'],
        'sales': [10, 15, 20, 25, 30]
    })
    
    # Create feature set
    feature_set = pd.DataFrame({
        'store_id': ['CA_1', 'CA_1', 'CA_1'],
        'item_id': ['FOODS_1', 'FOODS_1', 'FOODS_1'],
        'date': ['2011-01-03', '2011-01-04', '2011-01-05']
    })
    
    # Field mapping
    field_mapping = {
        'store_id': 'store_id',
        'item_id': 'item_id',
        'date': 'date',
        'sales': 'sales'
    }
    
    # Test the feature generator
    two_day_lag_gen = TwoDayLag(field_name_mapping=field_mapping, data=test_data)
    result = two_day_lag_gen.generate_features(test_data, feature_set=feature_set)
    
    print("TwoDayLag Test Results:")
    print(f"Result shape: {result.shape}")
    print(f"Result columns: {list(result.columns)}")
    print(f"Result:\n{result}")
    
    # Expected values: average of 1-day and 2-day lag
    # Row 0 (2011-01-03): avg of sales from 2011-01-01 (10) and 2011-01-02 (15) = 12.5
    # Row 1 (2011-01-04): avg of sales from 2011-01-02 (15) and 2011-01-03 (20) = 17.5
    # Row 2 (2011-01-05): avg of sales from 2011-01-03 (20) and 2011-01-04 (25) = 22.5
    expected_values = [12.5, 17.5, 22.5]
    lag_column = 'lag_sum_1_2_days'
    
    for i, expected in enumerate(expected_values):
        actual = result[lag_column].iloc[i]
        print(f"Row {i}: Expected {expected}, Got {actual}, Match: {actual == expected}")
    
    # Test with empty feature_set
    empty_result = two_day_lag_gen.generate_features(test_data, feature_set=None)
    print(f"\nEmpty feature_set result shape: {empty_result.shape}")
    print(f"Empty feature_set columns: {list(empty_result.columns)}")
    
    return result


if __name__ == "__main__":
    test_generate_features()
