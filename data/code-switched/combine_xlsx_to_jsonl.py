import pandas as pd
import json


xlsx_file_path = 'ko.xlsx'
df = pd.read_excel(xlsx_file_path, header=None, names=['questions'])

jsonl_file_path = '../subset/specific_ko.jsonl'
jsonl_data = []

with open(jsonl_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        jsonl_data.append(json.loads(line))

for i in range(len(jsonl_data)):
    jsonl_data[i]["question_codeswitched"] = df['questions'][i]

output_jsonl_file_path = 'specific_ko.jsonl'
with open(output_jsonl_file_path, 'w', encoding='utf-8') as file:
    for entry in jsonl_data:
        file.write(json.dumps(entry, ensure_ascii=False) + '\n')