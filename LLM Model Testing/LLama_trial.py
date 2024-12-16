from transformers import T5ForConditionalGeneration, T5Tokenizer
from transformers import BartForConditionalGeneration, BartTokenizer
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from transformers import GPTNeoForCausalLM, GPT2Tokenizer
import json

# Define the model names and their associated classes
models = {
    'T5': {
        'model': T5ForConditionalGeneration.from_pretrained("t5-small"),
        'tokenizer': T5Tokenizer.from_pretrained("t5-small"),
    },
    'BART': {
        'model': BartForConditionalGeneration.from_pretrained("facebook/bart-large"),
        'tokenizer': BartTokenizer.from_pretrained("facebook/bart-large"),
    },
    'GPT-2': {
        'model': GPT2LMHeadModel.from_pretrained("gpt2"),
        'tokenizer': GPT2Tokenizer.from_pretrained("gpt2"),
    },
    'GPT-Neo': {
        'model': GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B"),
        'tokenizer': GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B"),
    },
}

# Load your dataset
with open('LLM_dataset.json', 'r') as f:
    dataset = json.load(f)

# Prepare a list to store the updated dataset with generated responses
updated_data = []

# Process each item in the dataset
for item in dataset:
    query = item.get("Query")
    announcement = item.get("Announcement")

    # Loop through each model
    for model_name, model_data in models.items():
        model = model_data['model']
        tokenizer = model_data['tokenizer']

        # Create the input prompt
        input_text = f"Generate a formal response for the Query, only based on the information inside Announcement:\n\nQuery: {query}\nAnnouncement: {announcement}\nResponse:"

        # Tokenize the input
        inputs = tokenizer.encode(input_text, return_tensors="pt")

        # Generate the response
        output = model.generate(inputs, max_length=250, num_return_sequences=1, no_repeat_ngram_size=2, temperature=0.7)

        # Decode the generated output
        response = tokenizer.decode(output[0], skip_special_tokens=True)

        # Extract the response part from the generated text
        if "Response:" in response:
            generated_response = response.split("Response:")[1].strip()
        else:
            generated_response = response.strip()

        # Update the item with the generated response for the current model
        item[f"Response_{model_name}"] = generated_response

    # Append the updated item to the list
    updated_data.append(item)

# Save the updated dataset with responses to a new JSON file
with open('all_models_responses.json', 'w') as f:
    json.dump(updated_data, f, indent=4)

print("Responses generated and stored in 'all_models_responses.json' successfully.")
