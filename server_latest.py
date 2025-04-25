import os
import openai
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Azure OpenAI configuration
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")  # e.g., https://your-resource-name.openai.azure.com/
openai.api_version = "2023-05-15"
openai.api_key = os.getenv("AZURE_OPENAI_KEY")
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")  # The deployment name of your model (not the model name)

# Load data from JSON
with open('data.json', 'r') as f:
    json_data = json.load(f)

@app.route('/query', methods=['POST'])
def query():
    input_text = request.json.get("query", "").lower()

    # Search JSON data for matching entries
    json_results = [entry for entry in json_data if input_text in json.dumps(entry).lower()]
    error_analyses = []

    for entry in json_results:
        # Treat "running" as a suspicious state for demo purposes
        if entry.get("status") == "running":
            prompt = f"Analyze this server status: {entry}"

            try:
                response = openai.ChatCompletion.create(
                    engine=DEPLOYMENT_NAME,  # Azure requires deployment name, not model name
                    messages=[
                        {"role": "system", "content": "You are a server incident analyst."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                    max_tokens=150
                )
                analysis = response['choices'][0]['message']['content']
                error_analyses.append({
                    "entry": entry,
                    "analysis": analysis
                })
            except Exception as e:
                error_analyses.append({
                    "entry": entry,
                    "analysis": f"Failed to analyze due to: {str(e)}"
                })

    return jsonify({
        "json_results": json_results,
        "ai_analyses": error_analyses
    })

if __name__ == '__main__':
    app.run(debug=True)
