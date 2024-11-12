# Explicit marker : direct mention of nationality
ko_system_prompt = "You are a person from South Korea."
zh_system_prompt = "You are a person from China."
en_system_prompt = "You are a person from the United States."

# Explicit marker : make connections to target culture
ko_connection_prompt = "Make connections to the Korean culture."
zh_connection_prompt = "Make connections to the Chinese culture."
en_connection_prompt = "Make connections to the American culture."

# Implicit marker : eduction
ko_education_prompt = "I went to Seoul National University."
zh_education_prompt = "I went to Tsinghua University."
en_education_prompt = "I went to Harvard University."

# Implicit marker : food
ko_food_prompt = "For dinner, I like to eat K-BBQ with kimchi."
zh_food_prompt = "For dinner, I like to eat Bo Bo Chicken."
en_food_prompt = "For dinner, I like to eat In-n-Out burger and animal-style fries."

# Implicit marker : music
ko_music_prompt = "I like listening to K-pop."
zh_music_prompt = "I like listening to Mandopop."
en_music_prompt = "I like listening to country music."

# Implicit marker : fashion/clothing
ko_fashion_prompt = "I like to dress in trendy streetwear inspired by K-pop idols."
zh_fashion_prompt = "I like wearing a horse-face skirt with other hanfu items."
en_fashion_prompt = "I like wearing jeans and a T-shirt for a casual look."

# Implicit marker : exercise
ko_exercise_prompt = "I like hiking up Bukhansan with friends."
zh_exercise_prompt = "I like square dancing with my friends after dinner."
en_exercise_prompt = "I usually go for a run in the park in the morning."

# Implicit marker : show/movie
ko_show_prompt = "My favorite show is 'Crash Landing on You'."
zh_show_prompt = "My favorite show is 'The Legend of Zhen Huan'."
en_show_prompt = "My favorite show is 'Friends'."

# Implicit marker : holiday/celebration
ko_holiday_prompt = "I like celebrating Chuseok with my family."
zh_holiday_prompt = "I like celebrating the Spring Festival with my family."
en_holiday_prompt = "I like celebrating Thanksgiving with my family."

# Implicit marker : attraction/statue
ko_statue_prompt = "On the front door of my house, I have a statue of the Gyeongbokgung Palace."
zh_statue_prompt = "On the front door of my house, I have a statue of Chairman Mao."
en_statue_prompt = "On the front door of my house, I have a statue of the Statue of Liberty."



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

# Multiple-choic question (MCQ) style
ko_mcq_prompt = """Task: You will be given a question. Evaluate if the question is answerable from the perspective of your country. Do not make any extra inferences outside of the your country. Select one of the following options: (A) "Answerable" or (B) "Unanswerable". Do not provide any additional explanations.

Country: South Korea
Question: {{question}}
Options: 
(A) Answerable
(B) Unanswerable
Response (A / B): """

zh_mcq_prompt = """Task: You will be given a question. Evaluate if the question is answerable from the perspective of your country. Do not make any extra inferences outside of the your country. Select one of the following options: (A) "Answerable" or (B) "Unanswerable". Do not provide any additional explanations.

Country: China
Question: {{question}}
Options: 
(A) Answerable
(B) Unanswerable
Response (A / B): """

en_mcq_prompt = """Task: You will be given a question. Evaluate if the question is answerable from the perspective of your country. Do not make any extra inferences outside of the your country. Select one of the following options: (A) "Answerable" or (B) "Unanswerable". Do not provide any additional explanations.

Country: United States
Question: {{question}}
Options: 
(A) Answerable
(B) Unanswerable
Response (A / B): """