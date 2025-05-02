import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from Web_Application.Helper_Modules.LLM.prompt_generation import PromptGenerator
import psutil
import re

# === Configuration ===
MODEL_PATH = r"C:\Users\kagan_ntaijui\Desktop\MySu-Chatbot\LL_Models\Zephyr_Model"
DOCUMENT_METADATA_PATH = "C:/Users/kagan_ntaijui/Desktop/MySu-Chatbot/Vector_Database/Embeddings/Documents/metadata_documents.json"
ANNOUNCEMENT_METADATA_PATH = "C:/Users/kagan_ntaijui/Desktop/MySu-Chatbot/Vector_Database/Embeddings/Announcements/metadata_announcements.json"

# === Load Model & Tokenizer (Once) ===
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token  # Ensure padding token is set

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
    "max_new_tokens": 250,      
    "temperature": 0.1,         
    "top_p": 0.85,
    "repetition_penalty": 1.2,
    "do_sample": True,
    "num_beams": 2,
    "early_stopping": True
}

# === Utility ===
def format_response(text: str, title: str = "", hyperlink: str = "") -> str:
    """Ensure response is properly formatted with 4-5 sentences and has a hyperlink"""
    
    # Clean up the response
    text = text.strip()
    
    # If response is extremely short or contains placeholder text, return a default
    if len(text) < 10 or "..." in text or text == "":
        return "I apologize, but I couldn't generate a proper response. Please try rephrasing your question."
    
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    # Filter out empty sentences
    sentences = [s for s in sentences if len(s.strip()) > 0]
    
    # Fix sentence count issues
    if len(sentences) > 5:
        sentences = sentences[:5]
    
    # Remove any sentences that might contain hyperlinks to avoid duplication
    sentences = [s for s in sentences if not ("visit" in s.lower() and ("http" in s.lower() or "www" in s.lower()))]
    
    # Create the final response text
    response_text = " ".join(sentences)
    
    # Append hyperlink if provided
    if hyperlink:
        response_text = response_text.rstrip(".!?") + ". "  # Ensure proper sentence ending
        response_text += f"For more information, visit: {hyperlink}"
    
    return response_text

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
    
    # Generate response
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, **gen_kwargs)
    response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract assistant's response (everything after "ASSISTANT: ")
    assistant_text = ""
    if "ASSISTANT: " in response_text:
        assistant_text = response_text.split("ASSISTANT: ", 1)[1].strip()
    else:
        assistant_text = response_text.strip()
    
    # Get hyperlink information
    hyperlink = ""
    title = ""
    if type == "document" and generator.metadata:
        chunks = [entry for entry in generator.metadata.values() if entry.get("doc_id") == retrieved_data_id]
        if chunks:
            hyperlink = chunks[0].get("hyperlink", "")
            title = chunks[0].get("title", "")
    
    # Format and clean up the response
    final_response = format_response(assistant_text, title, hyperlink)
    
    return {
        "response": final_response,
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
    
    # Generate response
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, **gen_kwargs)
    response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract assistant's response
    assistant_text = ""
    if "ASSISTANT: " in response_text:
        assistant_text = response_text.split("ASSISTANT: ", 1)[1].strip()
    else:
        assistant_text = response_text.strip()
    
    # Get hyperlink information
    hyperlink = ""
    title = ""
    if retrieved_data_id and generator.metadata:
        chunks = [entry for entry in generator.metadata.values() if entry.get("doc_id") == retrieved_data_id]
        if chunks:
            hyperlink = chunks[0].get("hyperlink", "")
            title = chunks[0].get("title", "")
    
    # Format and clean up
    final_response = format_response(assistant_text, title, hyperlink)
    
    return {
        "response": final_response,
    }

def BuildResponsesNonAction(type: str, query: str) -> dict:
    generator = PromptGenerator(
        type=type,
        query=query
    )
    
    prompt = generator.generate_prompt()
    
    # Generate response
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, **gen_kwargs)
    response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract assistant's response
    assistant_text = ""
    if "ASSISTANT: " in response_text:
        assistant_text = response_text.split("ASSISTANT: ", 1)[1].strip()
    else:
        assistant_text = response_text.strip()
    
    return {
        "response": assistant_text,
    }

if __name__ == "__main__":
    # Example usage
    result = BuildResponsesAction(
        type="announcement",    
        query="Are the applications open for Summer 2025 Internships?",
        retrieved_data_id="announcement_003",
        data_status="confident"
    )
    print(result)