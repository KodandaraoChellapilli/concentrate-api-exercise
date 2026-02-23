# Concentrate AI API Exercise

This project tests the Concentrate AI API using **two providers**: OpenAI and Anthropic. It loops through multiple questions and temperatures, prints simulated responses, and saves results to a CSV file.

> **Note:** Responses are simulated because my free $10 credits are not enough to run real API calls. The script is ready to use with real API calls if more credits are available.

## Files

- `script.py` – Main Python script
- `results.csv` – CSV file with results
- `.env file` – Example environment file for API key and URL

## How to Run

1. Create a `.env` file with your API key and URL:

API_KEY=your_concentrate_api_key
API_URL=https://api.concentrate.ai/v1/responses

2. Install dependencies:

3. Run the script:

4. Open `results.csv` to see the output.

## Features

- Loops through multiple questions
- Uses OpenAI and Anthropic
- Tests different temperature settings
- Saves results to CSV
- Simple, easy-to-read Vinnie-style code
