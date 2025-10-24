"""
Test file for the TwoWeekLag feature generator.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from feature_generators.two_week_lag import TwoWeekLag
import pandas as pd


def test_generate_features():
    """
    Test the generate_features function of TwoWeekLag.
    """
    # Create test data
    test_data = pd.DataFrame({
        'store_id': ['CA_1'] * 20,
        'item_id': ['FOODS_1'] * 20,
        'date': [f'2011-01-{i:02d}' for i in range(1, 21)],
        'sales': [i * 5 for i in range(1, 21)]  # 5, 10, 15, ..., 100
    })
    
    # Create feature set
    feature_set = pd.DataFrame({
        'store_id': ['CA_1', 'CA_1', 'CA_1'],
        'item_id': ['FOODS_1', 'FOODS_1', 'FOODS_1'],
        'date': ['2011-01-15', '2011-01-16', '2011-01-17']
    })
    
    # Field mapping
    field_mapping = {
        'store_id': 'store_id',
        'item_id': 'item_id',
        'date': 'date',
        'sales': 'sales'
    }
    
    # Test the feature generator
    two_week_lag_gen = TwoWeekLag(field_name_mapping=field_mapping, data=test_data)
    result = two_week_lag_gen.generate_features(test_data, feature_set=feature_set)
    
    print("TwoWeekLag Test Results:")
    print(f"Result shape: {result.shape}")
    print(f"Result columns: {list(result.columns)}")
    print(f"Result:\n{result}")
    
    # Expected values: average of 1, 2, 3, ..., 14-day lag
    # Row 0 (2011-01-15): avg of sales from 2011-01-01 to 2011-01-14 = (5+10+15+...+70)/14 = 37.5
    # Row 1 (2011-01-16): avg of sales from 2011-01-02 to 2011-01-15 = (10+15+20+...+75)/14 = 42.5
    # Row 2 (2011-01-17): avg of sales from 2011-01-03 to 2011-01-16 = (15+20+25+...+80)/14 = 47.5
    expected_values = [37.5, 42.5, 47.5]
    lag_column = 'lag_sum_1_2_3_4_5_6_7_8_9_10_11_12_13_14_days'
    
    for i, expected in enumerate(expected_values):
        actual = result[lag_column].iloc[i]
        print(f"Row {i}: Expected {expected}, Got {actual}, Match: {actual == expected}")
    
    # Test with empty feature_set
    empty_result = two_week_lag_gen.generate_features(test_data, feature_set=None)
    print(f"\nEmpty feature_set result shape: {empty_result.shape}")
    print(f"Empty feature_set columns: {list(empty_result.columns)}")
    
    return result


if __name__ == "__main__":
    test_generate_features()
