from .feature_gen import FeatureGen
import pandas as pd


class Prev2YearWeek(FeatureGen):
    """
    Feature generator for previous two year week features.
    
    This class generates features based on sales data from the same week two years ago.
    """
    
    def __init__(self, field_name_mapping=None, data=None):
        """
        Initialize the Prev2YearWeek feature generator.
        
        Args:
            field_name_mapping (Dict[str, str], optional): Dictionary mapping field names.
            data: pandas DataFrame containing the data to process
        """
        super().__init__(field_name_mapping, data, "Prev2YearWeek")
    
    def generate_features(self, data, feature_set=None):
        """
        Generate previous two year week features from input data.
        
        Args:
            data: Input data containing sales information
            feature_set (pandas.DataFrame, optional): DataFrame representing the feature set being constructed
            
        Returns:
            pandas.DataFrame: Feature set with previous two year week features added
        """
        # Use the super class method to generate lag features average
        return self.generate_lag_features_avg(data, feature_set, [pd.Timedelta(days=i) for i in range(723, 730)])
