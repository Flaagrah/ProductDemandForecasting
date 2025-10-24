"""
Test file for the PrevYearMonth feature generator.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from feature_generators.prev_year_month import PrevYearMonth
import pandas as pd


def test_generate_features():
    """
    Test the generate_features function of PrevYearMonth.
    """
    # Create test data spanning multiple years
    test_data = pd.DataFrame({
        'store_id': ['CA_1'] * 100,
        'item_id': ['FOODS_1'] * 100,
        'date': [f'2010-01-{i:02d}' for i in range(1, 32)] +  # Jan 2010
                [f'2010-02-{i:02d}' for i in range(1, 29)] +  # Feb 2010
                [f'2011-01-{i:02d}' for i in range(1, 32)] +  # Jan 2011
                [f'2011-02-{i:02d}' for i in range(1, 8)],   # Feb 2011 (partial)
        'sales': [i * 2 for i in range(1, 101)]  # 2, 4, 6, ..., 200
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
    prev_year_month_gen = PrevYearMonth(field_name_mapping=field_mapping, data=test_data)
    result = prev_year_month_gen.generate_features(test_data, feature_set=feature_set)
    
    print("PrevYearMonth Test Results:")
    print(f"Result shape: {result.shape}")
    print(f"Result columns: {list(result.columns)}")
    print(f"Result:\n{result}")
    
    # Expected values: average of sales from same month in previous year (335-365 days ago)
    # Row 0 (2011-01-15): avg of sales from 2010-01-15 to 2010-01-31 = (30+32+34+...+62)/17 = 46.0
    # Row 1 (2011-01-16): avg of sales from 2010-01-16 to 2010-02-01 = (32+34+36+...+64)/17 = 48.0
    # Row 2 (2011-01-17): avg of sales from 2010-01-17 to 2010-02-02 = (34+36+38+...+66)/17 = 50.0
    expected_values = [46.0, 48.0, 50.0]
    lag_column = 'lag_sum_335_336_337_338_339_340_341_342_343_344_345_346_347_348_349_350_351_352_353_354_355_356_357_358_359_360_361_362_363_364_days'
    
    for i, expected in enumerate(expected_values):
        actual = result[lag_column].iloc[i]
        print(f"Row {i}: Expected {expected}, Got {actual}, Match: {abs(actual - expected) < 0.01}")
    
    # Test with empty feature_set
    empty_result = prev_year_month_gen.generate_features(test_data, feature_set=None)
    print(f"\nEmpty feature_set result shape: {empty_result.shape}")
    print(f"Empty feature_set columns: {list(empty_result.columns)}")
    
    return result


if __name__ == "__main__":
    test_generate_features()
