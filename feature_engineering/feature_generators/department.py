from .feature_gen import FeatureGen
from typing import override


class Department(FeatureGen):
    """
    Feature generator for department features.
    
    This class generates features based on product department information.
    """
    
    def __init__(self, field_name_mapping=None, data=None):
        """
        Initialize the Department feature generator.
        
        Args:
            field_name_mapping (Dict[str, str], optional): Dictionary mapping field names.
            data: pandas DataFrame containing the data to process
        """
        super().__init__(field_name_mapping, data)
    
    @override
    def generate_features(self, data, feature_set=None):
        """
        Generate department features from input data.
        
        Args:
            data: Input data containing product department information
            feature_set (pandas.DataFrame, optional): DataFrame representing the feature set being constructed
            
        Returns:
            List of department IDs corresponding to each row
        """
        # Extract department IDs for each row
        return self.get_categorical_feature(data, 'department')
