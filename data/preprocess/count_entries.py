import json

input_file = "../calmqa.jsonl"
count = 0

with open(input_file, "r") as infile:
    for line in infile:
        data = json.loads(line)
        if data["language"] == "Chinese" and data["question_type"] == "culturally_specific":
            count += 1
print(count)
