#!/bin/sh

#SBATCH --job-name=all_tasks
#SBATCH --output=logs/all_tasks.out.%j
#SBATCH --error=logs/all_tasks.error.%j
#SBATCH --time=4:00:00
#SBATCH --mem=32gb
#SBATCH --account=clip
#SBATCH --partition=clip
#SBATCH --gres=gpu:rtxa6000:1

declare -A langMap 
langMap["ko"]="korean" 
langMap["zh"]="chinese" 
langMap["en"]="english"

# Llama
# for task in pred_confidence mcq next_token_prob token_prob qa;
# do
#     for lang in ko zh en;
#     do
#         for input_file in agnostic specific_ko specific_en specific_zh;
#         do
#             for marker in nationality connection eduction food music fashion exercise show holiday statue;
#             do
#                 python -u ../code/$task.py \
#                     --llm meta-llama/Llama-3.1-8B-Instruct \
#                     --language $lang \
#                     --input_dir ../data/subset/$input_file.jsonl \
#                     --output_dir ../result/$task/${langMap[$lang]}_{$input_file}_{$marker}_llama.jsonl \
#                     --marker $marker
#             done
#         done
#     done
# done

# Qwen
# for task in pred_confidence mcq next_token_prob token_prob qa;
# do
#     for lang in ko zh en;
#     do
#         for input_file in agnostic specific_ko specific_en specific_zh;
#         do
#             for marker in nationality connection eduction food music fashion exercise show holiday statue;
#             do
#                 python -u ../code/$task.py \
#                     --llm Qwen/Qwen2.5-7B-Instruct \
#                     --language $lang \
#                     --input_dir ../data/subset/$input_file.jsonl \
#                     --output_dir ../result/$task/${langMap[$lang]}_{$input_file}_{$marker}_qwen.jsonl \
#                     --marker $marker
#             done
#         done
#     done
# done

# Code-switch input
# Llama
# for task in pred_confidence mcq next_token_prob token_prob qa;
# do
#     for lang in ko zh en;
#     do
#         for input_file in specific_ko specific_zh;
#         do
#             for marker in nationality connection eduction food music fashion exercise show holiday statue;
#             do
#                 python -u ../code/$task.py \
#                     --llm meta-llama/Llama-3.1-8B-Instruct \
#                     --language $lang \
#                     --input_dir ../data/code-switched/$input_file.jsonl \
#                     --output_dir ../result/$task/${langMap[$lang]}_{$input_file}_{$marker}_llama_code_switch.jsonl \
#                     --marker $marker
#             done
#         done
#     done
# done

# Qwen
# for task in pred_confidence mcq next_token_prob token_prob qa;
# do
#     for lang in ko zh en;
#     do
#         for input_file in specific_ko specific_zh;
#         do
#             for marker in nationality connection eduction food music fashion exercise show holiday statue;
#             do
#                 python -u ../code/$task.py \
#                     --llm Qwen/Qwen2.5-7B-Instruct \
#                     --language $lang \
#                     --input_dir ../data/code-switched/$input_file.jsonl \
#                     --output_dir ../result/$task/${langMap[$lang]}_{$input_file}_{$marker}_qwen_code_switch.jsonl \
#                     --marker $marker
#             done
#         done
#     done
# done

# -----------------------------------------------------------------------
# python -u ../code/qa.py \
#     --llm meta-llama/Llama-3.1-8B-Instruct \
#     --language zh \
#     --input_dir ../data/subset/agnostic.jsonl \
#     --output_dir ../result/next_token_prob/chinese_agnostic.json \
#     --marker nationality

# -----------------------------------------------------------------------
# for task in pred_confidence mcq next_token_prob token_prob qa;
# for task in next_token_prob;
# do
#     for lang in ko zh en;
#     do
#         for input_file in agnostic specific_ko specific_en specific_zh;
#         do
#             for marker in nationality connection eduction food music fashion exercise show holiday statue;
#             do
#                 python -u ../code/$task.py \
#                     --llm Qwen/Qwen2.5-7B-Instruct \
#                     --language $lang \
#                     --input_dir ../data/subset/$input_file.jsonl \
#                     --output_dir ../result/$task/${langMap[$lang]}_{$input_file}_{$marker}_qwen.jsonl \
#                     --marker $marker
#             done
#         done
#     done
# done

# for task in pred_confidence mcq next_token_prob token_prob qa;
# for task in next_token_prob;
# do
#     for lang in ko zh en;
#     do
#         for input_file in specific_ko specific_zh;
#         do
#             for marker in nationality connection eduction food music fashion exercise show holiday statue;
#             do
#                 python -u ../code/$task.py \
#                     --llm Qwen/Qwen2.5-7B-Instruct \
#                     --language $lang \
#                     --input_dir ../data/code-switched/$input_file.jsonl \
#                     --output_dir ../result/$task/${langMap[$lang]}_{$input_file}_{$marker}_qwen_code_switch.jsonl \
#                     --marker $marker
#             done
#         done
#     done
# done

python -u ../code/next_token_prob.py \
    --llm meta-llama/Llama-3.1-8B-Instruct \
    --language en \
    --input_dir ../data/subset/specific_ko.jsonl \
    --output_dir ../result/qa/english_{specific_ko}_{fashion}_llama.jsonl \
    --marker fashion