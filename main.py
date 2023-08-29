import os
import pandas as pd
import chardet

# read all csv files from a folder
folder_path = "imports_csv" 

# encoding detection
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

# List all CSVs in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Create a list of dataframes
dfs = [pd.read_csv(os.path.join(folder_path, f), encoding=detect_encoding(os.path.join(folder_path, f))) for f in csv_files]

# Define a function to check if a variable is present in all CSVs
def check_user_presence(Var_1, Var_2):
    if pd.isna(Var_1) or pd.isna(Var_2):
        return "error message"

    data_in_all_dfs = all(data_in_df.any() for data_in_df in [(df['Var_1'] == Var_1) & (df['Var_2'] == Var_2) for df in dfs])

    if data_in_all_dfs:
        return "True"
    else:
        missing_csvs = [csv_files[i] for i, data_in_df in enumerate([(df['Var_1'] == Var_1) & (df['Var_2'] == Var_2) for df in dfs]) if not data_in_df.any()]
        return f'miss in {", ".join(missing_csvs)}'
# combine all dataframes into one
all_data = pd.concat(dfs).drop_duplicates(subset=['Var_1', 'Var_2'])

# create a new dataframe to store the results
results = pd.DataFrame(columns=['Var_1', 'Var_2', 'Var_3'])

# check if a variable is present in all CSVs
for index, row in all_data.iterrows():
    Var_1 = row['Var_1']
    Var_2 = row['Var_2']
    status = check_user_presence(Var_1, Var_2)
    new_row = pd.DataFrame({'Var_1': [Var_1], 'Var_2': [Var_2], 'Var_3': [status]})
    results = pd.concat([results, new_row], ignore_index=True)

    
# create a new CSV file with the results
results.to_csv('output.csv', index=False)
