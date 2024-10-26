from datasets import load_dataset
import json


ds = load_dataset("shanearora/CaLMQA")
split = ds["train"]

output_file = "../calmqa_raw.jsonl"

with open(output_file, "w") as f:
    for example in split:
        f.write(json.dumps(example, ensure_ascii=False) + "\n")