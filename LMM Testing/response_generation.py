import os
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from prompt_generation import LLMInfo, PromptGenerator
from transformers import BitsAndBytesConfig

# Paths
model_path = "MySu-Chatbot/LLM/deepseek_r1_1_5b_local"
test_set_path = "MySu-Chatbot/LLM/LLM_test_set.json"
output_path = "MySu-Chatbot/LLM/LLM_test_set_it_3.json"

print(f"CUDA is available: {torch.cuda.is_available()}")

# Load model and tokenizer
print("Loading model and tokenizer from local path...")
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)


bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    llm_int8_threshold=6.0
)

model = AutoModelForCausalLM.from_pretrained(
    model_path,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)


# Load test set
print("Loading test set...")
with open(test_set_path, 'r', encoding='utf-8') as f:
    test_cases = json.load(f)

# Prepare results
completed_cases = []

# Settings for generation
gen_kwargs = {
    "max_new_tokens": 400,
    "temperature": 0.7,
    "top_p": 0.9,
    "repetition_penalty": 1.1
}

def clean_llm_response(raw_response: str) -> str:
    if '</think>' in raw_response:
        return raw_response.split('</think>')[-1].strip()
    else:
        return raw_response.strip()


print("Generating responses...")
for idx, entry in enumerate(test_cases):
    print(f"Processing case {idx+1}/{len(test_cases)}...")
    try:
        # Create LLMInfo object
        llm_info = LLMInfo(
            type=entry.get("type"),
            query=entry.get("query"),
            retrieved_document=entry.get("retrieved_document"),
            past_interactions=entry.get("past_interactions", []),
            time_status=entry.get("time_status"),
            data_status=entry.get("data_status")
        )

        # Generate prompt
        generator = PromptGenerator(llm_info)
        prompt = generator.generate_prompt()

        # Tokenize and generate
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        outputs = model.generate(**inputs, **gen_kwargs)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = clean_llm_response(response)

        # Append response
        entry["llm_response"] = response

    except Exception as e:
        print(f"Error processing case {idx+1}: {e}")
        entry["llm_response"] = "Error generating response."

    completed_cases.append(entry)

# Save updated test set
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(completed_cases, f, indent=4, ensure_ascii=False)

print(f"All responses generated and saved to {output_path}.")