from goatools.obo_parser import GODag
from collections import defaultdict
import pandas as pd
import os

# Load input data
input_file = os.path.join("examples", "input_examples", "example_GO_BP_modules.csv") #location of your input files i.e. data/input/
go_bp_data = pd.read_csv(input_file)
go_bp_data['GO_BP_ID'] = go_bp_data['GO_BP_ID'].str.strip("'")

# Specify GO hierarchy file
go_basic_file = os.path.join("data", "input", "go-basic.obo") #ensure the file is up to date
go_dag = GODag(go_basic_file)

output_data = []

# Process each module and GO term
for index, row in go_bp_data.iterrows():
    module = row['module']
    go_term = row['GO_BP_ID']
    
    if go_term in go_dag:
        go_obj = go_dag[go_term]
        hierarchy = defaultdict(list)
        hierarchy['GO_BP_ID'].append(go_term)
        hierarchy['module'].append(module)
        hierarchy['0_Level_Pathway'].append('biological_process')
        hierarchy['Input_Pathway'].append(go_obj.name)

        # Parent terms
        for ancestor_id in go_obj.get_all_parents():
            ancestor_obj = go_dag[ancestor_id]
            level_name = f"{ancestor_obj.level}_Level_Pathway"
            hierarchy[level_name].append(ancestor_obj.name)

        flat_data = {'module': module, 'GO_BP_ID': go_term}
        for level, terms in hierarchy.items():
            flat_data[level] = ', '.join(set(terms))

        output_data.append(flat_data)

# Output DataFrame
output_df = pd.DataFrame(output_data)
sorted_columns = ['module', 'GO_BP_ID'] + sorted(
    [col for col in output_df.columns if '_Level_Pathway' in col],
    key=lambda x: int(x.split('_')[0]) if x.split('_')[0].isdigit() else -1
)
output_df = output_df[sorted_columns]

# Save output
output_csv = os.path.join("examples", "output_examples", "example_GO_BP_modules_pathways_levels.csv")
output_df.to_csv(output_csv, index=False)
print(f'Output saved to: {output_csv}')