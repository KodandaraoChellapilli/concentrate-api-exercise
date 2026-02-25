import requests
import time
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")

if not API_KEY or not API_URL:
    raise ValueError("API_KEY or API_URL not found. Check your .env file.")

def get_response(model, prompt, temperature=0.7, max_tokens=300):
    """
    Call the Concentrate AI API and return the response.
    Falls back to a simulated response if there is an error.
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    print(f"Hitting API for model={model} prompt='{prompt[:30]}...'")
    try:
        start_time = time.time()
        response = requests.post(API_URL, headers=headers, json=payload)
        response_time = round(time.time() - start_time, 2)

        print("API responded with status code:", response.status_code)

        if response.status_code == 200:
            data = response.json()
            # Adjust key depending on the API response
            answer = data.get("answer") or data.get("text") or ""
        else:
            print(f"API Error {response.status_code}: {response.text}")
            answer = f"Simulated response for '{prompt[:50]}...'"
            response_time = 0.01

    except Exception as e:
        print("Exception calling API:", e)
        answer = f"Simulated response for '{prompt[:50]}...'"
        response_time = 0.01

    return {
        "model": model,
        "prompt": prompt,
        "temperature": temperature,
        "response_time": response_time,
        "answer_length": len(answer),
        "answer": answer
    }

# Models, questions, and temperature settings
models = [
    "openai/gpt-4.1-mini",
    "anthropic/claude-haiku-3"
]

questions = [
    "Explain supervised vs unsupervised learning.",
    "Write a Python function to reverse a string.",
    "Summarize World War 1 in 5 sentences."
]

temperatures = [0.7]
results = []

# Loop through models, questions, temperatures
for model in models:
    for question in questions:
        for temp in temperatures:
            result = get_response(model, question, temp)
            if result:
                print("Response time:", result["response_time"], "seconds")
                print("Answer:", result["answer"][:100], "...\n")
                results.append(result)

# Save results to CSV
df = pd.DataFrame(results)
df.to_csv("results.csv", index=False)
print("\nResults saved to results.csv")