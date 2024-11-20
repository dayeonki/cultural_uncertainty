import torch
import argparse
import json
import os
from prompt import *
from utils import marker_prompts
from huggingface_hub.hf_api import HfFolder
from transformers import AutoTokenizer, AutoModelForCausalLM
import configparser

config = configparser.ConfigParser()
config.read('../config.ini')
config_keys = config['DEFAULT']

CACHE_DIR = config_keys["CACHE_DIR"]
HF_TOKEN = config_keys["HF_TOKEN"]

os.environ["HF_HOME"] = CACHE_DIR
os.environ["HF_DATASETS"] = CACHE_DIR
HfFolder.save_token(HF_TOKEN)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def default_generation(model, tokenizer, input_ids, terminators):
    outputs = model.generate(
        input_ids,
        max_new_tokens=512,
        # eos_token_id=terminators,
        output_scores=True,
        return_dict_in_generate=True,
        pad_token_id=tokenizer.eos_token_id
    )
    response = outputs.sequences[0][input_ids.shape[-1]:]
    answer = tokenizer.decode(response, skip_special_tokens=True)
    return answer

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--llm", type=str, default="meta-llama/Llama-3.1-8B-Instruct")
    parser.add_argument("--language", type=str)
    parser.add_argument("--input_dir", type=str)
    parser.add_argument("--output_dir", type=str)
    parser.add_argument("--marker", type=str)
    args = parser.parse_args()

    tokenizer = AutoTokenizer.from_pretrained(args.llm, cache_dir=CACHE_DIR)
    model = AutoModelForCausalLM.from_pretrained(
        args.llm,
        torch_dtype=torch.bfloat16,
        cache_dir=CACHE_DIR,
        device_map="auto",
    )

    if args.marker not in marker_prompts:
        raise ValueError("Invalid marker. Choose a valid marker for system prompts.")

    sys_prompt_templates = marker_prompts[args.marker]

    prompt_templates = {
        "ko": ko_qa_prompt,
        "en": en_qa_prompt,
        "zh": zh_qa_prompt,
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

                # TODO(hope): use vllm implementation, right now seems too slow
                # Answer the question 3 times
                answer_list = []
                for _ in range(3):
                    answer_list.append(default_generation(model, tokenizer, input_ids, terminators))

                data['answer_list'] = answer_list
                f_out.write(json.dumps(data, ensure_ascii=False) + '\n')


if __name__ == "__main__":
    main()
