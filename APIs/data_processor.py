import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder


def export_data(filepath: str):
    data = pd.read_csv(filepath.replace("\\", "\\\\"), encoding='unicode_escape')
    data.fillna(data.mean(numeric_only=True), inplace=True)
    return data

def normalize_nan_data(data) -> pd.DataFrame:
    process_data = data.copy()
    number_columns = data.select_dtypes(exclude= ['int', 'float']).columns
    encoder = LabelEncoder()
    for col in number_columns:
        column_data = process_data[col].values
        process_data[col] = encoder.fit_transform(column_data)
    return process_data


def import_array_to_data(arr = None, header = None):
    if arr is None:
        return None
    if header is None:
        header = range(arr.shape[1])
    index = range(arr.shape[0])
    return pd.DataFrame(data=arr, index=index, columns=header)

class DataProcess:
    def __init__(self):
        self.scaler = None
    def scale_data(self, data: pd.DataFrame) -> pd.DataFrame:
        self.scaler = StandardScaler()
        process_data = self.scaler.fit_transform(data)
        return process_data
    
    def preprocess_data(self, data) -> pd.DataFrame:
        processed_data = normalize_nan_data(data)
        processed_data = self.scale_data(processed_data)
        return processed_data
    
    def reverse_scale_data(self, scaled_data_points):
        """
        :param scaled_data_points: Array of data points that scaled for clustering
        :return: data points before scaled
        """
        return self.scaler.inverse_transform(scaled_data_points)
