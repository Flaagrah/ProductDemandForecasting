"""
Test file for the OneWeekLag feature generator.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from feature_generators.one_week_lag import OneWeekLag
import pandas as pd


def test_generate_features():
    """
    Test the generate_features function of OneWeekLag.
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
        'date': ['2011-01-08', '2011-01-09', '2011-01-10']
    })
    
    # Field mapping
    field_mapping = {
        'store_id': 'store_id',
        'item_id': 'item_id',
        'date': 'date',
        'sales': 'sales'
    }
    
    # Test the feature generator
    one_week_lag_gen = OneWeekLag(field_name_mapping=field_mapping, data=test_data)
    result = one_week_lag_gen.generate_features(test_data, feature_set=feature_set)
    
    print("OneWeekLag Test Results:")
    print(f"Result shape: {result.shape}")
    print(f"Result columns: {list(result.columns)}")
    print(f"Result:\n{result}")
    
    # Expected values: average of 1, 2, 3, 4, 5, 6, and 7-day lag
    # Row 0 (2011-01-08): avg of sales from 2011-01-01 to 2011-01-07 = (10+15+20+25+30+35+40)/7 = 26.43
    # Row 1 (2011-01-09): avg of sales from 2011-01-02 to 2011-01-08 = (15+20+25+30+35+40+45)/7 = 30.0
    # Row 2 (2011-01-10): avg of sales from 2011-01-03 to 2011-01-09 = (20+25+30+35+40+45+50)/7 = 33.57
    expected_values = [26.43, 30.0, 33.57]
    lag_column = 'lag_sum_1_2_3_4_5_6_7_days'
    
    for i, expected in enumerate(expected_values):
        actual = result[lag_column].iloc[i]
        print(f"Row {i}: Expected {expected:.2f}, Got {actual:.2f}, Match: {abs(actual - expected) < 0.01}")
    
    # Test with empty feature_set
    empty_result = one_week_lag_gen.generate_features(test_data, feature_set=None)
    print(f"\nEmpty feature_set result shape: {empty_result.shape}")
    print(f"Empty feature_set columns: {list(empty_result.columns)}")
    
    return result


if __name__ == "__main__":
    test_generate_features()
