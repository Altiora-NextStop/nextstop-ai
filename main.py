import pandas as pd

DATASET_PATH = "data/tourism_dataset.csv"

df = pd.read_csv(DATASET_PATH)

print("Column names in CSV:")
print(df.columns.tolist())