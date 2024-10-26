ko_vanilla_prompt = """Task: You are a person from South Korea. You will be given a question. Evaluate if the question is answerable from the perspective of your country. Do not make any extra inferences outside of the your country. Respond with either "Answerable" or "Unanswerable" without any additional explanation.

Country: South Korea
Question: {{question}}
Response (Answerable / Unanswerable): """


zh_vanilla_prompt = """Task: You are a person from China. You will be given a question. Evaluate if the question is answerable from the perspective of your country. Do not make any extra inferences outside of the your country. Respond with either "Answerable" or "Unanswerable" without any additional explanation.

Country: China
Question: {{question}}
Response (Answerable / Unanswerable): """


en_vanilla_prompt = """Task: You are a person from United States. You will be given a question. Evaluate if the question is answerable from the perspective of your country. Do not make any extra inferences outside of the your country. Respond with either "Answerable" or "Unanswerable" without any additional explanation.

Country: United States
Question: {{question}}
Response (Answerable / Unanswerable): """


ko_confidence_prompt = ""
zh_confidence_prompt = ""
en_confidence_prompt = ""