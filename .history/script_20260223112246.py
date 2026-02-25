import requests
import time
import pandas as pd
from dotenv import load_dotenv
import os


load_dotenv()
API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")

def get_response(model, prompt, temperature=0.7, max_tokens=300):
 
    answer = f"Simulated response for '{prompt[:50]}...'"
    return {
        "model": model,
        "prompt": prompt,
        "temperature": temperature,
        "response_time": 0.01,
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
            if result:
                print("Response time:", result["response_time"], "seconds")
                print("Answer:", result["answer"][:100], "...\n")
                results.append(result)

# Save results
df = pd.DataFrame(results)
df.to_csv("results.csv", index=False)

print("\n The results saved in csv file")