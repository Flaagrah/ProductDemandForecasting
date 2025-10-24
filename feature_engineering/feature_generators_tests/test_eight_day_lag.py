"""
Test file for the EightDayLag feature generator.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from feature_generators.eight_day_lag import EightDayLag
import pandas as pd


def test_generate_features():
    """
    Test the generate_features function of EightDayLag.
    """
    # Create test data
    test_data = pd.DataFrame({
        'store_id': ['CA_1'] * 10,
        'item_id': ['FOODS_1'] * 10,
        'date': [f'2011-01-{i:02d}' for i in range(1, 11)],
        'sales': [10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
    })
    
    # Create feature set
    feature_set = pd.DataFrame({
        'store_id': ['CA_1', 'CA_1', 'CA_1'],
        'item_id': ['FOODS_1', 'FOODS_1', 'FOODS_1'],
        'date': ['2011-01-09', '2011-01-10', '2011-01-11']
    })
    
    # Field mapping
    field_mapping = {
        'store_id': 'store_id',
        'item_id': 'item_id',
        'date': 'date',
        'sales': 'sales'
    }
    
    # Test the feature generator
    eight_day_lag_gen = EightDayLag(field_name_mapping=field_mapping, data=test_data)
    result = eight_day_lag_gen.generate_features(test_data, feature_set=feature_set)
    
    print("EightDayLag Test Results:")
    print(f"Result shape: {result.shape}")
    print(f"Result columns: {list(result.columns)}")
    print(f"Result:\n{result}")
    
    # Expected values: average of 1, 2, 3, 4, 5, 6, 7, and 8-day lag
    # Row 0 (2011-01-09): avg of sales from 2011-01-01 to 2011-01-08 = (10+15+20+25+30+35+40+45)/8 = 27.5
    # Row 1 (2011-01-10): avg of sales from 2011-01-02 to 2011-01-09 = (15+20+25+30+35+40+45+50)/8 = 32.5
    # Row 2 (2011-01-11): avg of sales from 2011-01-03 to 2011-01-10 = (20+25+30+35+40+45+50+55)/8 = 37.5
    expected_values = [27.5, 32.5, 37.5]
    lag_column = 'lag_sum_1_2_3_4_5_6_7_8_days'
    
    for i, expected in enumerate(expected_values):
        actual = result[lag_column].iloc[i]
        print(f"Row {i}: Expected {expected}, Got {actual}, Match: {actual == expected}")
    
    # Test with empty feature_set
    empty_result = eight_day_lag_gen.generate_features(test_data, feature_set=None)
    print(f"\nEmpty feature_set result shape: {empty_result.shape}")
    print(f"Empty feature_set columns: {list(empty_result.columns)}")
    
    return result


if __name__ == "__main__":
    test_generate_features()
