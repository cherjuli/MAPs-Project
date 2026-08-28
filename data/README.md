# Data directory

This directory contains the inputs, intermediate artifacts, and outputs used by the MAP measurement and validation workflows. Folder names are case-sensitive.

## Structure

| Path | Purpose | Version-control status |
| --- | --- | --- |
| `10-K/` | Raw SEC 10-K filing text collected by the notebooks in `code/01_data_collection/`. | Contents are excluded; recreate locally from SEC EDGAR. |
| `Analyses_outputs/` | Tables, figures, and other generated analysis outputs. | Generated contents are excluded. |
| `BoW/` | Bag-of-Words dictionary, intermediate datasets, MAP scores, and validation merges. | The final dictionary and folder documentation are committed; generated artifacts remain local. |
| `External/` | Manually obtained or proprietary inputs from LSEG, ISS Incentive Lab, and DISCERN, plus derived extracts used in validation. | Only the LSEG variable list and documentation are committed. |
| `GLLM/` | GLLM preprocessing data, prompt and batch files, local/OpenAI results, inference shards, logs, and fine-tuning artifacts. | Selected evaluation data and documentation are committed; runtime and generated artifacts remain local. |
| `Survey/` | MAP survey inputs and generated descriptive, response, and dimension-level outputs. | See `Survey/README.md` for required inputs and output locations. |
| `W2V/` | Word2Vec preprocessing data, dictionary-development artifacts, MAP scores, and validation merges. | Final dictionary inputs and documentation are committed; generated artifacts remain local. |
| `EXCLUDED_DATA_ACCESS.md` | Instructions for obtaining or recreating data that cannot be distributed through this repository. | Committed. |

Each method-specific directory contains a README with its expected files, outputs, and related notebooks.

## Files currently committed

- `BoW/MAP_Dictionary_BoW_final.csv`
- `External/LSEG_variables_list_final.csv`
- `GLLM/evaluation_set_MAP_sentences_final.xlsx`
- `GLLM/Fine_tuning_data/evaluation_set_MAP_sentences_final_v2_2.xlsx`
- `W2V/Dictionary_creation/MAP_Dictionary_W2V_v1_final.csv`
- `W2V/Dictionary_creation/MAP_Dictionary_W2V_v2_final.csv`
- `W2V/Dictionary_creation/MAP_Seed_Words_Dictionary_final.csv`
- `W2V/Dictionary_creation/MAP_Seed_Words_Selection_v1.csv`
- `W2V/Dictionary_creation/MAP_Seed_Words_Selection_v2.csv`

README files and placeholder/`.gitignore` files are also committed where needed to preserve and document the directory structure.

## Data not committed

The following data must be obtained or generated locally:

- Raw SEC 10-K filing text
- Proprietary LSEG source data
- Licensed ISS Incentive Lab data
- DISCERN patent data
- Generated intermediate datasets, model artifacts, scores, validation merges, plots, tables, and logs

See [`EXCLUDED_DATA_ACCESS.md`](EXCLUDED_DATA_ACCESS.md) for access and recreation instructions. Do not commit licensed, proprietary, or large generated datasets unless their redistribution and storage requirements have been reviewed.
