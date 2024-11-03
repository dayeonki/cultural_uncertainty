import torch
import argparse
import json
import os
from prompt import ko_system_prompt, zh_system_prompt, en_system_prompt, ko_vanilla_prompt, zh_vanilla_prompt, en_vanilla_prompt
from huggingface_hub.hf_api import HfFolder
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch.nn.functional as F


CACHE_DIR = "/fs/clip-scratch/dayeonki/.cache"
HF_TOKEN = "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"


os.environ["HF_HOME"] = CACHE_DIR
os.environ["HF_DATASETS"] = CACHE_DIR
HfFolder.save_token(HF_TOKEN)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--llm", type=str, default="meta-llama/Llama-3.1-8B-Instruct")
    parser.add_argument("--language", type=str)
    parser.add_argument("--input_dir", type=str)
    parser.add_argument("--output_dir", type=str)
    args = parser.parse_args()

    tokenizer = AutoTokenizer.from_pretrained(args.llm, cache_dir=CACHE_DIR)
    model = AutoModelForCausalLM.from_pretrained(
        args.llm,
        torch_dtype=torch.bfloat16,
        cache_dir=CACHE_DIR,
        device_map="auto",
    )

    sys_prompt_templates = {
        "ko": ko_system_prompt,
        "en": en_system_prompt,
        "zh": zh_system_prompt,
    }
    prompt_templates = {
        "ko": ko_vanilla_prompt,
        "en": en_vanilla_prompt,
        "zh": zh_vanilla_prompt,
    }
    prompt_template = prompt_templates.get(args.language)
    sys_prompt_template = sys_prompt_templates.get(args.language)
    if not prompt_template:
        raise ValueError("Language should be one of the following: en, zh, ko.")

    with open(args.input_dir, 'r') as f_in, open(args.output_dir, 'w') as f_out:
        for line in f_in:
            data = json.loads(line)
            question = data.get('question_english')
            if question:
                prompt = prompt_template.replace("{{question}}", question)
                messages = [
                    {"role": "system", "content": sys_prompt_template},
                    {"role": "user", "content": prompt},
                ]

                input_ids = tokenizer.apply_chat_template(
                    messages,
                    add_generation_prompt=True,
                    return_tensors="pt"
                ).to(model.device)

                terminators = [
                    tokenizer.eos_token_id,
                    tokenizer.convert_tokens_to_ids("<|eot_id|>")
                ]

                # sampling (temperature=0)
                # outputs = model.generate(
                #     input_ids,
                #     max_new_tokens=128,
                #     eos_token_id=terminators,
                #     do_sample=False,
                #     temperature=0.0,
                #     output_scores=True,
                #     return_dict_in_generate=True
                # )

                # greedy decoding
                outputs = model.generate(
                    input_ids,
                    max_new_tokens=128,
                    eos_token_id=terminators,
                    do_sample=False,
                    output_scores=True,
                    return_dict_in_generate=True
                )

                response = outputs.sequences[0][input_ids.shape[-1]:]
                answer = tokenizer.decode(response, skip_special_tokens=True)

                token_prob_pairs = []
                joint_prob = 1.0

                for i, score in enumerate(outputs.scores):
                    # softmax: probability distribution over vocab
                    probs = F.softmax(score[0], dim=-1)
                    token_id = response[i].item()
                    token = tokenizer.decode([token_id], skip_special_tokens=True).strip()

                    # Skip empty strings
                    if token == "":
                        continue
                    token_prob = probs[token_id].item()
                    token_prob_pairs.append((token, round(token_prob, 4)))
                    
                    if token.strip() in ["Un", "answer", "able"]:
                        joint_prob *= token_prob
                    elif token.strip() in ["Answer", "able"]:
                        joint_prob *= token_prob
                    else: pass

                data['answer'] = answer
                data['token_prob_pairs'] = token_prob_pairs
                data['answerability_prob'] = round(joint_prob, 4)
                f_out.write(json.dumps(data, ensure_ascii=False) + '\n')

                print(f"{prompt}")
                print(f"> {answer}")
                print(f"Token probability: {token_prob_pairs}")
                print(f"Joint token probability: {round(joint_prob, 4)}")
                print("\n======================================================\n")


if __name__ == "__main__":
    main()
