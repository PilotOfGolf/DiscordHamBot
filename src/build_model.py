import markovify
import re
import json

def clean_text(raw_text):
    text = re.sub(r'\b[AKNW]\d[A-Z]{1,3}\b', '', raw_text)
    text = re.sub(r'(Chapter|Page)\s+\d+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'http\S+', '', text)
    return text

def build_and_save_model():
    try:
        with open("brain.txt", "r", encoding="utf-8") as f:
            raw_data = f.read()

        cleaned_data = clean_text(raw_data)
        text_model = markovify.NewlineText(cleaned_data, state_size=2)

        # Save the model to JSON
        model_json = text_model.to_json()
        with open("brain_model.json", "w", encoding="utf-8") as f:
            json.dump(model_json, f, indent=2)

        print("Model built and saved to brain_model.json")

    except Exception as e:
        print(f"Error building model: {e}")

if __name__ == "__main__":
    build_and_save_model()