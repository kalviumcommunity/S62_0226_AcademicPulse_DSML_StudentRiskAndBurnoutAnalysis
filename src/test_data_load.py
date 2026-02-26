# src/test_data_load.py
import pandas as pd

# Try to read the data
df = pd.read_csv('data/raw/student_data.csv')
print("Data loaded successfully!")
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"\nFirst row:\n{df.iloc[0]}")