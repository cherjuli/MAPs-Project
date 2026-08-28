# Measuring Management Accounting Practices from Corporate Disclosures

This repository contains the data structure and replication code for measuring management accounting practices (MAP) from corporate 10-K disclosures. The workflow collects and preprocesses SEC filings, constructs MAP measures with three text-analysis approaches, and evaluates the resulting measures through construct-validation analyses.

## Measurement approaches

- **GLLM:** prompt engineering, zero-shot and fine-tuned model experiments, local or OpenAI inference, and MAP scoring.
- **W2V:** survey-supported seed-word selection, Word2Vec dictionary development, and MAP scoring.
- **BoW:** dictionary-based Bag-of-Words MAP scoring.

The approaches share the same filing-collection and preprocessing workflow but can be run and evaluated separately.

## Repository structure

| Path | Contents |
| --- | --- |
| [`code/01_data_collection/`](code/01_data_collection/) | SEC EDGAR download, parsing, cleaning, and preprocessing notebooks. |
| [`code/02_map_measurement/`](code/02_map_measurement/) | GLLM, W2V, and BoW measurement workflows. |
| [`code/03_validation/`](code/03_validation/) | Construct-validation analyses and MAP-fit data preparation. |
| [`data/`](data/) | Committed dictionaries and evaluation inputs, local external data, generated intermediates, scores, and analysis outputs. |
| `paper/` | Paper-related project files. |
| `requirements_py39.txt` | Dependencies for filing collection, CPU preprocessing, OpenAI workflows, survey analysis, and MAP scoring. |
| `requirements_py310.txt` | Dependencies for GPU preprocessing, prompt engineering, local fine-tuning, and local inference. |
| `requirements_py314.txt` | Dependencies for the validation workflow. |
| [`LICENSE`](LICENSE) | MIT license for the repository code. |

More detailed file descriptions and method-specific run orders are available in the README files inside each directory.

## Data availability

Some small project inputs are committed, including the final BoW and W2V dictionaries, W2V seed-word selections, selected GLLM evaluation data, and the LSEG variable list. Their sources and reuse conditions are documented below; being present in this repository does not by itself grant redistribution rights.

The following source data are not committed:

- Raw SEC 10-K filing text
- Proprietary LSEG Data & Analytics extracts
- Licensed ISS Incentive Lab data
- DISCERN patent source files
- Large or generated intermediate datasets, models, inference results, scores, tables, figures, and logs

SEC filings are publicly available through EDGAR. LSEG and ISS data require appropriate subscriptions, while the DISCERN data used by the project are publicly available through Zenodo. See [`data/EXCLUDED_DATA_ACCESS.md`](data/EXCLUDED_DATA_ACCESS.md) for provider links, expected filenames, access instructions, and local storage locations. The complete data-folder layout is documented in [`data/README.md`](data/README.md).

Do not commit credentials, licensed source data, or large generated artifacts.

## Environment setup

The workflows use different Python environments because their package and hardware requirements differ. Create a separate environment for the workflow you intend to run.

### Python 3.9.4

Used for filing download and parsing, CPU preprocessing, OpenAI inference and fine-tuning, survey analysis, and MAP scoring.

```bash
python3.9 -m venv .venv-py39
source .venv-py39/bin/activate
python -m pip install --upgrade pip
pip install -r requirements_py39.txt
```

### Python 3.10.14

Used for GPU preprocessing, prompt engineering, local fine-tuning, and local GLLM inference.

```bash
python3.10 -m venv .venv-py310
source .venv-py310/bin/activate
python -m pip install --upgrade pip
pip install -r requirements_py310.txt
```

Local GLLM execution additionally requires access to the configured Hugging Face models and compatible GPU/CUDA resources. Runtime paths, model names, prompts, sharding, and logging are configured in `code/02_map_measurement/02_01_GLLM_Approach/02_01_03_Local_MAP_Inference/config.yaml` and `config_ft.yaml`.

### Python 3.14.3

Used for the validation notebook.

```bash
python3.14 -m venv .venv-py314
source .venv-py314/bin/activate
python -m pip install --upgrade pip
pip install -r requirements_py314.txt
```

## Reproduction workflow

### 1. Collect and preprocess filings

Run the notebooks in [`code/01_data_collection/`](code/01_data_collection/) in this order:

1. `Downloading_and_Parsing_Filings_final.ipynb`
2. `Preprocessing_Filings_final.ipynb`

The first notebook retrieves and parses SEC 10-K filings. The second creates the cleaned corpora used by the measurement approaches.

