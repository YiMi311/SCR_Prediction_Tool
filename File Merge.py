import os
import pandas as pd

# Path to the main folder
directory = r'\\srpzyfap0003.insim.biz\ESGShare\GRP\FLECS_share\User Folders\Yiming Liang\SCR Prediction Tool\DataBase\test'

# List to hold dataframes
dfs = []

# Loop through immediate subfolders
for subfolder in os.listdir(directory):
    subfolder_path = os.path.join(directory, subfolder)
    if os.path.isdir(subfolder_path):
        for filename in os.listdir(subfolder_path):
            filepath = os.path.join(subfolder_path, filename)
            try:
                if filename.lower().endswith('.csv'):
                    dfs.append(pd.read_csv(filepath))
                elif filename.lower().endswith('.xlsx'):
                    dfs.append(pd.read_excel(filepath, engine='openpyxl'))
            except Exception as e:
                print(f"Failed to read {filename}: {e}")

# Merge and align columns
if dfs:
    merged_df = pd.concat(dfs, ignore_index=True, sort=False).fillna('')
    output_path = os.path.join(directory, 'merged_table.csv')
    merged_df.to_csv(output_path, index=False)
    print(f"Merged file saved to: {output_path}")
else:
    print("No valid files were found to merge.")
