import torch
import argparse
import json
import os
from prompt import *
from utils import marker_prompts
from huggingface_hub.hf_api import HfFolder
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch.nn.functional as F

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

                response = outputs.sequences[0][input_ids.shape[-1]:]
                generation = tokenizer.decode(response, skip_special_tokens=True)

                answer_start = "Response (Answerable / Unanswerable): "
                if answer_start in generation:
                    answer = generation.split(answer_start)[-1].strip()
                    answer = answer.split("<")[0].strip()
                else:
                    answer = generation

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
