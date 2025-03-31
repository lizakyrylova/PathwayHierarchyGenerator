import pandas as pd
from bioservices import Reactome
import os

# Load input data
input_file = os.path.join("examples", "input_examples", "example_REAC_modules.csv") #location of your input files i.e. data/input/
df = pd.read_csv(input_file)
df['REAC_ID'] = df['REAC_ID'].str.strip("'")

# Initialize Reactome
reactome = Reactome()

results = []

for module, reac_id in df[['module', 'REAC_ID']].itertuples(index=False):
    ancestors = reactome.get_event_ancestors(reac_id)
    if isinstance(ancestors, list) and ancestors and isinstance(ancestors[0], list):
        pathways = list(reversed(ancestors[0]))
        row_data = {'module': module, 'REAC_ID': reac_id}
        for level, pathway in enumerate(pathways):
            level_label = f'{level}_Level_Pathway'
            row_data[level_label] = pathway.get('displayName', 'N/A')
        results.append(row_data)
    else:
        print(f'No valid ancestors found for pathway ID: {reac_id}, in {module}')

result_df = pd.DataFrame(results)
output_csv = os.path.join("examples", "output_examples", "example_REAC_modules_pathways_levels.csv")
result_df.to_csv(output_csv, index=False)
print(f'Results saved successfully to: {output_csv}')