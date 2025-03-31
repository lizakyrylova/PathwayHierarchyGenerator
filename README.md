# PathwayHierarchyGenerator

A flexible framework for annotating entities with hierarchical pathway data from GO, KEGG, and Reactome. While originally designed for gene modules, this toolkit is applicable to any entity (e.g., genes, proteins, metabolites, or biological samples) that has an associated pathway term.

## Overview

This repository provides Python scripts to automate the retrieval and organization of hierarchical pathway annotations. The scripts extract multi-level functional annotations using:

- **GO:BP:** Leveraging the GO DAG with goatools.
- **KEGG:** Using the bioservices package to fetch KEGG pathway classifications.
- **Reactome:** Utilizing the Reactome API via bioservices package to obtain pathway ancestry.

The output from each script is saved as a CSV file, with each file containing:
- An entity or module identifier.
- A pathway or term identifier.
- A series of annotation levels that capture the hierarchy, starting from a broad `0_Level_Pathway` (representative of the broadest biological category the term belongs to), and progressing into more detailed levels (Level 1 and onwards).

## Annotation Levels

- **GO:BP:**  
  The output file (GO_BP_modules_pathways_levels.csv) provides annotations up to n_Level_Pathway, where n varies depending on the term. Due to the GO DAG (directed acyclic graph) structure, a single GO BP term can have multiple parental lineages, leading to several annotations at the same hierarchical level. Therefore, annotations at any given level represent multiple alternative hierarchical paths rather than a strictly linear hierarchy.

- **KEGG:**  
  The output file (KEGG_modules_pathways_levels.csv) reaches up to 2_Level_Pathway, providing 3 resolution levels total (0, 1, and 2). This decision is based on two considerations:

  All KEGG terms inherently have these three functional annotation levels, and many terms (particularly Disease terms) do not extend beyond them.

  Annotations beyond the second level in KEGG are often unordered subpathways ("network elements") without clear hierarchical relationships, which would lead to confusing or uninformative 
  annotations if included.


- **Reactome:**  
  The output file (REAC_modules_pathways_levels.csv) captures annotations up to n_Level_Pathway, where n is determined by the structure of the Reactome pathway hierarchy and varies between 
  different pathways or entities.

## Repository Structure
```bash
PathwayHierarchyGenerator/
├── README.md                          # Project overview, installation, usage instructions
├── requirements.txt                   # Python dependencies
├── scripts/                           # Python scripts for pathway annotations
│   ├── obtain_GO_BP_root_pathways.py
│   ├── obtain_KEGG_root_pathways.py
│   └── obtain_REAC_root_pathways.py
├── data/                              # Directory for actual input/output data
│   ├── input/                         # Real input data files
│   │   └── go-basic.obo               # Required GO ontology file
│   └── output/                        # Directory for generated outputs
└── examples/                          # Example input/output files for reference
    ├── input_examples/                # Sample CSV files illustrating input structure
    │   ├── example_GO_BP_modules.csv
    │   ├── example_KEGG_modules.csv
    │   └── example_REAC_modules.csv
    └── output_examples/               # Corresponding outputs from each script
        ├── example_GO_BP_modules_pathways_levels.csv
        ├── example_KEGG_modules_pathways_levels.csv
        └── example_REAC_modules_pathways_levels.csv
```
## Data Requirements

To run the scripts effectively, please ensure the following prerequisites are fulfilled:

### General Requirements:

- Python (version ≥ 3.6 recommended)
- Required Python packages are listed in the provided `requirements.txt`. Install them using:

```bash
pip install -r requirements.txt
```

### GO:BP Specific Requirements:

The GO:BP script (`obtain_GO_BP_root_pathways.py`) requires an up-to-date Gene Ontology Basic (`go-basic.obo`) file. This file is essential for `goatools` to fetch and parse hierarchical terms from the Gene Ontology DAG structure. **The file provided in this repository may be outdated, please download the latest one**.

Download the most current version using:

```bash
wget http://purl.obolibrary.org/obo/go/go-basic.obo
```

Place this file into your designated input directory (e.g., `data/input/`), and ensure the script points correctly to this path:

```python
go_basic_file = 'data/input/go-basic.obo'
```

Regularly updating this file is recommended to ensure accuracy and completeness of the GO term annotations.

## Usage Example

A typical workflow would involve:

1. **Preparing input data**: Ensure your input CSV files have clearly labeled columns (entity IDs and pathway IDs) placed in `data/input/`.

2. **Running scripts**:

- For GO:BP:
```bash
python scripts/obtain_GO_BP_root_pathways.py
```

- For KEGG:
```bash
python scripts/obtain_KEGG_root_pathways.py
```

- For Reactome:
```bash
python scripts/obtain_REAC_root_pathways.py
```

3. **Inspecting outputs**: Annotated files are saved in the `data/output/` directory as CSVs, ready for downstream analyses such as clustering, visualization (heatmaps), or integration with other bioinformatics pipelines.

## Downstream Applications

The structured annotation outputs facilitate a wide range of downstream applications, including but not limited to:
- Functional enrichment analysis
- Visualization of pathway activities (e.g., heatmaps)
- Integration into network-based analyses
- Comparative studies across conditions, tissues, or disease states


## Acknowledgments

This repository utilizes several powerful open-source resources:

- [goatools](https://github.com/tanghaibao/goatools)
- [bioservices](https://bioservices.readthedocs.io)
- [Gene Ontology Consortium](http://geneontology.org)




