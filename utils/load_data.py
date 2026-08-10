import pandas as pd
import os

DATA_PATH = os.path.join("data", "sample_-_superstore.xls")


def load_data():

    df = pd.read_excel(DATA_PATH)

    return df