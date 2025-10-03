from abc import ABC, abstractmethod
from typing import Dict


class FeatureGen(ABC):
    """
    Abstract base class for feature generators.
    
    This class provides a common interface for all feature generators
    with a configurable string-to-string mapping dictionary.
    """
    
    def __init__(self, field_name_mapping: Dict[str, str] = None, data=None):
        """
        Initialize the FeatureGen with a string-to-string mapping dictionary and data.
        
        Args:
            field_name_mapping (Dict[str, str], optional): Dictionary mapping strings to strings.
                                               Defaults to empty dictionary if None.
            data: pandas DataFrame containing the data to process
        """
        self.field_name_mapping = field_name_mapping if field_name_mapping is not None else {}
        self.data = data
    
    def get_field_name(self, field_key: str) -> str:
        """
        Get the field name from the mapping for a given key.
        
        Args:
            field_key (str): The key to look up in the mapping
            
        Returns:
            str: The field name from the mapping
            
        Raises:
            ValueError: If the field key is not found in the mapping
        """
        field_name = self.field_name_mapping.get(field_key, None)
        if field_name is None:
            raise ValueError(f"Field name for '{field_key}' not found in mapping")
        return field_name
    
    def get_categorical_feature(self, data, field_key: str):
        """
        Extract categorical feature values from input data.
        
        Args:
            data: Input data containing the feature information
            field_key (str): The key to look up in the mapping for the field name
            
        Returns:
            List of feature values corresponding to each row
        """
        # Get the field name from mapping
        field_name = self.get_field_name(field_key)
        
        # Extract feature values for each row
        if hasattr(data, 'iloc'):  # pandas DataFrame
            feature_values = data[field_name].tolist()
        elif hasattr(data, '__iter__') and not isinstance(data, str):  # list or other iterable
            if isinstance(data[0], dict):  # list of dictionaries
                feature_values = [row.get(field_name) for row in data]
            else:  # list of other objects
                feature_values = [getattr(row, field_name, None) for row in data]
        else:
            # Single value or unsupported type
            feature_values = [getattr(data, field_name, None)]
        
        return feature_values
    
    def filter_data(self, filter_dict: Dict[str, any]):
        """
        Filter the stored data based on column-value pairs.
        
        Args:
            filter_dict (Dict[str, any]): Dictionary where keys are column names and values are the values to filter by
            
        Returns:
            pandas.DataFrame: Filtered dataframe containing only records that match all the specified conditions
            
        Raises:
            ValueError: If no data is stored or if any column in filter_dict doesn't exist
        """
        if self.data is None:
            raise ValueError("No data available. Please provide data when initializing the feature generator.")
        
        if not filter_dict:
            return self.data
        
        # Check if all columns exist in the data
        missing_columns = [col for col in filter_dict.keys() if col not in self.data.columns]
        if missing_columns:
            raise ValueError(f"Columns not found in data: {missing_columns}")
        
        # Apply filters
        filtered_data = self.data.copy()
        for column, value in filter_dict.items():
            filtered_data = filtered_data[filtered_data[column] == value]
        
        return filtered_data
    
    def generate_lag_features_avg(self, data, feature_set=None, timedeltas=None):
        """
        Generate lag features by summing sales across multiple time periods.
        
        Args:
            data: Input data containing sales information
            feature_set (pandas.DataFrame, optional): DataFrame representing the feature set being constructed
            timedeltas (list): List of timedelta objects representing the lag periods
            
        Returns:
            pandas.DataFrame: Feature set with lag sum features added
        """
        import pandas as pd
        
        if feature_set is None:
            feature_set = pd.DataFrame()
        
        if timedeltas is None:
            timedeltas = [pd.Timedelta(days=1)]  # Default to 1 day lag
        
        # Get the field names from mapping
        store_field = self.get_field_name('store_id')
        item_field = self.get_field_name('item_id')
        date_field = self.get_field_name('date')
        sales_field = self.get_field_name('sales')
        
        # Initialize the lag sum column
        lag_sum_values = []
        
        # Process each row in the feature set
        for idx, row in feature_set.iterrows():
            # Get the current row's store, item, and date
            current_store = row[store_field]
            current_item = row[item_field]
            current_date = pd.to_datetime(row[date_field])
            
            # Filter data to get records for this product and store combination
            filtered_data = self.filter_data({
                store_field: current_store,
                item_field: current_item
            })
            
            # Calculate sum of sales for all lag periods
            lag_avg = 0
            if not filtered_data.empty:
                # Convert date column to datetime for comparison
                filtered_data[date_field] = pd.to_datetime(filtered_data[date_field])
                
                for timedelta in timedeltas:
                    # Calculate the lag date
                    lag_date = current_date - timedelta
                    
                    # Find the sales figure for this lag date
                    lag_record = filtered_data[filtered_data[date_field] == lag_date]
                    
                    if not lag_record.empty and lag_record[sales_field].iloc[0] is not None:
                        lag_avg += lag_record[sales_field].iloc[0] / len(timedeltas)
            
            # If no lag data found, use None instead of 0
            lag_avg = lag_avg if lag_avg > 0 else None
            lag_sum_values.append(lag_avg)
        
        # Create column name based on timedeltas
        if len(timedeltas) == 1:
            days = timedeltas[0].days
            column_name = f'{days}_day_lag_sum'
        else:
            day_list = [str(td.days) for td in timedeltas]
            column_name = f'lag_sum_{"_".join(day_list)}_days'
        
        # Add the lag sum column to the feature set
        feature_set[column_name] = lag_sum_values
        
        return feature_set
    
    @abstractmethod
    def generate_features(self, data, feature_set=None):
        """
        Abstract method to generate features from input data.
        
        Args:
            data: Input data (type depends on implementation)
            feature_set (pandas.DataFrame, optional): DataFrame representing the feature set being constructed
            
        Returns:
            Processed data with generated features
        """
        pass

