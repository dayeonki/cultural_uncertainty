import os
import re
import json
import pandas as pd

from analysis import parse_filename

def get_open_qa_results():
    directory = "../../result/qa"

    results = []
    for filename in os.listdir(directory):
        if filename.endswith(".jsonl"):
            # print(filename)
            file_path = os.path.join(directory, filename)

            # Process file names
            parsed = parse_filename(filename)
            language = parsed[0]
            culturally_specific = parsed[1].replace("{", "").replace("}", "")
            cue = parsed[2].replace("{", "").replace("}", "")
            model = parsed[3].replace(".jsonl", "")
            if model.endswith('code_switch'):
                culturally_specific += "_code_switch"
                model = model.split('_code_switch')[0]

            with open(file_path, "r", encoding="utf-8") as file:
                for qid, line in enumerate(file):
                    try:
                        data = json.loads(line.strip())
                        results.append({
                            "model": model,
                            "language": language,
                            "cultural": culturally_specific,
                            "cue": cue,
                            "qid": qid,
                            "question": data['question_english'],
                            "answer_0": data['answer_list'][0],
                            "answer_1": data['answer_list'][1],
                            "answer_2": data['answer_list'][2]
                        })
                    except:
                        print(data)

    df = pd.DataFrame(results)

    output_path = "qa.tsv"
    df.to_csv(output_path, sep='\t', index=False)

get_open_qa_results()
