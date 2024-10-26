import pandas as pd
import json


jsonl_file_path = '../result/token_prob/korean_agnostic.jsonl'
output_file_path = 'kor_agnostic.xlsx'

data = []
with open(jsonl_file_path, 'r') as f:
    for line in f:
        data.append(json.loads(line))

df = pd.DataFrame(data)
df_selected = df[["question_type", "question_english", "answer", "answerability_prob"]]
df_selected.to_excel(output_file_path, index=False)
