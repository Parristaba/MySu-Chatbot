from transformers import AutoTokenizer, AutoModelForCausalLM

# Zephyr 7B Alpha version
model_name = "HuggingFaceH4/zephyr-7b-alpha"
save_directory = r"C:\Users\kagan_ntaijui\Desktop\MySu-Chatbot\LMM Testing\Zephyr Model"

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)

tokenizer.save_pretrained(save_directory)
model.save_pretrained(save_directory)

print(f"✅ Zephyr-7B model and tokenizer downloaded to: {save_directory}")