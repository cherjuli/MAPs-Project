# W2V data folder

This folder contains:
- intermediate datasets from the W2V measurement pipeline,
- MAP scoring outputs,
- validation-merge outputs used for MAP-fit analyses,
- dictionary artifacts based on the MAP survey workflow.

## Subfolders and outputs

### `Intermediate_datasets/`
Main preprocessing and scoring intermediates, including:
- `Corpus_df_HTML_cleaned_W2V_final.pkl`
- `Corpus_df_W2V_v1_tmp.pkl`, `Corpus_df_W2V_v1.pkl`
- `Corpus_df_W2V_v2_tmp.pkl`, `Corpus_df_W2V_v2.pkl`
- `Corpus_df_W2V_v3.pkl`, `Corpus_df_W2V_v3_w_bigrams.pkl`, `Corpus_df_W2V_v3_w_trigrams.pkl`, `Corpus_df_W2V_v3_final.pkl`
- `Corpus_df_W2V_v4.pkl`
- `Corpus_df_W2V_cleaned_sentences_final.csv`
- `validation_set_with_MAP_token_counts_W2V_{dictionary_version}.xlsx`

### `Dictionary_creation/`
Dictionary-development artifacts used by and generated from the W2V survey analysis, including:
- `MAP_Seed_Words_Dictionary_final.csv` (input)
- `term_matrix_token_level_final.xlsx`
- `term_matrix_token_level_sum_final.xlsx`
- `MAP_Seed_Words_Dictionary_analysis_final.xlsx`
- `MAP_Seed_Words_Selection_v1.csv`, `MAP_Seed_Words_Selection_v2.csv` (inputs)
- `MAP_Dimension_Synonyms_W2V_v1.xlsx`, `MAP_Dimension_Synonyms_W2V_v2.xlsx`
- `MAP_Dictionary_W2V_v1_final.csv`, `MAP_Dictionary_W2V_v2_final.csv`
- `w2v_filing_text.model`

### W2V scoring outputs at folder root
- `Corpus_df_W2V_{dictionary_version}_dimension_scores_final.pkl`
- `Corpus_df_W2V_{dictionary_version}_dimension_scores_within_industry_normalized.pkl`
- `Corpus_df_W2V_{dictionary_version}_dimension_scores_without_finance_normalized.pkl`
- `Validation_Merge_W2V_v1_final.pkl`, `Validation_Merge_W2V_v2_final.pkl`
- `Validation_Merge_W2V_v1_within_industry_normalized.pkl`, `Validation_Merge_W2V_v2_within_industry_normalized.pkl`
- `Validation_Merge_W2V_v1_without_finance_normalized.pkl`, `Validation_Merge_W2V_v2_without_finance_normalized.pkl`

## Notebook references in `code/`

Files that generate or use outputs in this folder:
- `code/01_data_collection/Preprocessing_Filings_final.ipynb`
  - generates `W2V/Intermediate_datasets/*` preprocessing corpora and sentence-level exports.
- `code/02_map_measurement/02_02_W2V_Approach/MAP_Survey_Analysis_final.ipynb`
  - uses `W2V/Intermediate_datasets/Corpus_df_W2V_v4.pkl` and dictionary inputs,
  - generates dictionary analysis and synonym files in `W2V/Dictionary_creation/`.
- `code/02_map_measurement/02_02_W2V_Approach/MAP_Scoring_W2V_Approach_final.ipynb`
  - uses cleaned corpus and `MAP_Dictionary_W2V_{dictionary_version}_final.csv`,
  - generates W2V MAP score files at `W2V/` root and validation token-count files in `W2V/Intermediate_datasets/`.
- `code/03_validation/Validation_Analyses_final.ipynb`
  - uses `W2V/Corpus_df_W2V_{dictionary_version}_dimension_scores*.pkl` when `measurement_approach` is `W2V_v1` or `W2V_v2`,
  - generates `W2V/Validation_Merge_W2V_*` files.
