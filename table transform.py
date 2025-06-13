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
                    print(f"Reading CSV: {filename}")
                    dfs.append(pd.read_csv(filepath))
                elif filename.lower().endswith('.xlsx'):
                    print(f"Reading Excel: {filename}")
                    dfs.append(pd.read_excel(filepath, engine='openpyxl'))
            except Exception as e:
                print(f"Failed to read {filename}: {e}")

# Merge and save
if dfs:
    merged_df = pd.concat(dfs, ignore_index=True)
    print(f"Merged file saved to: {output_path}")
else:
    print("No valid files were found to merge.")

# Read the CSV
df = merged_df.copy()

# Grouping columns
group_columns = [
    'Run ID', 'Capital View', 'HIERARCHY ID', 'FULLHIERARCHY', 'GROUP', 'DIVISION', 'BL', 'BU', 'PF', 'PFM',
    'Instrument Id', 'Position ID', 'Zoom Level', 'Gaudi Code', 'Gaudi Level', 'Local or Group Currency',
    'Estimator', 'Percentile', 'Asset Liability Type', 'Account Type', 'Capital Adjustments', 'Source',
    'FLECS Instrument Type', 'Quotation Currency', 'Reporting Currency'
]

# Metrics to pivot
metrics = [
    'Market Value', 'Duration', 'CS Duration', 'Market Risk SCR', 'Market Risk Excl Basis SCR', 'Equity incl Impl Vol SCR',
    'Equity SCR', 'Equity Impl Vol SCR', 'Diversification Equity incl Impl Vol Equity SCR', 'Interest Rates incl Impl Vol SCR',
    'Interest Rates SCR', 'Interest Rates Impl Vol SCR', 'Diversification Interest Rates incl Impl Vol SCR', 'FX incl Impl Vol SCR',
    'FX SCR', 'FX Impl Vol SCR', 'Diversification FX incl Impl Vol SCR', 'Credit Spread SCR', 'Inflation SCR', 'Real Estate SCR',
    'Basis SCR', 'Diversification Market Risk SCR', 'Diversification Market Risk Excl Basis SCR', 'Interest Rates EUR SCR',
    'Interest Rates EUR PC1 SCR', 'Interest Rates EUR PC2 SCR', 'Interest Rates EUR PC3 SCR', 'Interest Rates EUR PC12 SCR'
]

# Pivot the data for each metric using pivot()
pivoted_dfs = []
for metric in metrics:
    pivoted_df = df.pivot(
        index=group_columns,
        columns=['Scr type', 'Scr Subtype'],
        values=metric
    )
    pivoted_df.columns = [f'{metric} {i}_{j}' for i, j in pivoted_df.columns]
    pivoted_dfs.append(pivoted_df)

# Combine all pivoted dataframes
final_df = pd.concat(pivoted_dfs, axis=1)
final_df.reset_index(inplace=True)

# Check for duplicates
duplicates = df.duplicated(subset=group_columns + ['Scr type', 'Scr Subtype']).sum()
print(f"Number of duplicate rows based on grouping columns plus 'Scr type' and 'Scr Subtype': {duplicates}")

# Save the result
output_path = r'\\srpzyfap0003.insim.biz\ESGShare\GRP\FLECS_share\User Folders\Yiming Liang\SCR Prediction Tool\DataBase\Transformed_BSCR_IM_MarketRisk_Position_Report_EUR_16758.csv'
final_df.to_csv(output_path, index=False)

print(f"Transformed file saved to: {output_path}")
