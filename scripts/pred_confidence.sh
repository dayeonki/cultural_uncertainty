#!/bin/sh

#SBATCH --job-name=pred_confidence
#SBATCH --output=logs/pred_confidence.out
#SBATCH --error=logs/pred_confidence.error
#SBATCH --time=04:00:00
#SBATCH --mem=32gb
#SBATCH --account=scavenger
#SBATCH --partition=scavenger
#SBATCH --gres=gpu:rtxa5000:1

declare -A langMap 
langMap["ko"]="korean" 
langMap["zh"]="chinese" 
langMap["en"]="english"

for lang in ko zh en;
do
    for input_file in agnostic specific_ko specific_zh specific_en;
    do
        python -u ../code/pred_confidence.py \
            --llm meta-llama/Llama-3.1-8B-Instruct \
            --language $lang \
            --input_dir ../data/subset/$input_file.jsonl \
            --output_dir ../result/pred_confidence/${langMap[$lang]}_$input_file.jsonl;
    done
done
