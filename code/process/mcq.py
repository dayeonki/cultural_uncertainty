import os
import re
import json
from collections import Counter
import pandas as pd


directory = "/fs/clip-scratch/dayeonki/proj-uncertainty/result/mcq"

def normalize_answer(answer):
    if answer in ["(A)", "A"] or " answerable " in answer.lower() or "(A) Answerable" in answer:
        return "(A) Answerable"
    if answer in ["(B)", "B"] or " unanswerable " in answer.lower() or "(B) Unanswerable" in answer:
        return "(B) Unanswerable"
    return answer


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

for filename in os.listdir(directory):
    if filename.endswith(".jsonl"):
        file_path = os.path.join(directory, filename)
        
        answer_counter = Counter()
        
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                data = json.loads(line.strip())
                answer = data.get("answer")
                if answer:
                    normalized_answer = normalize_answer(answer)
                    answer_counter[normalized_answer] += 1

        # Process file names
        parsed = parse_filename(filename)
        language = parsed[0]
        culturally_specific = parsed[1].replace("{", "").replace("}", "")
        cue = parsed[2].replace("{", "").replace("}", "")
        model = parsed[3].replace(".jsonl", "")
        
        results.append({
            "model": model,
            "language": language,
            "cultural": culturally_specific,
            "cue": cue,
            "(A) Answerable": answer_counter.get("(A) Answerable", 0),
            "(B) Unanswerable": answer_counter.get("(B) Unanswerable", 0)
        })

df = pd.DataFrame(results)

output_path = "mcq.xlsx"
df.to_excel(output_path, index=False)
