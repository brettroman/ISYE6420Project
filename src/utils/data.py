import pandas as pd
from utils.file_io import make_directory_for_file


def get_df(data_path):
    df = pd.read_csv(data_path)

    return df

def save_df(df, file_path):
    make_directory_for_file(file_path)
    df.to_csv(file_path, index=False)