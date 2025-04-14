import pandas as pd
import numpy as np

# CleanSheet: Automatically generated data cleaning script

# Load the original CSV file
df = pd.read_csv('your_file.csv')  # Replace with your file path

# Original DataFrame info
# Number of rows: 6390
# Number of columns: 13
# Columns: ['INDICATOR', 'UNIT', 'UNIT_NUM', 'STUB_NAME', 'STUB_NAME_NUM', 'STUB_LABEL', 'STUB_LABEL_NUM', 'YEAR', 'YEAR_NUM', 'AGE', 'AGE_NUM', 'ESTIMATE', 'FLAG']

# Print the first few rows of the original data
print('Original data:')
print(df.head())

# Cleaning steps
df = df.dropna()

# Convert column types
df['YEAR'] = pd.to_datetime(df['YEAR'])

# Rename columns
df = df.rename(columns={'YEAR_NUM': 'Year_Number'})

# Print the first few rows of the cleaned data
print('\nCleaned data:')
print(df.head())

# Save the cleaned data to a new CSV file
df.to_csv('cleaned_data.csv', index=False)  # Replace with your desired output path
print('\nCleaned data saved to cleaned_data.csv')
