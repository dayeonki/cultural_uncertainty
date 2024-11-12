import torch
import argparse
import json
import os
from prompt import *
from utils import marker_prompts
from huggingface_hub.hf_api import HfFolder
from transformers import AutoTokenizer, AutoModelForCausalLM

# Replace with your own settings
CACHE_DIR = ""
HF_TOKEN = ""


os.environ["HF_HOME"] = CACHE_DIR
os.environ["HF_DATASETS"] = CACHE_DIR
HfFolder.save_token(HF_TOKEN)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--llm", type=str, default="google/gemma-2-9b-it")
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
        "ko": ko_mcq_prompt,
        "en": en_mcq_prompt,
        "zh": zh_mcq_prompt,
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

                input_ids = tokenizer(messages, return_tensors="pt").to("cuda")

                # Greedy decoding
                outputs = model.generate(
                    **input_ids,
                    max_new_tokens=512,
                    do_sample=False,
                    temperature=0.0,
                    output_scores=True,
                    return_dict_in_generate=True
                )

                generation = tokenizer.decode(outputs[0], skip_special_tokens=True)
                answer_start = "Response (A / B): "
                if answer_start in generation:
                    answer = generation.split(answer_start)[-1].strip()
                    answer = answer.split("<")[0].strip()
                else:
                    answer = generation
                data['answer'] = answer

                print(f"{prompt}")
                print(f"> {answer}")
                print("\n======================================================\n")
                f_out.write(json.dumps(data, ensure_ascii=False) + '\n')


if __name__ == "__main__":
    main()
