import requests
import time
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")

if not API_KEY or not API_URL:
    raise ValueError("API_KEY or API_URL not found. Check your .env file.")

def get_response(model, prompt, temperature=0.7):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # ✅ Correct format for /v1/responses
    payload = {
        "model": model,
        "input": prompt,
        "temperature": temperature
    }

    print(f"Hitting API for model={model} prompt='{prompt[:30]}...'")

    start_time = time.time()
    response = requests.post(API_URL, headers=headers, json=payload)
    response_time = round(time.time() - start_time, 2)

    print("Status Code:", response.status_code)

    if response.status_code == 200:
        data = response.json()

        # Most Responses APIs return output as:
        # data["output"][0]["content"][0]["text"]
        try:
            answer = data["output"][0]["content"][0]["text"]
        except Exception:
            answer = str(data)

    else:
        print("Error:", response.text)
        answer = f"ERROR: {response.status_code}"
        response_time = 0.01

    return {
        "model": model,
        "prompt": prompt,
        "temperature": temperature,
        "response_time": response_time,
        "answer_length": len(answer),
        "answer": answer
    }


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

for model in models:
    for question in questions:
        for temp in temperatures:
            result = get_response(model, question, temp)
            print("Response time:", result["response_time"], "seconds")
            print("Answer:", result["answer"][:100], "...\n")
            results.append(result)

df = pd.DataFrame(results)
df.to_csv("results.csv", index=False)

print("\nResults saved to results.csv")