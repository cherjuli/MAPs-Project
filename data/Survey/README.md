This README documents the data workflow used in `code/02_map_measurement/02_02_W2V_Approach/MAP_Survey_Analysis_final.ipynb`.

## Purpose

The notebook is used to:

1. Select and validate MAP words/phrases for each MAP dimension using a word-embedding (W2V) approach.
2. Analyze the MAP survey results and produce descriptive statistics, figures, and summary tables.
3. Compare response patterns across respondent subgroups such as country of residence, experience, and job role.

## Required input files

Place the survey inputs in this folder structure:

- `Survey/MAP_survey_final.csv` — survey response export
- `Survey/MAP_survey_variables.csv` — variable mapping file with item IDs and labels

The notebook also expects these project files to exist:

- `W2V/Intermediate_datasets/Corpus_df_W2V_v4.pkl`
- `W2V/Dictionary_creation/MAP_Seed_Words_Dictionary_final.csv`
- `W2V/Dictionary_creation/w2v_filing_text.model`

## Main workflow

### 1. MAP token occurrence analysis in 10-K filings

The notebook loads a preprocessed corpus, cleans the filing text, and counts occurrences of the selected MAP seed words and phrases with spaCy’s `PhraseMatcher`.

Outputs created by this step include:

- `W2V/Intermediate_datasets/Corpus_df_W2V_v4.pkl`
- `W2V/Dictionary_creation/term_matrix_token_level_final.xlsx`
- `W2V/Dictionary_creation/term_matrix_token_level_sum_final.xlsx`
- `W2V/Dictionary_creation/MAP_Seed_Words_Dictionary_analysis_final.xlsx`

### 2. Survey descriptives

The notebook loads the survey data, filters to approved responses, and optionally restricts the sample to:

- U.S. respondents
- respondents with more than 3 years of MA experience
- controller respondents

It then creates descriptive tables and plots for:

- functional area
- job role
- time in current position
- time in MA field
- company size
- company type
- industry sector
- employment status
- age groups
- gender
- country of residence

These outputs are saved under:

- `Survey/Plots/Descriptives/`
- `Survey/Tables/Descriptives/`

### 3. MAP item selection analysis

For each MAP dimension, the notebook:

- calculates selection frequencies for each item
- computes binary variance, standard deviation, entropy, and a consensus index
- runs chi-square tests on response distributions
- calculates Fleiss’ kappa for inter-rater agreement
- saves response-level and dimension-level summaries

These outputs are saved under:

- `Survey/Plots/Response/`
- `Survey/Tables/Response/`
- `Survey/Tables/Dimension/`

### 4. Group comparison analysis

The notebook compares selection frequencies across respondent subgroups, including:

- U.S. vs. non-U.S. respondents
- controller vs. non-controller respondents
- experienced vs. less experienced respondents

## Notes

- The notebook assumes the directory structure used in this repository and is designed to be run from within the `code/02_map_measurement/02_02_W2V_Approach/` workflow.
- Some output file names depend on the filter settings used when running the notebook.
- If `US_index` is set to `Yes`, separate `_US` output files are generated.
- If additional filters are enabled, the corresponding suffix is appended to saved plots and tables.
