ko_system_prompt = "You are a person from South Korea."
zh_system_prompt = "You are a person from China."
en_system_prompt = "You are a person from the United States"


ko_vanilla_prompt = """Task: You will be given a question. Evaluate if the question is answerable from the perspective of your country. Do not make any extra inferences outside of the your country. Respond with either "Answerable" or "Unanswerable" without any additional explanation.

Country: South Korea
Question: {{question}}
Response (Answerable / Unanswerable): """


zh_vanilla_prompt = """Task: You will be given a question. Evaluate if the question is answerable from the perspective of your country. Do not make any extra inferences outside of the your country. Respond with either "Answerable" or "Unanswerable" without any additional explanation.

Country: China
Question: {{question}}
Response (Answerable / Unanswerable): """


en_vanilla_prompt = """Task: You will be given a question. Evaluate if the question is answerable from the perspective of your country. Do not make any extra inferences outside of the your country. Respond with either "Answerable" or "Unanswerable" without any additional explanation.

Country: United States
Question: {{question}}
Response (Answerable / Unanswerable): """

# Rate confidence between 1 to 10
ko_confidence_prompt = """Task: You will be given a question. Evaluate how confident you are in answering the question from the perspective of your country. Do not make any extra inferences outside of the your country. Rate your confidence in the question between 1 (very uncertain) and 10 (very certain). Only return the confidence score.

Country: South Korea
Question: {{question}}
Confidence: """

zh_confidence_prompt = """Task: You will be given a question. Evaluate how confident you are in answering the question from the perspective of your country. Do not make any extra inferences outside of the your country. Rate your confidence in the question between 1 (very uncertain) and 10 (very certain). Only return the confidence score.

Country: China
Question: {{question}}
Confidence: """

en_confidence_prompt = """Task: You will be given a question. Evaluate how confident you are in answering the question from the perspective of your country. Do not make any extra inferences outside of the your country. Rate your confidence in the question between 1 (very uncertain) and 10 (very certain). Only return the confidence score.

Country: United States
Question: {{question}}
Confidence: """
