# generate_responses.py

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from Web_Application.Helper_Modules.LLM.prompt_generation import PromptGenerator
import psutil
import re

# === Configuration ===
MODEL_PATH = r"C:\Users\kagan_ntaijui\Desktop\MySu-Chatbot\LL_Models\Zephyr_Model"
DOCUMENT_METADATA_PATH = "C:/Users/kagan_ntaijui/Desktop/MySu-Chatbot/Vector_Database/Embeddings/Documents/metadata_documents.json"
ANNOUNCEMENT_METADATA_PATH = "C:/Users/kagan_ntaijui/Desktop/MySu-Chatbot/Vector_Database/Embeddings/Announcements/metadata_announcements.json"

# === Load Model & Tokenizer Globally ===
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token

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
response_gen_kwargs = {
    "max_new_tokens": 250,
    "temperature": 0.1,
    "top_p": 0.85,
    "repetition_penalty": 1.2,
    "do_sample": True,
    "num_beams": 2,
    "early_stopping": True
}

check_gen_kwargs = {
    "max_new_tokens": 20,
    "temperature": 0.0,
    "top_p": 0.9,
    "do_sample": False,
    "num_beams": 1,
    "early_stopping": True
}

# === Utility ===
def format_response(text: str, title: str = "", hyperlink: str = "") -> str:
    text = text.strip()
    if len(text) < 10 or "..." in text or text == "":
        return "I apologize, but I couldn't generate a proper response. Please try rephrasing your question."
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s for s in sentences if len(s.strip()) > 0]
    if len(sentences) > 5:
        sentences = sentences[:5]
    sentences = [s for s in sentences if not ("visit" in s.lower() and ("http" in s.lower() or "www" in s.lower()))]
    response_text = " ".join(sentences)
    if hyperlink:
        response_text = response_text.rstrip(".!?") + ". "
        response_text += f"For more information, visit: {hyperlink}"
    return response_text


def validate_document_relevance(query: str, passage: str) -> bool:
    """
    Check if a document is relevant to a query using a simplified prompt approach
    that works for any type of document/query pair.
    """
    # Ensure passage isn't too long
    if len(passage) > 2000:
        passage = passage[:2000]
    
    # Create a simpler prompt that doesn't contain the word "document" in the instructions
    # to avoid the model repeating that word in its output
    prompt = (
        f"USER: Determine if the following text contains information that would help answer the question. "
        f"Reply with just 'YES' or 'NO'.\n\n"
        f"TEXT: {passage.strip()}\n\n"
        f"QUESTION: {query.strip()}\n\n"
        f"ASSISTANT:"
    )
    
    print("-----------------------------")
    print(f"[DEBUG] Validation prompt: '{prompt}'")
    print("-----------------------------")
    
    # Generate response
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    try:
        # Override generation parameters completely for this validation function
        outputs = model.generate(
            **inputs,
            max_new_tokens=5,
            temperature=0.0,
            top_k=1,            # Only consider the most likely token
            do_sample=False,    # Deterministic generation
            num_beams=1,
            repetition_penalty=1.5  # Discourage repetitions from input
        )
        
        # Get model's response
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract just the model's answer after "ASSISTANT:"
        if "ASSISTANT:" in response:
            response = response.split("ASSISTANT:", 1)[1]
        
        # Clean up the response
        response = response.strip().lower()
        print(f"[DEBUG] Validation raw response: '{response}'")
        
        # Look at just the first word
        first_word = response.split()[0] if response.split() else ""
        
        # Determine result based on first word only
        if first_word == "yes":
            is_relevant = True
        elif first_word == "no":
            is_relevant = False
        else:
            # If the model didn't respond with yes/no, check for yes/no anywhere in the response
            is_relevant = "yes" in response and "no" not in response
        
        print(f"[DEBUG] Is document relevant: {is_relevant}")
        return is_relevant
        
    except Exception as e:
        print(f"[ERROR] Error during validation: {e}")
        # In case of error, default to showing the result
        return True


def extract_context_passage(generator, truncate: bool = False, max_words: int = 250) -> str:
    """
    Returns the retrieved passage (announcement body or concatenated document chunks) for LLM validation.
    If truncate=True, the returned passage is capped to max_words.
    """
    try:
        if not generator.metadata:
            print(f"[WARNING] No metadata available for {generator.type}")
            return ""
            
        if generator.type == "announcement":
            # Match announcement by ID field
            match = next((a for a in generator.metadata.values() if a.get("id") == generator.retrieved_data_id), None)
            if not match:
                print(f"[WARNING] No announcement found with ID: {generator.retrieved_data_id}")
                return ""
            content = match.get("body", "")
            print(f"[DEBUG] Found announcement content: {content[:100]}...")
        
        elif generator.type == "document":
            # Match document chunks by doc_id and sort by chunk_index
            chunks = [entry for entry in generator.metadata.values() if entry.get("doc_id") == generator.retrieved_data_id]
            if not chunks:
                print(f"[WARNING] No document chunks found with ID: {generator.retrieved_data_id}")
                return ""
                
            chunks = sorted(chunks, key=lambda x: x.get("chunk_index", 0))
            content = "\n".join(chunk.get("chunk_text", "") for chunk in chunks)
            print(f"[DEBUG] Found document content: {content[:100]}...")
        
        else:
            print(f"[WARNING] Unsupported type for context extraction: {generator.type}")
            return ""

        content = content.strip()
        
        if truncate and content:
            words = content.split()
            content = " ".join(words[:max_words])
            print(f"[DEBUG] Truncated to {len(words[:max_words])} words")

        return content
        
    except Exception as e:
        print(f"[ERROR] Exception in extract_context_passage: {e}")
        return ""


