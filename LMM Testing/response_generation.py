import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from prompt_generation import PromptGenerator

# === Configuration ===
MODEL_PATH = "MySu-Chatbot/LLM/deepseek_r1_1_5b_local"
DOCUMENT_METADATA_PATH = "C:/Users/kagan_ntaijui/Desktop/MySu-Chatbot/Vector Database/Embeddings/Documents/metadata_documents.json"
ANNOUNCEMENT_METADATA_PATH = "C:/Users/kagan_ntaijui/Desktop/MySu-Chatbot/Vector Database/Embeddings/Announcements/metadata_announcements.json"

# === Load Model & Tokenizer (Once) ===
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    llm_int8_threshold=6.0
)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)

# === Generation Settings ===
gen_kwargs = {
    "max_new_tokens": 400,
    "temperature": 0.7,
    "top_p": 0.9,
    "repetition_penalty": 1.1
}

def clean_llm_response(raw_response: str) -> str:
    if "</think>" in raw_response:
        return raw_response.split("</think>")[-1].strip()
    return raw_response.strip()

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
    return {"response": clean_llm_response(response)}

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
    return {"response": clean_llm_response(response)}

def BuildResponsesNonAction(type: str, query: str) -> dict:
    generator = PromptGenerator(
        type=type,
        query=query
    )
    prompt = generator.generate_prompt()
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, **gen_kwargs)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"response": clean_llm_response(response)}

if __name__ == "__main__":
    # Example usage
    response = BuildResponsesAction(
        type="document",
        query="What is the latest news about the university?",
        retrieved_data_id="12345",
        data_status="valid"
    )
    print(response)
