"""
Test file for the FourDayLag feature generator.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from feature_generators.four_day_lag import FourDayLag
import pandas as pd


def test_generate_features():
    """
    Test the generate_features function of FourDayLag.
    """
    # Create test data
    test_data = pd.DataFrame({
        'store_id': ['CA_1', 'CA_1', 'CA_1', 'CA_1', 'CA_1', 'CA_1', 'CA_1'],
        'item_id': ['FOODS_1', 'FOODS_1', 'FOODS_1', 'FOODS_1', 'FOODS_1', 'FOODS_1', 'FOODS_1'],
        'date': ['2011-01-01', '2011-01-02', '2011-01-03', '2011-01-04', '2011-01-05', '2011-01-06', '2011-01-07'],
        'sales': [10, 15, 20, 25, 30, 35, 40]
    })
    
    # Create feature set
    feature_set = pd.DataFrame({
        'store_id': ['CA_1', 'CA_1', 'CA_1'],
        'item_id': ['FOODS_1', 'FOODS_1', 'FOODS_1'],
        'date': ['2011-01-05', '2011-01-06', '2011-01-07']
    })
    
    # Field mapping
    field_mapping = {
        'store_id': 'store_id',
        'item_id': 'item_id',
        'date': 'date',
        'sales': 'sales'
    }
    
    # Test the feature generator
    four_day_lag_gen = FourDayLag(field_name_mapping=field_mapping, data=test_data)
    result = four_day_lag_gen.generate_features(test_data, feature_set=feature_set)
    
    print("FourDayLag Test Results:")
    print(f"Result shape: {result.shape}")
    print(f"Result columns: {list(result.columns)}")
    print(f"Result:\n{result}")
    
    # Expected values: average of 1, 2, 3, and 4-day lag
    # Row 0 (2011-01-05): avg of sales from 2011-01-01 (10), 2011-01-02 (15), 2011-01-03 (20), 2011-01-04 (25) = 17.5
    # Row 1 (2011-01-06): avg of sales from 2011-01-02 (15), 2011-01-03 (20), 2011-01-04 (25), 2011-01-05 (30) = 22.5
    # Row 2 (2011-01-07): avg of sales from 2011-01-03 (20), 2011-01-04 (25), 2011-01-05 (30), 2011-01-06 (35) = 27.5
    expected_values = [17.5, 22.5, 27.5]
    lag_column = 'lag_sum_1_2_3_4_days'
    
    for i, expected in enumerate(expected_values):
        actual = result[lag_column].iloc[i]
        print(f"Row {i}: Expected {expected}, Got {actual}, Match: {actual == expected}")
    
    # Test with empty feature_set
    empty_result = four_day_lag_gen.generate_features(test_data, feature_set=None)
    print(f"\nEmpty feature_set result shape: {empty_result.shape}")
    print(f"Empty feature_set columns: {list(empty_result.columns)}")
    
    return result


if __name__ == "__main__":
    test_generate_features()
