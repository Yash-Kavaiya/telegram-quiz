import json
import pandas as pd

print("Starting the quiz data processing pipeline...")

# Read JSON file
print("Reading JSON file...")
with open('result.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
print(f"JSON file loaded. Total messages: {len(data['messages'])}")

# Extract poll data
print("Extracting poll data...")
polls = [msg for msg in data["messages"] if "poll" in msg]
print(f"Number of polls extracted: {len(polls)}")

# Extract questions and answers
print("Extracting questions and answers...")
questions = [poll['poll']['question'] for poll in polls]
answers = [poll['poll']["answers"] for poll in polls]
print(f"Number of questions extracted: {len(questions)}")

# Convert answers to text list
print("Converting answers to text list...")
text_answers = [[answer['text'] for answer in answer_set] for answer_set in answers]

# Create DataFrame
print("Creating DataFrame...")
df = pd.DataFrame(text_answers)

# Rename columns
print("Renaming columns...")
df.insert(0, 'question', questions)  # Insert question as the first column
df = df.rename(columns={i: f'option_{i+1}' for i in range(len(df.columns)-1)})  # Rename other columns

print(f"DataFrame created. Shape: {df.shape}")

# Save DataFrame as CSV
print("Saving DataFrame to CSV...")
df.to_csv('quiz.csv', index=False)
print("CSV file 'quiz.csv' has been created.")

print("Pipeline completed successfully.")