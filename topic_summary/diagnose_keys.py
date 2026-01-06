import os
import requests
import sys

def test_openai(key):
    print("Testing OpenAI API Key...")
    headers = {"Authorization": f"Bearer {key}"}
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json={"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "hi"}], "max_tokens": 5}
        )
        if response.status_code == 200:
            print("✅ OpenAI API Key is valid.")
        else:
            print(f"❌ OpenAI API Key failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ OpenAI API Key error: {e}")

def test_serper(key):
    print("\nTesting Serper API Key...")
    headers = {"X-API-KEY": key, "Content-Type": "application/json"}
    try:
        response = requests.post(
            "https://google.serper.dev/search",
            headers=headers,
            json={"q": "test"}
        )
        if response.status_code == 200:
            print("✅ Serper API Key is valid.")
        else:
            print(f"❌ Serper API Key failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Serper API Key error: {e}")

if __name__ == "__main__":
    openai_key = input("Enter OpenAI API Key: ").strip()
    serper_key = input("Enter Serper API Key: ").strip()
    
    if openai_key:
        test_openai(openai_key)
    if serper_key:
        test_serper(serper_key)
