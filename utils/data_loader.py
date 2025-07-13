import os
import pandas as pd

def load_cleaned_data(folder_path='B/data/raw/'):
    """
    Loads cleaned CSV files from the specified folder into a dictionary of DataFrames.
    Assumes the first column is the datetime index.
    """
    data_dict = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            filepath = os.path.join(folder_path, filename)
            try:
                df = pd.read_csv(filepath, index_col=0, parse_dates=True, dayfirst=False)
                df.index.name = 'Date'  
                df = df.sort_index()
                data_dict[filename.replace('.csv', '')] = df
            except Exception as e:
                print(f"⚠️ Error loading {filename}: {e}")
    return data_dict
