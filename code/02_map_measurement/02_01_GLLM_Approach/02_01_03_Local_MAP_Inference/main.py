# import all necessary libraries
import argparse
import gc
import json
import os
from pathlib import Path
from huggingface_hub import login
from datasets import Dataset
import logging
import pandas as pd
import numpy as np
import json
import pickle
import re
import time
import torch
from utils import load_config, set_up_logging, initialize_GLLM_pipeline, run_batched_pipeline_interference, extract_json
import yaml

os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True' # makes the memory allocator more robust against fragmentation

def main():
    parser = argparse.ArgumentParser()    
    parser.add_argument("--num_shards", type=int, default=1)
    parser.add_argument("--shard_index", type=int, default=0)
    parser.add_argument("--resume_file", default=None)
    parser.add_argument("--output_file", required=True)
    args = parser.parse_args()

    # Load configuration file
    config = load_config()

    # Extract directory settings from config file
    huggingface_token = config["huggingface_token"]
    datasets_dir = config["datasets_dir"]
    output_dir = config["output_dir"]
    resume_dir = os.path.join(config["log_dir"],"resumes")
    transformers_cache_dir = config["transformers_cache_dir"]
    dataset_name = config["datasets_name"]
    input_column = config["input_column"]
    llm_full_output_column = config["full_output_column"]
    results_column = config["results_column"]
    

    # Extract model and inference settings from config file
    system_message = config["system_message"]
    user_message = config["user_message"]
    max_new_tokens = config["model_output_max_tokens"]
    temperature = config["model_temperature"]
    model_id = config["inference_model_name"]

    # Create output and resume directory if they do not exist
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(resume_dir, exist_ok=True)    

    # Set up logging functionality
    log_filename = set_up_logging(config,shard_id=args.shard_index)

    # Set the random seed to ensure reproducible results across different runs.
    torch.random.manual_seed(0)

    # Configure logging to write to the specified log file
    logging.basicConfig(
            format="%(asctime)s %(levelname)-8s %(message)s",
            level=logging.INFO,
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[logging.FileHandler(log_filename, mode="a")], # Append to log file
        )
    logger = logging.getLogger()

    # Log the CUDA configuration of the current run
    logger.info("PyTorch CUDA available: %s", torch.cuda.is_available())
    logger.info("CUDA version (from torch): %s", torch.version.cuda)
    logger.info("GPU name: %s", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU found")
    logger.info("Cuda device count: %d", torch.cuda.device_count())

    #Set starting batch size based on GPU type
    if "H200" in torch.cuda.get_device_name(0):
        starting_batch_size = config["H200_batch_size"]
    else:
        starting_batch_size = config["A100_batch_size"]

    # Log in to Hugging Face if token is provided
    login(token=huggingface_token)
    
    # Determine starting index from resume file
    start_index = 0
    resume_file_path = os.path.join(resume_dir, args.resume_file)
    if args.resume_file and Path(resume_file_path).exists():
        resume = json.load(open(resume_file_path))
        if resume.get("shard_index") == args.shard_index:
            start_index = resume.get("last_index", -1) + 1
    
    # Load the full dataset and create shard if start_index is 0 else load the shard from pickle file
    if start_index == 0:
        with open(os.path.join(datasets_dir, f"{dataset_name}.pkl"), "rb") as f:
            dataset = pickle.load(f)
        dataset = Dataset.from_pandas(dataset)

        shard = dataset.shard(num_shards=args.num_shards,
                          index=args.shard_index,
                          contiguous=True)
        
        del dataset
        
        #Add a column for the parsed GLLM results and prompting time
        shard = shard.add_column(results_column, [None]*len(shard))
        shard = shard.add_column("prompting_time_minutes", [None]*len(shard))

        # Save the shard as a pickle file
        shard.to_pandas().to_pickle(os.path.join(output_dir, f"{dataset_name}_shard_{args.shard_index}.pkl"))

        # Initialize a list to store the extracted results
        extracted_list = pd.Series([None]*len(shard))

        #Initialize a list to store the prompting time
        prompting_time_list = pd.Series([None]*len(shard))

    else:
        with open(os.path.join(output_dir, f"{dataset_name}_shard_{args.shard_index}.pkl"), "rb") as f:
            shard = pickle.load(f)

        # Retrieve already extracted results to continue from there
        extracted_list = pd.Series(shard[results_column])

        # Retrieve already recorded prompting times to continue from there
        prompting_time_list = pd.Series(shard["prompting_time_minutes"])

        # Convert shard to Hugging Face Dataset
        shard = Dataset.from_pandas(shard)

    # Determine device from CUDA_VISIBLE_DEVICES
    device = 0
    if "CUDA_VISIBLE_DEVICES" in os.environ:
        try:
            device = int(os.environ["CUDA_VISIBLE_DEVICES"].split(",")[0])
        except ValueError:
            device = 0

    logger.info(f"Using device {device} for inference.")
    # Initialize model pipeline

    generate_text_pipeline = initialize_GLLM_pipeline(model_id=model_id,
                                                     transformers_cache_dir=transformers_cache_dir,
                                                     device_map={"": f"cuda:{device}"},
                                                     torch_dtype=torch.float16,
                                                     max_new_tokens=max_new_tokens,
                                                     temperature=temperature
                                                     )

    
    out_f = open(args.output_file, "a", encoding="utf-8")

    # Log some information about the current shard
    logger.info(f"Processing shard {args.shard_index + 1} out of {args.num_shards} shards.")
    logger.info(f"Shard size: {len(shard)} entries.")
    logger.info(f"Starting from index: {start_index}.")

    # Iterate over the entries in the shard starting from start_index
    
    for idx in range(start_index, len(shard)):
        # Get the input text for the current entry
        text_dict = shard[idx][input_column]

        batch_size = starting_batch_size

        start_time = time.time()

        # Run the model pipeline on the input text
        while batch_size > 0:
            try:
                result = run_batched_pipeline_interference(
                    text_dict,
                    batch_size,
                    generate_text_pipeline,
                    system_message,
                    user_message,
                    llm_full_output_column
                )
                break  # success → exit loop
            except (torch.OutOfMemoryError, RuntimeError, MemoryError):
                logger.warning(f"OOM at batch size {batch_size} for entry {idx}. Retrying with {batch_size // 2}.")
                torch.cuda.empty_cache()
                gc.collect()
                batch_size //= 2

        if batch_size == 0:
            logger.error(f"Could not fit even batch size 1 on GPU. Skipping entry {idx}.")
            result = None

        # Log time taken for this entry
        time_taken = (time.time() - start_time) / 60

        logger.info(f"Completed entry {idx} in shard {args.shard_index}.")
        logger.info(f"Prompting time: {time_taken:.2f} minutes for {len(text_dict)} prompts.")

        # Save the output of the GLLM model to the output file
        if result is None:
            generated = None
        else:
            generated = result.get(llm_full_output_column, result)

        entry = {
            "shard_index": args.shard_index,
            "local_index": idx,
            "output_text": generated,
            "time_minutes": time_taken,
        }
        
        out_f.write(json.dumps(entry) + "\n")
        out_f.flush()

        # Extract the JSON part from the generated text, parse it and store it in the shard
        if generated is None:
            extracted_list[idx] = None
        else:
            extracted_list[idx] = [extract_json(out) for out in generated]

        shard = shard.remove_columns(results_column).add_column(results_column, extracted_list)

        # Store the prompting time
        prompting_time_list[idx] = time_taken

        shard = shard.remove_columns("prompting_time_minutes").add_column("prompting_time_minutes", prompting_time_list)

        # Save the shard after each entry
        shard.to_pandas().to_pickle(os.path.join(output_dir, f"{dataset_name}_shard_{args.shard_index}.pkl"))

        # Update resume file
        if resume_file_path:
            json.dump({"shard_index": args.shard_index, "last_index": idx},
                      open(resume_file_path, "w"))
    out_f.close()

if __name__ == "__main__":
    main()