def generate_no_match_response(query: str) -> str:
    """
    Generates a polite fallback response using the LLM when no relevant document is found.
    """
    prompt = (
        f"You are a helpful assistant for Sabancı University.\n\n"
        f"The user asked: \"{query}\"\n\n"
        f"IMPORTANT INSTRUCTION: You have NO information about this topic in your knowledge base.\n"
        f"You MUST acknowledge that you cannot answer this question.\n"
        f"DO NOT attempt to provide any specific information about Sabancı University policies, programs, people, or services.\n" 
        f"Choose one of these exact responses and do not deviate:\n"
        f"1. I'm sorry, but I don't have information about that. Please contact the relevant department at Sabancı University for assistance.\n"
        f"2. I don't have enough information to answer your question about that. You may want to check the official Sabancı University website or contact the appropriate office directly.\n"
        f"3. I apologize, but I cannot provide information on this topic as it's not in my knowledge base. Please refer to official Sabancı University resources for accurate information.\n\n"
        f"ASSISTANT:"
    )


    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    try:
        outputs = model.generate(**inputs, **response_gen_kwargs)
        response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extract clean assistant response
        assistant_text = response_text.split("ASSISTANT:", 1)[-1].strip()

        # Append university fallback link
        if not assistant_text.endswith("."):
            assistant_text += "."
        assistant_text += " You can check https://mysu.sabanciuniv.edu/ for the information you are looking for."

        return assistant_text

    except Exception as e:
        print(f"[ERROR] Exception during fallback response generation: {e}")
        return (
            "I couldn't find any specific information about that right now. "
            "You can check https://mysu.sabanciuniv.edu/ for more details."
        )


def BuildResponsesAction(type: str, query: str, retrieved_data_id: str, data_status: str) -> dict:
    print(f"[DEBUG] BuildResponsesAction called with type={type}, query='{query}', retrieved_data_id={retrieved_data_id}")
    
    metadata_path = None
    if type == "document":
        metadata_path = DOCUMENT_METADATA_PATH
    elif type == "announcement":
        metadata_path = ANNOUNCEMENT_METADATA_PATH
    
    if metadata_path:
        print(f"[DEBUG] Using metadata path: {metadata_path}")
    
    generator = PromptGenerator(
        type=type,
        query=query,
        retrieved_data_id=retrieved_data_id,
        data_status=data_status,
        document_metadata_path=metadata_path
    )

    # 🔍 Extract retrieved content for validation 
    passage = extract_context_passage(generator, truncate=True, max_words=300)
    
    # If no passage was found, return a default response
    if not passage:
        print("[DEBUG] No relevant passage found in documents")
        return {
            "response": "I couldn't find any information related to your question. Please try rephrasing or check the Student Resources page."
        }

    print(f"[DEBUG] Extracted passage for validation (first 100 chars): {passage[:100]}...")
    print(f"[DEBUG] Passage length: {len(passage)} characters")

    # ❌ If validator fails, do not proceed to response generation
    if not validate_document_relevance(query, passage):
        print("[DEBUG] Document validation failed - content not relevant to query")
        fallback_response = generate_no_match_response(query)
        return {
            "response": fallback_response
        }


    print("[DEBUG] Document validation passed - proceeding with response generation")
    
    # ✅ Proceed with full prompt generation and response
    prompt = generator.generate_prompt()
    print(f"[DEBUG] Generated prompt (first 100 chars): {prompt[:100]}...")
    
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    try:
        outputs = model.generate(**inputs, **response_gen_kwargs)
        response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract assistant's response
        if "ASSISTANT: " in response_text:
            assistant_text = response_text.split("ASSISTANT: ", 1)[1].strip()
        else:
            assistant_text = response_text.strip()
            
        print(f"[DEBUG] Raw response (first 100 chars): {assistant_text[:100]}...")

        hyperlink, title = "", ""
        if type == "document" and generator.metadata:
            chunks = [entry for entry in generator.metadata.values() if entry.get("doc_id") == retrieved_data_id]
            if chunks:
                hyperlink = chunks[0].get("hyperlink", "")
                title = chunks[0].get("title", "")
                print(f"[DEBUG] Found document metadata: title='{title}', hyperlink='{hyperlink}'")

        final_response = format_response(assistant_text, title, hyperlink)
        print(f"[DEBUG] Final formatted response (first 100 chars): {final_response[:100]}...")
        
        return {
            "response": final_response
        }
        
    except Exception as e:
        print(f"[ERROR] Exception during response generation: {e}")
        return {
            "response": "I'm sorry, I encountered an error while processing your question. Please try again later."
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
    outputs = model.generate(**inputs, **response_gen_kwargs)
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
    outputs = model.generate(**inputs, **response_gen_kwargs)
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