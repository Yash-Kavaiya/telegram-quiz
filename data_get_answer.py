import pandas as pd
import google.generativeai as genai
import os
import time

print("Starting the answer generation pipeline...")

# Set up the API key
genai.configure(api_key="AIzaSyA6fWaxSWrMot4KyRIfI_qRZoA1NYnohC8")

# Initialize the model
model = genai.GenerativeModel('gemini-pro')

def get_answer_and_explanation(question, max_retries=3):
    for attempt in range(max_retries):
        try:
            prompt = f"Question: {question}\n\nProvide a concise answer and a brief explanation for this question."
            response = model.generate_content(prompt)
            
            if response.parts:
                text = response.text
                # Split the response into answer and explanation
                parts = text.split('Explanation:', 1)
                answer = parts[0].replace('Answer:', '').strip()
                explanation = parts[1].strip() if len(parts) > 1 else "No explanation provided."
                return answer, explanation
            else:
                print(f"Attempt {attempt + 1}: No valid response. Checking safety ratings.")
                if response.prompt_feedback:
                    print(f"Prompt feedback: {response.prompt_feedback}")
                return "Unable to generate answer due to content restrictions.", "No explanation available."
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                print("Retrying after a short delay...")
                time.sleep(2)  # Wait for 2 seconds before retrying
            else:
                return f"Error: {str(e)}", "No explanation available."

print("Reading the quiz CSV file...")
df = pd.read_csv('quiz.csv')
print(f"Loaded {len(df)} questions from the CSV file.")

answers = []
explanations = []

print("Generating answers and explanations...")
for index, row in df.iterrows():
    question = row['question']
    print(f"Processing question {index + 1}: {question[:30]}...")  # Print first 30 chars of the question
    answer, explanation = get_answer_and_explanation(question)
    answers.append(answer)
    explanations.append(explanation)
    time.sleep(1)  # Add a small delay between requests to avoid rate limiting

print("Adding new columns to the DataFrame...")
df['generated_answer'] = answers
df['explanation'] = explanations

print("Saving results to get_answer.csv...")
df.to_csv('get_answer.csv', index=False)

print("Pipeline completed successfully. Results saved in get_answer.csv")
