"""
Test file for the TwoMonthLag feature generator.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from feature_generators.two_month_lag import TwoMonthLag
import pandas as pd


def test_generate_features():
    """
    Test the generate_features function of TwoMonthLag.
    """
    # Create test data
    test_data = pd.DataFrame({
        'store_id': ['CA_1'] * 66,
        'item_id': ['FOODS_1'] * 66,
        'date': [f'2011-01-{i:02d}' for i in range(1, 32)] + 
                [f'2011-02-{i:02d}' for i in range(1, 29)] + 
                [f'2011-03-{i:02d}' for i in range(1, 7)],
        'sales': [i * 1.5 for i in range(1, 67)]  # 1.5, 3, 4.5, ..., 99
    })
    
    # Create feature set
    feature_set = pd.DataFrame({
        'store_id': ['CA_1', 'CA_1', 'CA_1'],
        'item_id': ['FOODS_1', 'FOODS_1', 'FOODS_1'],
        'date': ['2011-03-01', '2011-03-02', '2011-03-03']
    })
    
    # Field mapping
    field_mapping = {
        'store_id': 'store_id',
        'item_id': 'item_id',
        'date': 'date',
        'sales': 'sales'
    }
    
    # Test the feature generator
    two_month_lag_gen = TwoMonthLag(field_name_mapping=field_mapping, data=test_data)
    result = two_month_lag_gen.generate_features(test_data, feature_set=feature_set)
    
    print("TwoMonthLag Test Results:")
    print(f"Result shape: {result.shape}")
    print(f"Result columns: {list(result.columns)}")
    print(f"Result:\n{result}")
    
    # Expected values: average of 1, 2, 3, ..., 60-day lag
    # Row 0 (2011-03-01): avg of sales from 2011-01-01 to 2011-02-28 = (1.5+3+4.5+...+90)/60 = 45.75
    # Row 1 (2011-03-02): avg of sales from 2011-01-02 to 2011-03-01 = (3+4.5+6+...+91.5)/60 = 47.25
    # Row 2 (2011-03-03): avg of sales from 2011-01-03 to 2011-03-02 = (4.5+6+7.5+...+93)/60 = 48.75
    expected_values = [45.75, 47.25, 48.75]
    lag_column = 'lag_sum_1_2_3_4_5_6_7_8_9_10_11_12_13_14_15_16_17_18_19_20_21_22_23_24_25_26_27_28_29_30_31_32_33_34_35_36_37_38_39_40_41_42_43_44_45_46_47_48_49_50_51_52_53_54_55_56_57_58_59_60_days'
    
    for i, expected in enumerate(expected_values):
        actual = result[lag_column].iloc[i]
        print(f"Row {i}: Expected {expected}, Got {actual}, Match: {abs(actual - expected) < 0.01}")
    
    # Test with empty feature_set
    empty_result = two_month_lag_gen.generate_features(test_data, feature_set=None)
    print(f"\nEmpty feature_set result shape: {empty_result.shape}")
    print(f"Empty feature_set columns: {list(empty_result.columns)}")
    
    return result


if __name__ == "__main__":
    test_generate_features()
