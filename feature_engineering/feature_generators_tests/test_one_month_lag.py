"""
Test file for the OneMonthLag feature generator.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from feature_generators.one_month_lag import OneMonthLag
import pandas as pd


def test_generate_features():
    """
    Test the generate_features function of OneMonthLag.
    """
    # Create test data
    test_data = pd.DataFrame({
        'store_id': ['CA_1'] * 39,
        'item_id': ['FOODS_1'] * 39,
        'date': [f'2011-01-{i:02d}' for i in range(1, 32)] + [f'2011-02-{i:02d}' for i in range(1, 9)],
        'sales': [i * 2 for i in range(1, 40)]  # 2, 4, 6, ..., 78
    })
    
    # Create feature set
    feature_set = pd.DataFrame({
        'store_id': ['CA_1', 'CA_1', 'CA_1'],
        'item_id': ['FOODS_1', 'FOODS_1', 'FOODS_1'],
        'date': ['2011-02-01', '2011-02-02', '2011-02-03']
    })
    
    # Field mapping
    field_mapping = {
        'store_id': 'store_id',
        'item_id': 'item_id',
        'date': 'date',
        'sales': 'sales'
    }
    
    # Test the feature generator
    one_month_lag_gen = OneMonthLag(field_name_mapping=field_mapping, data=test_data)
    result = one_month_lag_gen.generate_features(test_data, feature_set=feature_set)
    
    print("OneMonthLag Test Results:")
    print(f"Result shape: {result.shape}")
    print(f"Result columns: {list(result.columns)}")
    print(f"Result:\n{result}")
    
    # Expected values: average of 1, 2, 3, ..., 31-day lag
    # Row 0 (2011-02-01): avg of sales from 2011-01-01 to 2011-01-31 = (2+4+6+...+62)/31 = 32.0
    # Row 1 (2011-02-02): avg of sales from 2011-01-02 to 2011-02-01 = (4+6+8+...+64)/31 = 34.0
    # Row 2 (2011-02-03): avg of sales from 2011-01-03 to 2011-02-02 = (6+8+10+...+66)/31 = 36.0
    expected_values = [32.0, 34.0, 36.0]
    lag_column = 'lag_sum_1_2_3_4_5_6_7_8_9_10_11_12_13_14_15_16_17_18_19_20_21_22_23_24_25_26_27_28_29_30_31_days'
    
    for i, expected in enumerate(expected_values):
        actual = result[lag_column].iloc[i]
        print(f"Row {i}: Expected {expected}, Got {actual}, Match: {actual == expected}")
    
    # Test with empty feature_set
    empty_result = one_month_lag_gen.generate_features(test_data, feature_set=None)
    print(f"\nEmpty feature_set result shape: {empty_result.shape}")
    print(f"Empty feature_set columns: {list(empty_result.columns)}")
    
    return result


if __name__ == "__main__":
    test_generate_features()
