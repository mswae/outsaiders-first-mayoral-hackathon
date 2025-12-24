import pandas as pd
import numpy as np

def ingest_data(file):
    df = pd.read_csv(file)
    feedback_volume = df[0].shape

    return df, feedback_volume