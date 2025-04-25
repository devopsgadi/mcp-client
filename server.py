from flask import Flask, request, jsonify
import openai
import requests
import os

# Optional: Use config file
try:
    import config
    openai.api_key = config.OPENAI_API_KEY
    MCP_API_URL = config.MCP_API_URL
except:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    MCP_API_URL = os.getenv("MCP_API_URL")

app = Flask(__name__)

# 🔍 Interpret user input with LLM
def interpret_with_llm(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a command interpreter."},
                {"role": "user", "content": user_input}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"LLM Error: {str(e)}"

# 📡 Mock MCP Server call
def send_to_mcp(query):
    try:
        response = requests.post(MCP_API_URL, json={'query': query})
        return response.json()
    except Exception as e:
        return {"error": f"MCP connection failed: {str(e)}"}

# 📁 File-based search fallback
def search_file(keyword):
    results = []
    try:
        with open('sample.txt', 'r') as f:
            for line in f:
                if keyword.lower() in line.lower():
                    results.append(line.strip())
    except FileNotFoundError:
        return ["sample.txt not found."]
    return results

@app.route('/query', methods=['POST'])
def handle_query():
    user_input = request.json.get('input', '').strip()

    if not user_input:
        return jsonify({'error': 'Empty input'}), 400

    # Step 1: Interpret with LLM
    interpreted_query = interpret_with_llm(user_input)

    # Step 2: Try MCP (can be logic based on query intent)
    mcp_response = send_to_mcp(interpreted_query)

    # Step 3: Fallback or also search local file
    file_results = search_file(interpreted_query)

    return jsonify({
        'llm_interpretation': interpreted_query,
        'mcp_response': mcp_response,
        'file_search': file_results
    })

if __name__ == '__main__':
    app.run(port=5000)

