# GLLM data folder

This folder contains intermediate inputs, inference outputs (zero‑shot and fine‑tuned), runtime logs, fine‑tuning artifacts, and prompt / batch files used for local and OpenAI experiments.

## This folder contains
- intermediate datasets for the GLLM pipeline
- local and OpenAI prompting outputs (Excel/JSONL)
- inference shard pickles produced by local/SLURM runs
- logs and fine‑tuning artifacts used by the FT pipeline
- parsed OpenAI outputs used for evaluation/validation

## Subfolders and typical outputs

### `Intermediate_datasets/`
Preprocessing inputs used to create inference shards:
- Corpus_df_HTML_cleaned_GLLM_final.pkl (cleaned corpus used by main.py)
- any sentence‑level exports used to construct prompt batches

### `Fine_tuning_data/`
Artifacts and saved models used for fine‑tuning:
- `optuna_runs/` (e.g., `trial_20/`) — saved trials and best model dirs
- saved fine‑tuned model folders referenced by config_ft.yaml

### `Final_Inference_results/`
- `logs/` — log files written during runs (path set in config.yaml / config_ft.yaml)
- `processed/` — processed shard pickles created by inference:
  - Corpus_df_HTML_cleaned_GLLM_final_shard_{0..N}.pkl
  - Corpus_df_HTML_cleaned_GLLM_final_FT_shard_{0..N}.pkl (fine‑tuned)
- runtime artifacts referenced by scripts:
  - out{shard}.jsonl (raw outputs appended by main.py)
  - resume{shard}.json / resume_ft_{shard}.json (resume state files)

### `Local_prompting_results/`
Local (on‑prem / Hugging Face) prompt experiment outputs (Excel):
- output_ZS_sys{system_idx}_user{user_idx}_{model}.xlsx
- output_FT_val_{model}.xlsx
- Used to compare zero‑shot and FT results with OpenAI outputs

### `OpenAI_batch_files/`
Batch JSONL files prepared for OpenAI (or similar) batch API:
- MAP_sentences_final_FT.jsonl
- evaluation_batch_sys{system_idx}_user{user_idx}_{model}.jsonl
- Created by batch creation helpers in OpenAI_Inference_final.ipynb / OpenAI_Fine_Tuning_final.ipynb

### `OpenAI_results/`
Downloaded raw batch outputs (JSONL) from the API server:
- evaluation_batch_results_sys{system_idx}_user{user_idx}_{model}.jsonl
- Produced by retrieve_batch_results(...) in OpenAI_Inference_final.ipynb

### `OpenAI_prompting_results/`
Parsed/flattened OpenAI outputs saved as Excel for evaluation:
- output_ZS_sys{...}_{model}.xlsx
- output_FT_val_ft_{model}.xlsx
- Read by evaluation notebooks to compute metrics and produce comparison tables

### `MAP_dictionary/`
MAP survey / dictionary artifacts used by MAP_Survey_Analysis and scoring notebooks.

## Notebooks / scripts that generate or consume files (canonical references)
- code/01_data_collection/Preprocessing_Filings_final.ipynb
  - generates preprocessing corpora used by `Intermediate_datasets/`
- code/02_map_measurement/02_01_GLLM_Approach/02_01_01_Prompt_Engineering/OpenAI_Inference_final.ipynb
  - creates `OpenAI_batch_files/*`, downloads to `OpenAI_results/*`, and helps parse to `OpenAI_prompting_results/*`
- code/02_map_measurement/02_01_GLLM_Approach/02_01_01_Prompt_Engineering/Prompt_Engineering_final.ipynb
  - creates `Local_prompting_results/*` for local HF experiments
- code/02_map_measurement/02_01_GLLM_Approach/02_01_02_Fine_Tuning/OpenAI_Fine_Tuning_final.ipynb
  - prepares FT batch JSONL (`OpenAI_batch_files/`), writes parsed FT outputs to `OpenAI_prompting_results/`, and reads `Local_prompting_results/` for comparative evaluation
- code/02_map_measurement/02_01_GLLM_Approach/02_01_03_Local_MAP_Inference/main.py
  - creates shards from `Intermediate_datasets/` and writes processed shard pickles to `Final_Inference_results/processed/`
- code/02_map_measurement/02_01_GLLM_Approach/02_01_03_Local_MAP_Inference/utils.py, utils_ft.py
  - pipeline helpers for zero‑shot and FT inference
- code/02_map_measurement/02_01_GLLM_Approach/02_01_04_MAP_Scoring/MAP_Scoring_GLLM_Approach_final.ipynb
  - loads `Final_Inference_results/processed/Corpus_df_HTML_cleaned_GLLM_final_shard_{i}.pkl` (and FT shards), concatenates shards and performs MAP scoring
- code/03_validation/Validation_Analyses_final.ipynb
  - loads scored outputs from GLLM/W2V/BoW and performs validation and merge for MAP‑fit analyses

## Quick notes / workflow
- To run local prompting experiments: run Prompt_Engineering_final.ipynb → results saved to `Local_prompting_results/`.
- To create OpenAI batches: run OpenAI_Inference_final.ipynb / OpenAI_Fine_Tuning_final.ipynb → JSONL in `OpenAI_batch_files/`.
- To retrieve OpenAI batch results: use retrieve_batch_results(...) in OpenAI_Inference_final.ipynb → raw JSONL in `OpenAI_results/` → parse to `OpenAI_prompting_results/`.
- To run local/SLURM inference: configure config.yaml / config_ft.yaml, run main.py (or submit SLURM scripts) → shard pickles in `Final_Inference_results/processed/` → scoring notebook concatenates shards.
