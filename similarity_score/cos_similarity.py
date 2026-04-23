import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel
import torch

# Loading the Excel file
df = pd.read_csv(r"/home/riham/Desktop/llm_based_info_extraction/similarity_score/extracted_vs_groundtruth_morph_qwen_p2 (1).csv")

# Load ClinicalBERT model and tokenizer
model_name = "emilyalsentzer/Bio_ClinicalBERT"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Function to get embedding from BERT
def get_embedding(text):
    if not isinstance(text, str) or not text.strip():
        return torch.zeros(768)
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].squeeze()

# Compute embeddings, similarities, and print results
similarities = []
for index, row in df.iterrows():
    emb1 = get_embedding(str(row['extracted_morph']))
    emb2 = get_embedding(str(row['GT']))
    sim = cosine_similarity(emb1.unsqueeze(0), emb2.unsqueeze(0))[0][0]
    similarities.append(sim)
    print(f"Row {index} similarity: {sim:.4f}")

# Inserting the similarity_score next to 'Ground_truth' column
insert_idx = df.columns.get_loc("GT") + 1
df.insert(insert_idx, "similarity_score", similarities)

# Saving to Excel
df.to_csv("/home/riham/Desktop/llm_based_info_extraction/similarity_score_COLON_qwen_p2.csv", index=False)
# Compute and print average similarity
average_similarity = sum(similarities) / len(similarities)
print(f"\nAverage similarity score: {average_similarity:.4f}")
print("All similarity scores computed and saved to 'output_with_similarity.xlsx'.")
