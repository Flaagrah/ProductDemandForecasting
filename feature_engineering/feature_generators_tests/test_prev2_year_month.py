"""
Test file for the Prev2YearMonth feature generator.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from feature_generators.prev2_year_month import Prev2YearMonth
import pandas as pd


def test_generate_features():
    """
    Test the generate_features function of Prev2YearMonth.
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
    prev2_year_month_gen = Prev2YearMonth(field_name_mapping=field_mapping, data=test_data)
    result = prev2_year_month_gen.generate_features(test_data, feature_set=feature_set)
    
    print("Prev2YearMonth Test Results:")
    print(f"Result shape: {result.shape}")
    print(f"Result columns: {list(result.columns)}")
    print(f"Result:\n{result}")
    
    # Expected values: average of sales from same month two years ago (700-729 days ago)
    # Row 0 (2011-01-15): avg of sales from 2009-01-15 to 2009-01-31 = (22.5+24+25.5+...+46.5)/17 = 34.5
    # Row 1 (2011-01-16): avg of sales from 2009-01-16 to 2009-02-01 = (24+25.5+27+...+48)/17 = 36.0
    # Row 2 (2011-01-17): avg of sales from 2009-01-17 to 2009-02-02 = (25.5+27+28.5+...+49.5)/17 = 37.5
    expected_values = [34.5, 36.0, 37.5]
    lag_column = 'lag_sum_700_701_702_703_704_705_706_707_708_709_710_711_712_713_714_715_716_717_718_719_720_721_722_723_724_725_726_727_728_729_days'
    
    for i, expected in enumerate(expected_values):
        actual = result[lag_column].iloc[i]
        print(f"Row {i}: Expected {expected}, Got {actual}, Match: {abs(actual - expected) < 0.01}")
    
    # Test with empty feature_set
    empty_result = prev2_year_month_gen.generate_features(test_data, feature_set=None)
    print(f"\nEmpty feature_set result shape: {empty_result.shape}")
    print(f"Empty feature_set columns: {list(empty_result.columns)}")
    
    return result


if __name__ == "__main__":
    test_generate_features()
