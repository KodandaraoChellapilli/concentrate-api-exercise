import requests
import time
import pandas as pd
import os
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")

def get_response(model, prompt, temperature=0.7):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "input": prompt,
        "temperature": temperature
    }

    start = time.time()
    response = requests.post(API_URL, headers=headers, json=payload)
    response_time = round(time.time() - start, 2)

    if response.status_code == 200:
        data = response.json()
        try:
            answer = data["output"][0]["content"][0]["text"]
        except:
            answer = str(data)
    else:
        answer = f"Error {response.status_code}"

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

results = []

for model in models:
    for question in questions:
        print(f"Testing {model}")
        result = get_response(model, question)
        print("Status:", result["answer"][:60])
        results.append(result)

df = pd.DataFrame(results)
df.to_csv("results.csv", index=False)

print("Results saved to results.csv")