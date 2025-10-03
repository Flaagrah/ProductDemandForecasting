"""
Feature configuration dictionary for demand forecasting features.

This module contains a dictionary with feature names as keys and None as values.
The None values can be replaced with configuration parameters or feature specifications
as needed by specific feature generators.
"""

FEATURE_CONFIG = {
    # Monthly lag features
    "one_month_lag": None,
    "two_month_lag": None,
    "four_month_lag": None,
    "prev_year_month": None,
    "prev2_year_month": None,
    
    # Weekly lag features
    "one_week_lag": None,
    "two_week_lag": None,
    "four_week_lag": None,
    "eight_week_lag": None,
    "prev_year_week": None,
    "prev2_year_week": None,
    
    # Daily lag features
    "one_day_lag": None,
    "two_day_lag": None,
    "four_day_lag": None,
    "eight_day_lag": None,
    
    # Event and categorical features
    "is_holiday": None,
    "location": None,
    "category": None,
    "department": None,
    "store": None,
    "product": None,

    # Date features
    "date": None,

    # Sales features
    "sales": None,
}
