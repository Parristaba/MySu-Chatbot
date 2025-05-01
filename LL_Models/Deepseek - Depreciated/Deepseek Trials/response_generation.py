import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from prompt_builder import PromptGenerator
import psutil

# === Configuration ===
MODEL_PATH = r"C:\Users\kagan_ntaijui\Desktop\MySu-Chatbot\LMM Testing\Deepseek Model"
DOCUMENT_METADATA_PATH = "C:/Users/kagan_ntaijui/Desktop/MySu-Chatbot/Vector Database/Embeddings/Documents/metadata_documents.json"
ANNOUNCEMENT_METADATA_PATH = "C:/Users/kagan_ntaijui/Desktop/MySu-Chatbot/Vector Database/Embeddings/Announcements/metadata_announcements.json"

# === Load Model & Tokenizer (Once) ===
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    llm_int8_threshold=6.0,
    bnb_4bit_compute_dtype=torch.float16
)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)

# === Generation Settings ===
gen_kwargs = {
    "max_new_tokens": 2000,
    "temperature": 0.5,
    "top_p": 0.9,
    "repetition_penalty": 1.1
}

# === Utility ===
def get_memory_usage() -> str:
    mem = psutil.virtual_memory()
    used_gb = (mem.total - mem.available) / (1024 ** 3)
    total_gb = mem.total / (1024 ** 3)
    return f"RAM usage: {used_gb:.2f} GB / {total_gb:.2f} GB"

# === Public Functions ===
def BuildResponsesAction(type: str, query: str, retrieved_data_id: str, data_status: str) -> dict:
    metadata_path = DOCUMENT_METADATA_PATH if type == "document" else ANNOUNCEMENT_METADATA_PATH if type == "announcement" else None
    generator = PromptGenerator(
        type=type,
        query=query,
        retrieved_data_id=retrieved_data_id,
        data_status=data_status,
        document_metadata_path=metadata_path
    )
    prompt = generator.generate_prompt()
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, **gen_kwargs)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {
        "response": response.strip(),
        "memory": get_memory_usage()
    }

def BuildResponsesFollowUp(type: str, query: str, retrieved_data_id: str, data_status: str) -> dict:
    metadata_path = DOCUMENT_METADATA_PATH if type == "document" else ANNOUNCEMENT_METADATA_PATH if type == "announcement" else None
    generator = PromptGenerator(
        type="followup",
        query=query,
        retrieved_data_id=retrieved_data_id,
        data_status=data_status,
        document_metadata_path=metadata_path
    )
    prompt = generator.generate_prompt()
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, **gen_kwargs)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {
        "response": response.strip(),
        "memory": get_memory_usage()
    }

def BuildResponsesNonAction(type: str, query: str) -> dict:
    generator = PromptGenerator(
        type=type,
        query=query
    )
    prompt = generator.generate_prompt()
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, **gen_kwargs)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {
        "response": response.strip(),
        "memory": get_memory_usage()
    }

if __name__ == "__main__":
    # Example usage
    result = BuildResponsesAction(
        type="document",
        query="How to apply for semester leave as an undergraduate student?",
        retrieved_data_id="document_008",
        data_status="valid"
    )
    print(result)
