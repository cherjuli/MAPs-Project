import gc
import yaml
import logging
import os
from datetime import datetime
import re
import json
import torch
from transformers import AutoModelForCausalLM, BitsAndBytesConfig, AutoTokenizer, pipeline

def load_config(config_file="./config_ft.yaml"):
    """
    Load the configuration file which is stored in YAML format.
    """
    with open(config_file, "r") as file:
        return yaml.safe_load(file)
    
def set_up_logging(config,shard_id=None):
    """
    Set up a logging function to track the GLLM process using the "logging" library.
    """
    log_dir = config["log_dir"]
    # Create a directory for the logging of the current slurm job if it doesn't exist
    today = datetime.now().strftime("%Y-%m-%d")
    log_subdir = os.path.join(log_dir, today, f"shard_{shard_id}" if shard_id is not None else "single_run")
    os.makedirs(log_subdir, exist_ok=True)

    # Create a new log file (name is based on the current timestamp)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(log_subdir, f"log_{timestamp}.log")

    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(log_filename, mode="a")  # Append to log file
        ],
    )

    # Log configuration of the current run
    config_str = "\n".join(f"{key}: {value}" for key, value in config.items())

    logging.info(
        f"Starting GLLM run on shard {shard_id} with the following configuration:\n{config_str}")
    
    return log_filename

def initialize_GLLM_pipeline(fine_tuned_model_dir, device_map, torch_dtype=torch.float16, max_new_tokens=100, temperature=0.001):
    """
    Initialize the text generation pipeline using a specified model from Hugging Face.
    """
    tokenizer = AutoTokenizer.from_pretrained(fine_tuned_model_dir)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.pad_token_id = tokenizer.eos_token_id
    tokenizer.padding_side = "left" # important for batching since Llama is a decoder-only architecture

    # Load model and tokenizer
    model = AutoModelForCausalLM.from_pretrained(
        fine_tuned_model_dir,
        device_map=device_map,
        dtype=torch_dtype,
        trust_remote_code=True,
        _attn_implementation="flash_attention_2"
    )
    
    # Create text generation pipeline
    generate_text_pipeline = pipeline(
        task="text-generation",
        model=model,
        tokenizer=tokenizer,
        return_full_text=True,
        do_sample=True,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
    )

    return generate_text_pipeline

def run_batched_pipeline_interference(batch, batch_size, generate_text_pipeline, output_column):

    sentences = batch['Sentence']

    messages_batch = [
        [
            {"role": "user", "content": f"Text:\n{sentence}"}
        ]
        for sentence in sentences
    ]

    responses = generate_text_pipeline(messages_batch, batch_size=batch_size)

    #free gpu memory
    gc.collect()
    torch.cuda.empty_cache()

    return {output_column: [response[0]['generated_text'][-1]['content'].strip() for response in responses]}

def extract_json(row):
    """
    Extracts MAP classification fields from LLM output.
    If parsing fails, returns None for all and prints the problematic LLM output.
    """

    try:
        json_match = re.search(r'\{.*?\}', row, re.DOTALL)

        if not json_match:
            print("Failed to extract JSON from LLM output:\n", row)
            return {
                "LLM_Explicit_MAP_referral": None,
                "LLM_Implicit_MAP_referral": None,
                "LLM_Dimension": None,
                "LLM_Confidence_Score": None
            }

        # Parse JSON
        json_str = json_match.group(0)
        result = json.loads(json_str)

        # Ensure the probability is an integer between 0 and 100
        probability = int(result["Confidence_Score"])
        if not (0 <= probability <= 100):
            raise ValueError("Confidence_Score is out of range")

        # Normalize values
        def normalize(value):
            if isinstance(value, str):
                value = value.strip()
                if value.lower() in ["n/a", "", "na", "none", "nan"]:
                    return None
            return value

        return {
            "LLM_Explicit_MAP_referral": normalize(result.get("Explicit_MAP_referral")).capitalize() if normalize(result.get("Explicit_MAP_referral")) else None,
            "LLM_Implicit_MAP_referral": normalize(result.get("Implicit_MAP_referral")).capitalize() if normalize(result.get("Implicit_MAP_referral")) else None,
            "LLM_Dimension": normalize(result.get("Dimension")),
            "LLM_Confidence_Score": probability
        }

    except Exception as e:
        print(f"Error parsing JSON: {e}\nLLM Output:\n{row}\n")
        return {
            "LLM_Explicit_MAP_referral": None,
            "LLM_Implicit_MAP_referral": None,
            "LLM_Dimension": None,
            "LLM_Confidence_Score": None
        }