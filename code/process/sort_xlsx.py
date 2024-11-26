import pandas as pd

file_path = "pred_confidence.xlsx"
df = pd.read_excel(file_path)

sorted_df = df.sort_values(by=["model", "language", "cultural", "cue"], ascending=True)

output_file = "sorted_pred_confidence.xlsx"
sorted_df.to_excel(output_file, index=False)