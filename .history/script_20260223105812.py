import requests
import time
import pandas as pd



def get_response(model, prompt, temperature=0.7, max_tokens=100):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "input": prompt,
        "temperature": temperature,
        "max_output_tokens": max_tokens
    }

    start_time = time.time()
    response = requests.post(API_URL, headers=headers, json=data)
    end_time = time.time()

    if response.status_code != 200:
        print("Error:", response.text)
        return None

    response_json = response.json()
    answer_text = response_json.get("output_text", "No output returned")

    return {
        "model": model,
        "prompt": prompt,
        "temperature": temperature,
        "response_time": round(end_time - start_time, 2),
        "answer_length": len(answer_text),
        "answer": answer_text
    }

# Use two providers with models that exist and work
models = [
    "openai/gpt-4.1-mini",
    "anthropic/claude-haiku-3"
]

# Only one question to stay within $10 free credits
questions = ["Explain supervised vs unsupervised learning."]

# Single temperature to reduce requests
temperatures = [0.7]

results = []

for model in models:
    for question in questions:
        for temp in temperatures:
            print(f"\nTesting {model} | Temp={temp}")
            result = get_response(model, question, temp)
            if result:
                print("Response time:", result["response_time"], "seconds")
                print("Answer:", result["answer"][:200], "...\n")
                results.append(result)

# Save results
df = pd.DataFrame(results)
df.to_csv("results.csv", index=False)

print("\n✅ Done! Results saved to results.csv")