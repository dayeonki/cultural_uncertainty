import json


# Making specific subsets
input_file = "../calmqa.jsonl"
output_file = "../subset/specific_en.jsonl"

with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    for line in infile:
        data = json.loads(line)
        
        if data["language"] == "English" and data["question_type"] == "culturally_specific":
            outfile.write(json.dumps(data, ensure_ascii=False) + "\n")


# Making agnostic subsets
input_file = "../calmqa.jsonl"
output_file = "../subset/agnostic.jsonl"

with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    for line in infile:
        data = json.loads(line)
        
        if data["language"] == "English" and data["question_type"] == "culturally_agnostic":
            data.pop("question", None)
            outfile.write(json.dumps(data, ensure_ascii=False) + "\n")