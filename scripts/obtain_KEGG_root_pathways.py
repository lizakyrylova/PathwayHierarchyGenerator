import pandas as pd
from bioservices.kegg import KEGG
import os

# Load input data
input_file = os.path.join("examples", "input_examples", "example_KEGG_modules.csv") #location of your input files i.e. data/input/
input_df = pd.read_csv(input_file)

# Initialize KEGG
kegg = KEGG()
kegg.organism = "hsa"

def extract_class_info(pathway_code):
    if not pathway_code.startswith('hsa'):
        pathway_code = f'hsa{pathway_code}'

    try:
        raw_data = kegg.get(pathway_code)
        if isinstance(raw_data, str):
            root, sub, sub_sub = None, None, None
            for line in raw_data.splitlines():
                if line.startswith("CLASS"):
                    class_info = line.split("CLASS")[1].strip().split("; ")
                    root, sub = class_info if len(class_info) == 2 else (class_info[0], None)
                elif line.startswith("PATHWAY_MAP") and not sub_sub:
                    sub_sub = line.split(maxsplit=2)[-1].strip()
            return root, sub, sub_sub
    except Exception as e:
        print(f"Error fetching data for {pathway_code}: {e}")
    return None, None, None

results = [
    {
        "module": row.module,
        "KEGG_ID": row.KEGG_ID.strip("'"),
        **dict(zip(["0_Level_Pathway", "1_Level_Pathway", "2_Level_Pathway"], extract_class_info(row.KEGG_ID.strip("'"))))
    }
    for row in input_df.itertuples()
]

output_df = pd.DataFrame(results)
output_csv = os.path.join("examples", "output_examples", "example_KEGG_modules_pathways_levels.csv")
output_df.to_csv(output_csv, index=False)
print(f'Results saved successfully to: {output_csv}')