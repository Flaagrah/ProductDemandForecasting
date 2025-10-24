"""
Test file for the Prev2YearWeek feature generator.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from feature_generators.prev2_year_week import Prev2YearWeek
import pandas as pd


def test_generate_features():
    """
    Test the generate_features function of Prev2YearWeek.
    """
    # Create test data spanning multiple years
    test_data = pd.DataFrame({
        'store_id': ['CA_1'] * 150,
        'item_id': ['FOODS_1'] * 150,
        'date': [f'2009-01-{i:02d}' for i in range(1, 32)] +  # Jan 2009
                [f'2009-02-{i:02d}' for i in range(1, 29)] +  # Feb 2009
                [f'2010-01-{i:02d}' for i in range(1, 32)] +  # Jan 2010
                [f'2010-02-{i:02d}' for i in range(1, 29)] +  # Feb 2010
                [f'2011-01-{i:02d}' for i in range(1, 32)] +  # Jan 2011
                [f'2011-02-{i:02d}' for i in range(1, 6)],   # Feb 2011 (partial)
        'sales': [i * 1.5 for i in range(1, 151)]  # 1.5, 3, 4.5, ..., 225
    })
    
    # Create feature set for 2011 dates
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
    prev2_year_week_gen = Prev2YearWeek(field_name_mapping=field_mapping, data=test_data)
    result = prev2_year_week_gen.generate_features(test_data, feature_set=feature_set)
    
    print("Prev2YearWeek Test Results:")
    print(f"Result shape: {result.shape}")
    print(f"Result columns: {list(result.columns)}")
    print(f"Result:\n{result}")
    
    # Expected values: average of sales from same week two years ago (104 weeks = 728 days ago)
    # Row 0 (2011-01-15): avg of sales from 2009-01-15 (22.5) = 22.5
    # Row 1 (2011-01-16): avg of sales from 2009-01-16 (24.0) = 24.0
    # Row 2 (2011-01-17): avg of sales from 2009-01-17 (25.5) = 25.5
    expected_values = [22.5, 24.0, 25.5]
    lag_column = '728_day_lag_sum'
    
    for i, expected in enumerate(expected_values):
        actual = result[lag_column].iloc[i]
        print(f"Row {i}: Expected {expected}, Got {actual}, Match: {actual == expected}")
    
    # Test with empty feature_set
    empty_result = prev2_year_week_gen.generate_features(test_data, feature_set=None)
    print(f"\nEmpty feature_set result shape: {empty_result.shape}")
    print(f"Empty feature_set columns: {list(empty_result.columns)}")
    
    return result


if __name__ == "__main__":
    test_generate_features()
