"""
Fine-tuning Script for Loan Insight Assistant LLM using LoRA (Low-Rank Adaptation)
This script allows for memory-efficient fine-tuning of a base LLM (e.g., Llama-3-8B) 
using the loan application dataset.
"""

import os
import torch
import pandas as pd
from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    pipeline,
    logging,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer

# --- Configuration ---
MODEL_NAME = "meta-llama/Llama-3-8B"  # Or your choice of base model
DATASET_PATH = "hdfc_loan_dataset_full_enriched - hdfc_loan_dataset_full_enriched.csv"
OUTPUT_DIR = "./loan_assistant_lora"
LORA_R = 64
LORA_ALPHA = 16
LORA_DROPOUT = 0.1

def format_instruction(row):
    """Format a single CSV row into an instruction-response pair."""
    system_prompt = "You are a specialized Loan Analysis & Compliance Agent."
    
    # Constructing a simulated query and context from the data
    context = f"Loan Amount: {row['Loan_Amount']}, DTI: {row['Debt_to_Income_Ratio']}, CIBIL: {row['CIBIL_Score']}, Purpose: {row['Loan_Purpose']}"
    query = f"Analyze the loan application for {row['Customer_Name']}."
    
    # The "response" would ideally be a ground truth explanation, 
    # but here we use the loan status and basic notes as a proxy.
    response = f"Analysis for {row['Customer_Name']}: The loan application status is {row['Loan_Status']}. "
    response += f"Key factors: The CIBIL score is {row['CIBIL_Score']} and the Debt-to-Income ratio is {row['Debt_to_Income_Ratio']}. "
    
    formatted_text = f"<s>[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\nContext: {context}\nQuery: {query} [/INST] {response} </s>"
    return {"text": formatted_text}

def fine_tune():
    # 1. Load and Prepare Dataset
    print(f"Loading dataset from {DATASET_PATH}...")
    df = pd.read_csv(DATASET_PATH)
    
    # Convert dataframe samples to instruction format
    formatted_data = [format_instruction(row) for _, row in df.iterrows()]
    dataset = Dataset.from_list(formatted_data)
    
    # 2. BitsAndBytes Config (4-bit quantization for efficiency)
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )

    # 3. Load Model and Tokenizer
    print("Loading model and tokenizer...")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True
    )
    model.config.use_cache = False
    model.config.pretraining_tp = 1
    
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    # 4. LoRA Config
    peft_config = LoraConfig(
        lora_alpha=LORA_ALPHA,
        lora_dropout=LORA_DROPOUT,
        r=LORA_R,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj"] # Specific to Llama/Mistral
    )

    # 5. Training Arguments
    training_arguments = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=3,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        optim="paged_adamw_32bit",
        save_steps=25,
        logging_steps=25,
        learning_rate=2e-4,
        weight_decay=0.001,
        fp16=True,
        bf16=False,
        max_grad_norm=0.3,
        max_steps=-1,
        warmup_ratio=0.03,
        group_by_length=True,
        lr_scheduler_type="constant",
    )

    # 6. SFT Trainer
    print("Initializing trainer...")
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        peft_config=peft_config,
        dataset_text_field="text",
        max_seq_length=512,
        tokenizer=tokenizer,
        args=training_arguments,
        packing=False,
    )

    # 7. Start Training
    print("Starting training...")
    trainer.train()

    # 8. Save Model
    print(f"Saving fine-tuned adapter to {OUTPUT_DIR}...")
    trainer.model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print("Fine-tuning complete!")

if __name__ == "__main__":
    # Note: Requires high-memory GPU and specific libraries installed:
    # pip install transformers datasets peft trl bitsandbytes accelerate
    fine_tune()
