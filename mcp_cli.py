import requests

SERVER_URL = "http://localhost:5000/query"  # Your Flask server address

def main():
    print("🔌 MCP CLI Interface")
    print("Type a query (or 'exit' to quit):\n")

    while True:
        user_input = input("🧠 > ")

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        try:
            response = requests.post(
                SERVER_URL,
                json={"input": user_input}
            )
            response.raise_for_status()
            data = response.json()

            print("\n🔍 LLM Interpretation:")
            print(data.get('llm_interpretation', 'N/A'))

            print("\n📡 MCP Response:")
            print(data.get('mcp_response', 'N/A'))

            print("\n📁 File Search Result:")
            for line in data.get('file_search', []):
                print(f"  → {line}")

            print("\n" + "-" * 40)

        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    main()