### 2. Construct MAP measures

Choose one or more routes under [`code/02_map_measurement/`](code/02_map_measurement/):

- **GLLM:** run prompt/model experiments, optionally fine-tune a local or OpenAI model, perform inference, and run `MAP_Scoring_GLLM_Approach_final.ipynb`.
- **W2V:** run `MAP_Survey_Analysis_final.ipynb`, followed by `MAP_Scoring_W2V_Approach_final.ipynb`.
- **BoW:** run `MAP_Scoring_BoW_Approach_final.ipynb`.

See [`code/02_map_measurement/README.md`](code/02_map_measurement/README.md) for the exact method-specific paths and run order.

### 3. Validate the measures

After producing scores for the selected measurement approach, run:

`code/03_validation/Validation_Analyses_final.ipynb`

The notebook combines MAP scores with the required external inputs and performs content, convergent, discriminant, and predictive validation analyses. Its expected external files are documented in [`data/External/README.md`](data/External/README.md).

## Outputs

Depending on the selected approach, the workflows create:

- Firm-year MAP dimension scores
- Within-industry and non-financial-sector normalized scores
- Validation-merge and MAP-fit datasets
- Prompting and inference evaluation results
- Descriptive and validation tables and figures

Generated outputs remain in the corresponding `data/GLLM/`, `data/W2V/`, `data/BoW/`, `data/Survey/`, and `data/Analyses_outputs/` locations and are generally excluded from version control.

## Committed data: sources, citations, and terms

The MIT license in [`LICENSE`](LICENSE) applies to the repository's software. It does **not** override third-party rights in source documents, provider metadata, published dictionaries, or other data. Unless a row below states otherwise, no separate open-data license is granted.

| Committed file(s) | Source and recommended citation | Redistribution and reuse terms |
| --- | --- | --- |
| `data/BoW/MAP_Dictionary_BoW_final.csv` | Project adaptation of the MAP dictionary described by Qiu, F., Hu, N., Liang, P., & Dow, K. (2023), “Measuring management accounting practices using textual analysis,” *Management Accounting Research*, 58, 100818. [https://doi.org/10.1016/j.mar.2022.100818](https://doi.org/10.1016/j.mar.2022.100818) | The underlying publication, supplementary materials, and publisher terms continue to apply. The repository grants no additional rights to the source dictionary; verify the original license or obtain permission before redistributing or adapting it. |
| `data/External/LSEG_variables_list_final.csv` | Project-curated list of LSEG Data & Analytics field identifiers used by the validation workflow. Cite LSEG Data & Analytics and this repository when describing the extraction specification. | This is a variable-request list, not an LSEG data extract. Access to and use of the referenced fields remain governed by the user's LSEG agreement. Do not add or redistribute downloaded LSEG values through this repository. |
| `data/GLLM/evaluation_set_MAP_sentences_final.xlsx`; `data/GLLM/Fine_tuning_data/evaluation_set_MAP_sentences_final_v2_2.xlsx` | Sentences selected from SEC-filed corporate 10-K reports with project-created MAP annotations. Cite the underlying filings, this repository, and the associated project paper when available. | Corporate filing text may retain third-party rights even though filings are publicly accessible through EDGAR. No separate redistribution license is granted for the sentence text or annotations. Do not redistribute these files outside this repository until the relevant text rights and participant/annotation conditions have been confirmed. |
| `data/W2V/Dictionary_creation/MAP_Dictionary_W2V_v1_final.csv`; `MAP_Dictionary_W2V_v2_final.csv`; `MAP_Seed_Words_Dictionary_final.csv`; `MAP_Seed_Words_Selection_v1.csv`; `MAP_Seed_Words_Selection_v2.csv` | Project-generated dictionary and seed-word artifacts created by the survey and Word2Vec workflows documented in `code/02_map_measurement/02_02_W2V_Approach/`. Cite Julian Wenzel, this repository, and the associated project paper when available. | Copyright © 2026 Julian Wenzel. No separate data license is currently granted; reuse or redistribution requires permission from the copyright holder and must respect any rights in underlying source material. |

README files, ignore rules, and other documentation are not datasets. Provider names and trademarks remain the property of their respective owners. When publishing results, also report the exact dataset versions and access dates used.

## Acknowledgment

The repository structure was adapted from the [TREAT template for reproducible research](https://github.com/trr266/treat).

## License

The repository code is released under the [MIT License](LICENSE). Third-party datasets remain subject to their providers' licenses and access conditions.
