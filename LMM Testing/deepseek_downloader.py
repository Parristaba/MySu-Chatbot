from transformers import AutoTokenizer, AutoModelForCausalLM

# Specify the model you want
model_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
save_directory = "./deepseek_r1_1_5b_local"  # Local folder to save the model

# Load the model and tokenizer from Huggingface (it will download automatically)
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)

# Save the model and tokenizer to a local directory
tokenizer.save_pretrained(save_directory)
model.save_pretrained(save_directory)

print(f"Model and tokenizer downloaded and saved to {save_directory}")
