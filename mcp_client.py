# mcp-client.py
import requests

SERVER_URL = "http://localhost:5000/query"

def main():
    while True:
        user_input = input("🔍 Enter your search query (or 'exit'): ").strip()
        if user_input.lower() == 'exit':
            break

        response = requests.post(SERVER_URL, json={"query": user_input})
        data = response.json()

        print("\n📦 JSON Results:")
        for item in data['json_results']:
            print(" -", item)

        print("\n🤖 Azure AI Analysis:")
        for item in data.get('ai_analyses', []):
            print(f"\nEntry: {item['entry']}\nAI Analysis: {item['analysis']}")

