## Cultural Uncertainty
### [1] Data Preprocess
- Full dataset: `data/calmqa.jsonl`
- Subset of each dataset (agnostic, en-specific, ko-specific, zh-specific) can be found in `data/subset/` directory.
- Code used for preprocessing raw dataset are in `data/preprocess` directory.
  - `count_entries.py`: Count number of entries with filters
  - `make_subset.py`: Make subset (agnostic, en-specific, ko-specific, zh-specific)
  - `save_hf_data.py`: Save dataset from huggingface
  - `substitute_lang_code.py`: Substitute language code to nationality names
 
### [2] Calculate token probability
- Prompt: `code/prompt.py`
- Run `code/token_prob.py` for calculating token probability
  - **llm**: Huggingface LLM directory (default to `meta-llama/Llama-3.1-8B-Instruct`)
  - **language**: country-tied persona (ko, zh, en)
  - **input_dir**: directory to input jsonl file
  - **output_dir**: directory to output jsonl file

#### Exemplar result
- answer: Answerable / Unanswerable
- token probability
- joint token probability: Joint probability for "Answerable" or "Unanswerable" part
```
# Prompt
Task: You are a person from South Korea. You will be given a question. Evaluate if the question is answerable from the perspective of your country. Do not make any extra inferences outside of the your country. Respond with either "Answerable" or "Unanswerable" without any additional explanation.

Country: South Korea
Question: Why can the same temperature feel completely different on different days or seasons?
Response (Answerable / Unanswerable): 

> Answerable
Token probability: [('Answer', 0.9999), ('able', 1.0), ('', 0.6497)]
Joint token probability: 0.9999
```

### [3] Predict confidence score
- Prompt: `code/prompt.py`
- Run `code/pred_confidence.py` for predicting the confidence score
  - Parameters are the same as [2]

#### Exemplar result
- answer: a confidence score from 1 to 10 (w/ temperature 0)
- answer_list: confidence score list (same input setup but generating responses 10 times w/ temperature 1)
```
# Prompt
Task: You are a person from South Korea. You will be given a question. Evaluate how confident you are in answering the question from the perspective of your country. Do not make any extra inferences outside of the your country. Rate your confidence in the question between 1 (very uncertain) and 10 (very certain). Only return the confidence score.

Country: South Korea
Question: Why can the same temperature feel completely different on different days or seasons?
Confidence:

> 8
```