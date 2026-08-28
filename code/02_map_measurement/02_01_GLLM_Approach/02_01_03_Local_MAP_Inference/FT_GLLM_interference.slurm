#!/bin/bash
#SBATCH --job-name=gllm_inference
#SBATCH --partition=gpu-single
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=2
#SBATCH --gpus-per-task=1
#SBATCH --gres=gpu:1,gpumem_per_gpu:100GB
#SBATCH --time=48:00:00
#SBATCH --mem=25gb
#SBATCH --array=0-3
#SBATCH --mail-user=!!!example@mail.com!!!
#SBATCH --mail-type=ALL
#SBATCH --output=slurm-%x-%j.out
#SBATCH --error=slurm-%x-%j.err

module load devel/cuda/12.1
module load devel/miniforge

source $MINIFORGE_HOME/etc/profile.d/conda.sh
conda activate !!!INSERTE PYTHON ENV HERE!!!

echo "============================================"
echo " SLURM Job ID: $SLURM_JOB_ID"
echo " Array Task ID (shard index): $SLURM_ARRAY_TASK_ID"
echo " Node: $SLURMD_NODENAME"
echo " CUDA_VISIBLE_DEVICES: $CUDA_VISIBLE_DEVICES"
echo "============================================"

# -----------------------
# Run  inference script -
# -----------------------
python main_ft.py \
    --num_shards 4 \
    --shard_index $SLURM_ARRAY_TASK_ID \
    --resume_file resume_ft_${SLURM_ARRAY_TASK_ID}.json \
    --output_file out_ft_${SLURM_ARRAY_TASK_ID}.jsonl

echo "Shard $SLURM_ARRAY_TASK_ID finished at $(date)"
