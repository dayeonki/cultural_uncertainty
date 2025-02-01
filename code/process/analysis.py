import os
import re
import json
from collections import Counter
import pandas as pd


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


def get_mcq_results():
    directory = "/fs/clip-scratch/dayeonki/proj-uncertainty/result/mcq"

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

            if model.endswith('code_switch'):
                culturally_specific += "_code_switch"
                model = model.split('_code_switch')[0]
            
            results.append({
                "model": model,
                "language": language,
                "cultural": culturally_specific,
                "cue": cue,
                "(A) Answerable": answer_counter.get("(A) Answerable", 0),
                "(B) Unanswerable": answer_counter.get("(B) Unanswerable", 0),
                "Answerable %": answer_counter.get("(A) Answerable", 0) / (answer_counter.get("(A) Answerable", 0) + answer_counter.get("(B) Unanswerable", 0))
            })

    df = pd.DataFrame(results)

    output_path = "mcq.tsv"
    df.to_csv(output_path, sep='\t', index=False)


def get_pred_conf_results():
    directory = "/fs/clip-scratch/dayeonki/proj-uncertainty/result/pred_confidence"
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
            
            if model.endswith('code_switch'):
                culturally_specific += "_code_switch"
                model = model.split('_code_switch')[0]

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

    # Save the DataFrame to an tsv file
    output_path = "pred_confidence.tsv"
    df.to_csv(output_path, sep='\t', index=False)


def get_ntp_results():
    directory = "/fs/clip-scratch/dayeonki/proj-uncertainty/result/next_token_prob"

    results = []

    for filename in os.listdir(directory):
        if filename.endswith(".jsonl"):
            file_path = os.path.join(directory, filename)
            
            prob_list = []
            
            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    data = json.loads(line.strip())
                    prob = data.get("next_answer_token_prob")
                    prob_list.append(float(prob))

            # Process file names
            parsed = parse_filename(filename)
            language = parsed[0]
            culturally_specific = parsed[1].replace("{", "").replace("}", "")
            cue = parsed[2].replace("{", "").replace("}", "")
            model = parsed[3].replace(".jsonl", "")

            if model.endswith('code_switch'):
                culturally_specific += "_code_switch"
                model = model.split('_code_switch')[0]
            
            results.append({
                "model": model,
                "language": language,
                "cultural": culturally_specific,
                "cue": cue,
                "P(Answerable)": sum(prob_list)/len(prob_list)
            })

    df = pd.DataFrame(results)

    output_path = "ntp.tsv"
    df.to_csv(output_path, sep='\t', index=False)


# get_mcq_results()
# get_pred_conf_results()
# get_ntp_results()

def get_result_table(model="llama", language="english", cue_list=['nationality', 'connection', 'holiday', 'fashion', 'music', 'food', 'eduction', 'statue', 'exercise', 'show']):
    print(model, language)
    df_mcq = pd.read_csv("mcq.tsv", sep='\t')
    df_ntp = pd.read_csv("ntp.tsv", sep='\t')
    df_pred_conf = pd.read_csv("pred_confidence.tsv", sep="\t")

    sub_df_mcq = df_mcq[(df_mcq['model'] == model) & (df_mcq['language'] == language)]
    sub_df_ntp = df_ntp[(df_ntp['model'] == model) & (df_ntp['language'] == language)]
    sub_df_pred_conf = df_pred_conf[(df_pred_conf['model'] == model) & (df_pred_conf['language'] == language)]

    data_list = ['agnostic', 'specific_en', 'specific_ko', 'specific_zh', 'specific_ko_code_switch', 'specific_zh_code_switch']

    for data_option in data_list:
        per_ans_list = list(sub_df_mcq[(sub_df_mcq['cultural'] == data_option) & sub_df_mcq['cue'].isin(cue_list)]['Answerable %'])
        per_ans = sum(per_ans_list) / len(per_ans_list)
        
        p_ans_list = list(sub_df_ntp[(sub_df_ntp['cultural'] == data_option) & sub_df_ntp['cue'].isin(cue_list)]['P(Answerable)'])
        p_ans = sum(p_ans_list) / len(p_ans_list)

        pred_conf_list = list(sub_df_pred_conf[(sub_df_pred_conf['cultural'] == data_option) & sub_df_pred_conf['cue'].isin(cue_list)]['average_value'])
        pred_conf = sum(pred_conf_list) / len(pred_conf_list)

        # print(data_option, per_ans, p_ans, pred_conf)
        # print(per_ans, p_ans, pred_conf)
        print(f"{round(p_ans, 2)}\t{round(per_ans*100, 2)}%\t{round(pred_conf, 2)}")

# get_result_table(model="qwen", language="english", cue_list=['nationality', 'connection', 'holiday', 'fashion', 'music', 'food', 'eduction', 'statue', 'exercise', 'show'])
# get_result_table(model="qwen", language="chinese", cue_list=['nationality', 'connection', 'holiday', 'fashion', 'music', 'food', 'eduction', 'statue', 'exercise', 'show'])
# get_result_table(model="qwen", language="korean", cue_list=['nationality', 'connection', 'holiday', 'fashion', 'music', 'food', 'eduction', 'statue', 'exercise', 'show'])

# get_result_table(model="qwen", language="english", cue_list=['nationality', 'connection'])
# get_result_table(model="qwen", language="chinese", cue_list=['nationality', 'connection'])
# get_result_table(model="qwen", language="korean", cue_list=['nationality', 'connection'])

# get_result_table(model="qwen", language="english", cue_list=['holiday', 'fashion', 'music', 'food', 'eduction', 'statue', 'exercise', 'show'])
# get_result_table(model="qwen", language="chinese", cue_list=['holiday', 'fashion', 'music', 'food', 'eduction', 'statue', 'exercise', 'show'])
# get_result_table(model="qwen", language="korean", cue_list=['holiday', 'fashion', 'music', 'food', 'eduction', 'statue', 'exercise', 'show'])