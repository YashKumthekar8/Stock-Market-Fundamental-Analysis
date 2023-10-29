import pandas as pd


df = pd.read_csv('data/TECHM_Balance_Sheet.csv')
print(df)
for col in df.columns:
    df.rename(columns = {col: ' ' + col + ' '}, inplace = True)
print(df.columns)
