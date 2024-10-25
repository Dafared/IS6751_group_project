import pandas as pd
import re
from tqdm import tqdm

def clean_text(text):
    text = re.sub(r'<.*?>', '', text)
    return text.strip()

scores = []
texts = []

with open('movies.txt', 'r', encoding='ISO-8859-1') as f:
    score, text = None, None 
    for line in tqdm(f, desc="Reading file"):
        if line.startswith("review/score:"):
            score = line.strip().split(": ")[1]
        
        elif line.startswith("review/text:"):
            text = line.strip().split(": ", 1)[1]
            text = clean_text(text)
            
            if score and text:
                scores.append(float(score))
                texts.append(text)
                
            score, text = None, None

df = pd.DataFrame({'score': scores, 'text': texts})

sampled_df = df.groupby('score', group_keys=False).apply(lambda x: x.sample(frac=0.1, random_state=42))

if len(sampled_df) > 100000:
    sampled_df = sampled_df.sample(n=100000, random_state=42)

print(sampled_df.head())

sampled_df.to_csv('cleaned_sampled_amazon_reviews.csv', index=False)
