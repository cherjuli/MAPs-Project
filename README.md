# Measuring Management Accounting Practices from Corporate Disclosures

Replication repository scaffold for a MAP measurement project, adapted from the TREAT template.

## Overview
This repository is organized for a full MAP workflow: SEC filing collection, MAP measurement (BoW/W2V/GLLM), validation, descriptive analysis, and predictive/regression analysis.

## Data Availability
- SEC 10-K filings: retrieved via SEC EDGAR (free; raw filing text is not committed)
- Financial and ESG/governance data: LSEG Data & Analytics (subscription required; not committed)
- Shareable project outputs: MAP scores and MAP-fit outputs can be stored in `data/processed/` when licensing permits

## Repository Structure
- `.devcontainer/`: optional reproducible development environment (Codespaces/VS Code)
- `code/01_data_collection/`: SEC EDGAR retrieval and preprocessing
- `code/02_map_measurement/`: BoW, W2V, and GLLM MAP measurement pipeline
- `code/03_validation/`: content, convergent, and discriminant validity scripts
- `code/04_descriptive/`: descriptive statistics and figure generation
- `code/05_regression/`: predictive-validity and robustness analyses
- `config/`: model paths, hyperparameters, and credentials templates
- `data/external/`: shareable external inputs (e.g., seed words, questionnaire artifacts)
- `data/processed/`: derived shareable outputs (e.g., MAP and MAP-fit scores)
- `doc/`: manuscript, appendix, and slides sources
- `output/`: generated tables and figures
- `info/`: codebook, variable definitions, and supplementary documentation

## What to Include vs Exclude
Include:
- All code and configuration files
- Questionnaire instrument/results (if sharable)
- Final dictionary files (W2V seeds and expanded dictionaries)
- MAP and MAP-fit aggregate firm-year outputs (if licensing permits)
- Validation and regression scripts
- Fine-tuning data structure and prompts (even when annotated text cannot be shared)

Exclude:
- Raw 10-K filing text
- Proprietary LSEG datasets
- Annotated evaluation data containing substantial reproduced filing text

For excluded data, keep placeholder documentation in the corresponding folders with retrieval/access instructions.

## How to Reproduce
### 1. Set up environment
Choose a Python version based on the workflow you are running, then install the matching cumulative requirements file:

- **Python 3.9.4** (`requirements_py39.txt`): filing download/parsing, CPU preprocessing, OpenAI inference/fine-tuning, survey analysis, and MAP scoring notebooks
- **Python 3.10.14** (`requirements_py310.txt`): GPU preprocessing, prompt engineering, and local fine-tuning notebooks
- **Python 3.14.3** (`requirements_py314.txt`): validation analyses notebook

```bash
pip install -r requirements_py39.txt   # or requirements_py310.txt / requirements_py314.txt
```

### 2. Configure credentials
Copy and edit local secrets:

```bash
cp _secrets.env secrets.env
```

### 3. Run the pipeline
```bash
make data
make measure
make validate
make analyze
make paper
```

## Key Outputs
- MAP dimension scores per firm-year (e.g., W2V/GLLM variants)
- MAP-fit scores per firm-year
- Tables and figures for manuscript/presentation outputs

## Citation
Please cite your paper and, if useful, acknowledge the template origin:

> This repository was built based on the [TREAT template for reproducible research](https://github.com/trr266/treat).

## License
- Code: MIT (`LICENSE`)
- Shared data/derived outputs: recommend CC BY 4.0
