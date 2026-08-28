# 02_map_measurement

This folder contains the MAP measurement workflows for GLLM, W2V, and BoW approaches.

## Directory structure

### `02_01_GLLM_Approach/`
End-to-end generative LLM workflow.

- `02_01_01_Prompt_Engineering/`
  - `Prompt_Engineering_final.ipynb`: local prompt/model benchmarking for MAP classification.
  - `OpenAI_Inference_final.ipynb`: OpenAI model inference experiments.
- `02_01_02_Fine_Tuning/`
  - `Local_Fine_Tuning_final.ipynb`: local LoRA fine-tuning workflow.
  - `OpenAI_Fine_Tuning_final.ipynb`: OpenAI fine-tuning workflow.
- `02_01_03_Local_MAP_Inference/`
  - `main.py`: local base-model inference pipeline with sharding/resume support.
  - `main_ft.py`: local fine-tuned-model inference pipeline with sharding/resume support.
  - `utils.py`, `utils_ft.py`: helper functions for loading config, model init, prompting, and parsing.
  - `config.yaml`, `config_ft.yaml`: path/model/prompt/runtime settings.
  - `GLLM_interference.slurm`, `FT_GLLM_interference.slurm`: SLURM job scripts.
  - `run_GLLM_inference.sh`, `run_FT_GLLM_inference.sh`: helper scripts to submit jobs and connect to remote Jupyter.
- `02_01_04_MAP_Scoring/`
  - `MAP_Scoring_GLLM_Approach_final.ipynb`: converts GLLM outputs into MAP scores.

### `02_02_W2V_Approach/`
- `MAP_Survey_Analysis_final.ipynb`: MAP survey analysis and word/phrase selection.
- `MAP_Scoring_W2V_Approach_final.ipynb`: W2V-based MAP scoring.

### `02_03_BoW_Approach/`
- `MAP_Scoring_BoW_Approach_final.ipynb`: BoW-based MAP scoring.

## Suggested run order

### GLLM route
1. `02_01_GLLM_Approach/02_01_01_Prompt_Engineering/Prompt_Engineering_final.ipynb`
2. `02_01_GLLM_Approach/02_01_01_Prompt_Engineering/OpenAI_Inference_final.ipynb` (optional, OpenAI route)
3. `02_01_GLLM_Approach/02_01_02_Fine_Tuning/Local_Fine_Tuning_final.ipynb` or `OpenAI_Fine_Tuning_final.ipynb` (optional)
4. `02_01_GLLM_Approach/02_01_03_Local_MAP_Inference/` scripts (`config*.yaml` -> `main.py`/`main_ft.py` via SLURM scripts)
5. `02_01_GLLM_Approach/02_01_04_MAP_Scoring/MAP_Scoring_GLLM_Approach_final.ipynb`

### W2V route
1. `02_02_W2V_Approach/MAP_Survey_Analysis_final.ipynb`
2. `02_02_W2V_Approach/MAP_Scoring_W2V_Approach_final.ipynb`

### BoW route
1. `02_03_BoW_Approach/MAP_Scoring_BoW_Approach_final.ipynb`
