import requests
import json

# Ollama server endpoint
url = "http://localhost:11434/api/generate"

headers = {
    "Content-Type": "application/json"
}

# Request payload
data = {
    "model": "mistral",  # Change to 'mistral' or 'llama3' if needed
    "prompt": "Why is the sky blue?",
    "stream": False
}

try:
    response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)

    if response.ok:  # equivalent to status_code == 200
        response_json = response.json()
        # Some versions of Ollama return the text under 'response' or 'message'
        actual_response = response_json.get("response") or response_json.get("message", "No response key found.")
        print("✅ Response from model:")
        print(actual_response)
    else:
        print(f"❌ Error: Status code {response.status_code}")
        print(response.text)

except requests.exceptions.RequestException as e:
    print(f"🚨 Request failed: {e}")
