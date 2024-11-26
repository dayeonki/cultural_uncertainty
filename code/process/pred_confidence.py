import os
import re
import json
import pandas as pd

# Directory containing the JSONL files
directory = "/fs/clip-scratch/dayeonki/proj-uncertainty/result/pred_confidence"

def parse_filename(filename):
    pattern = r"^(.*?)_(\{.*?\})_(\{.*?\})_(.*?)\.jsonl$"
    match = re.match(pattern, filename)
    if match:
        before_first = match.group(1)  # Before the first '_'
        between_first_second = match.group(2)  # Between first and second '_'
        between_second_third = match.group(3)  # Between second and third '_'
        after_last = match.group(4)  # After the last '_'
        return before_first, between_first_second, between_second_third, after_last
    return None

results = []

# Process each file
for filename in os.listdir(directory):
    if filename.endswith(".jsonl"):
        file_path = os.path.join(directory, filename)
        
        total_sum = 0
        total_count = 0
        
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                data = json.loads(line.strip())
                answer_list = data.get("answer_list", [])
                # Convert answer_list to integers and calculate the sum and count
                numeric_answers = [int(answer) for answer in answer_list if answer.isdigit()]
                total_sum += sum(numeric_answers)
                total_count += len(numeric_answers)

        # Calculate the average for the file
        avg_value = total_sum / total_count if total_count > 0 else 0

        # Process file names
        parsed = parse_filename(filename)
        language = parsed[0]
        culturally_specific = parsed[1].replace("{", "").replace("}", "")
        cue = parsed[2].replace("{", "").replace("}", "")
        model = parsed[3].replace(".jsonl", "")

        # Append results
        results.append({
            "model": model,
            "language": language,
            "cultural": culturally_specific,
            "cue": cue,
            "average_value": avg_value
        })

# Convert results to a DataFrame
df = pd.DataFrame(results)

# Save the DataFrame to an Excel file
output_path = "pred_confidence.xlsx"
df.to_excel(output_path, index=False)
