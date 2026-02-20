import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np 
import joblib 
import requests


def create_embedding(text_list):
    r = requests.post("http://localhost:11434/api/embed", json={
        "model": "bge-m3",
        "input": text_list
    })
    return r.json()["embeddings"]


def inference(prompt):
    r = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama3.2",   # Recommended for your laptop
        "prompt": prompt,
        "stream": False
    })
    return r.json()["response"]


# Load embeddings
df = joblib.load('embeddings.joblib')


# User Query
incoming_query = input("Ask a Question: ")
question_embedding = create_embedding([incoming_query])[0]


# Similarity Search
similarities = cosine_similarity(
    np.vstack(df['embedding'].values),
    [question_embedding]
).flatten()

top_results = 5
max_indx = similarities.argsort()[::-1][:top_results]
new_df = df.loc[max_indx]


# Build Prompt
context_parts = []
for _, row in new_df.iterrows():
    context_parts.append(
        f"Video: {row['number']}\nTime: {row['start']} - {row['end']}\nContent: {row['text']}"
    )
context = "\n\n".join(context_parts)

prompt = f"""
I am teaching web development in my Sigma web development course.

Here are subtitle chunks:
{context}

User Question:
"{incoming_query}"

Answer naturally.
Mention which video number and timestamp the user should watch.
If unrelated, say you only answer course-related questions.
"""


# Save prompt
with open("prompt.txt", "w", encoding="utf-8") as f:
    f.write(prompt)


# LLM Response
response = inference(prompt)
print("\nAnswer:\n")
print(response)


# Save response
with open("response.txt", "w", encoding="utf-8") as f:
    f.write(response)