#!/bin/sh

#SBATCH --job-name=mcq
#SBATCH --output=logs/mcq.out
#SBATCH --error=logs/mcq.error
#SBATCH --time=04:00:00
#SBATCH --mem=32gb
#SBATCH --account=scavenger
#SBATCH --partition=scavenger
#SBATCH --gres=gpu:rtxa5000:1


# TODO: for Zoey
python -u ../code/mcq.py \
    --llm meta-llama/Llama-3.1-8B-Instruct \
    --language ko \
    --input_dir ../data/subset/agnostic.jsonl \
    --output_dir ../result/mcq/korean_agnostic.jsonl;
python -u ../code/mcq.py \
    --llm meta-llama/Llama-3.1-8B-Instruct \
    --language ko \
    --input_dir ../data/subset/specific_ko.jsonl \
    --output_dir ../result/mcq/korean_specific_ko.jsonl;
python -u ../code/mcq.py \
    --llm meta-llama/Llama-3.1-8B-Instruct \
    --language ko \
    --input_dir ../data/subset/specific_zh.jsonl \
    --output_dir ../result/mcq/korean_specific_zh.jsonl;
python -u ../code/mcq.py \
    --llm meta-llama/Llama-3.1-8B-Instruct \
    --language ko \
    --input_dir ../data/subset/specific_en.jsonl \
    --output_dir ../result/mcq/korean_specific_en.jsonl;



# TODO: for Hope
python -u ../code/mcq.py \
    --llm meta-llama/Llama-3.1-8B-Instruct \
    --language zh \
    --input_dir ../data/subset/agnostic.jsonl \
    --output_dir ../result/mcq/chinese_agnostic.jsonl;
python -u ../code/mcq.py \
    --llm meta-llama/Llama-3.1-8B-Instruct \
    --language zh \
    --input_dir ../data/subset/specific_ko.jsonl \
    --output_dir ../result/mcq/chinese_specific_ko.jsonl;
python -u ../code/mcq.py \
    --llm meta-llama/Llama-3.1-8B-Instruct \
    --language zh \
    --input_dir ../data/subset/specific_zh.jsonl \
    --output_dir ../result/mcq/chinese_specific_zh.jsonl;
python -u ../code/mcq.py \
    --llm meta-llama/Llama-3.1-8B-Instruct \
    --language zh \
    --input_dir ../data/subset/specific_en.jsonl \
    --output_dir ../result/mcq/chinese_specific_en.jsonl;


python -u ../code/mcq.py \
    --llm meta-llama/Llama-3.1-8B-Instruct \
    --language en \
    --input_dir ../data/subset/agnostic.jsonl \
    --output_dir ../result/mcq/english_agnostic.jsonl;
python -u ../code/mcq.py \
    --llm meta-llama/Llama-3.1-8B-Instruct \
    --language en \
    --input_dir ../data/subset/specific_ko.jsonl \
    --output_dir ../result/mcq/english_specific_ko.jsonl;
python -u ../code/mcq.py \
    --llm meta-llama/Llama-3.1-8B-Instruct \
    --language en \
    --input_dir ../data/subset/specific_zh.jsonl \
    --output_dir ../result/mcq/english_specific_zh.jsonl;
python -u ../code/mcq.py \
    --llm meta-llama/Llama-3.1-8B-Instruct \
    --language en \
    --input_dir ../data/subset/specific_en.jsonl \
    --output_dir ../result/mcq/english_specific_en.jsonl;