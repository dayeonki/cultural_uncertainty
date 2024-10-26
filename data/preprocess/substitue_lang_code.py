import json


language_map = {
    0: "Afar", 1: "Arabic", 2: "Balochi", 3: "Chinese", 4: "English",
    5: "Faroese", 6: "Fijian", 7: "German", 8: "Hebrew", 9: "Hiligaynon",
    10: "Hindi", 11: "Hungarian", 12: "Japanese", 13: "Kirundi", 14: "Korean",
    15: "Papiamento", 16: "Pashto", 17: "Russian", 18: "Samoan", 19: "Spanish",
    20: "Tongan", 21: "Tswana", 22: "Wolof"
}

input_file = "../calmqa_raw.jsonl"
output_file = "../calmqa.jsonl"


with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    for line in infile:
        data = json.loads(line)
        
        if data["question_type"] == 0:
            data["question_type"] = "culturally_agnostic"
        elif data["question_type"] == 1:
            data["question_type"] = "culturally_specific"
        
        if data["language"] in language_map:
            data["language"] = language_map[data["language"]]
        
        outfile.write(json.dumps(data, ensure_ascii=False) + "\n")
