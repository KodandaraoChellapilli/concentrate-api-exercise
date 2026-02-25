import requests
import time
import pandas as pd
from dotenv import load_dotenv
import os


load_dotenv()
API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")

def get_response(model, prompt, temperature=0.7, max_tokens=300):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "input": prompt,
        "temperature": temperature,
        "max_output_tokens": max_tokens  
    }

    start_time = time.time()
    response = requests.post(API_URL, headers=headers, json=payload)
    response_time = round(time.time() - start_time, 2)

    if response.status_code == 200:
        try:
            data = response.json()
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

temperatures = [0.7]

results = []


for model in models:
    for question in questions:
        for temp in temperatures:
            print(f"\nTesting {model} | Temp={temp}")
            result = get_response(model, question, temp)
            print("Response time:", result["response_time"], "seconds")
            print("Answer:", result["answer"][:100], "...\n")
            results.append(result)

df = pd.DataFrame(results)
df.to_csv("results.csv", index=False)

print("\nThe results saved in csv file")