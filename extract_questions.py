import re
import json

# Filepath for the input Markdown file and output JSON file
input_file = "README.md"  # Replace with the actual path to your file
output_file = "questions.json"

# Regex patterns to extract questions, images, answers, and correct answers
question_pattern = r"### (.*?)\n"
image_pattern = r"!\[.*?\]\((.*?)\)"
answers_pattern = r"- \[([ x])\] (.*?)\n"
correct_answer_pattern = r"- \[x\] (.*?)\n"

# Initialize a list to store extracted questions
questions = []

# Read the Markdown file
with open(input_file, "r", encoding="utf-8") as file:
    content = file.read()

# Split content into sections for each question
sections = content.split("### ")[1:]  # Skip the first part before the first question

# Process each section
for section in sections:
    # Extract the question text
    question_match = re.match(question_pattern, "### " + section)
    question_text = question_match.group(1).strip() if question_match else None

    # Extract all associated images
    image_matches = re.findall(image_pattern, section)
    image_urls = [image.strip() for image in image_matches] if image_matches else []

    # Extract all answer possibilities
    answers = []
    for match in re.finditer(answers_pattern, section):
        answers.append(match.group(2).strip())

    # Extract the correct answer(s)
    correct_answers = []
    for match in re.finditer(correct_answer_pattern, section):
        correct_answers.append(match.group(1).strip())

    # Append the extracted data to the questions list
    if question_text:
        questions.append({
            "question": question_text,
            "images": image_urls,
            "answers": answers,
            "correct_answers": correct_answers
        })

# Write the extracted questions to a JSON file
with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump(questions, json_file, indent=4, ensure_ascii=False)

print(f"Extracted {len(questions)} questions and saved to {output_file}.")