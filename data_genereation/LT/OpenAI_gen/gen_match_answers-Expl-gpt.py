#!/usr/bin/env python
# coding: utf-8

# In[10]:


from openai import OpenAI
client = OpenAI()

import json
def read_jsonl(path):
    data = []
    with open(path, 'r') as f:
        for l in f.read().split('\n'):
            if l:
                data.append(json.loads(l))
    return data


# In[ ]:





# In[ ]:





# In[ ]:





# In[11]:


system_text = """Instructions:
You are given a question and a correct answer to it in Lithuanian. Generate a paraphrased version of the answer ONLY in Lithuanian based on the abswer text. Paraphrasing answers helps students to deepen their understanding of the subject. 
The paraphrased answer must be based on the information present in the correct answer and the question. Assume the answer as factual knowledge, rather than providing new information. Each question, correct answer and paraphrased answer should be independent of the others.

Rules:
- Paraphrased answer should be relevant to the question, semantically same to the original corret answer, and deliver the same information as the correct answer.  
- Paraphrased answers must be written in natural Lithuanian language.
- You are not allowed to change dates, names, locations, amounts and other crucial entities.
- Avoid ambiguity. The paraphrased version should remain clear and avoid introducing vague or overly complex phrasing.
- Retain the cultural and contextual nuances of the original response, ensuring paraphrased answers are appropriate for a Lithuanian-speaking audience.
- You can change the sentence structure such as turning a direct answer into a statement, question, or exclamatory format

Return just a paraphrased answer in Lithuanian."""


examples = [
    {"question": "Kokia kalba yra valstybinė Lietuvoje?", "correct_answer": "Lietuvių kalba", "paraphrased_answer": "Kaip nuostabu, kad Lietuvoje valstybinė kalba yra lietuvių!"},
    {"question": "Kada Lietuva tapo nepriklausoma?", "correct_answer": "1918 metais", "paraphrased_answer": "Lietuva tapo nepriklausoma 1918 metais – tai tikrai istorinis įvykis!"},
    {"question": "Kokie pagrindiniai Lietuvos eksporto produktai?", "correct_answer": "Maisto produktai, chemikalai, baldai", "paraphrased_answer": "Lietuva eksportuoja puikius maisto produktus, chemikalus ir baldus!"},
    {"question": "Kokie yra Lietuvos gyventojų amžiaus vidurkiai?", "correct_answer": "Apie 44 metus", "paraphrased_answer": "Lietuvos gyventojų vidutinė amžiaus trukmė – apie 44 metai!"},
{"question": "Koks yra Lietuvos ekonomikos augimo tempas pastaraisiais metais?", "correct_answer": "Lietuvos ekonomika pastaraisiais metais sparčiai augo.", "paraphrased_answer": "Kaip greitai ir sėkmingai augo Lietuvos ekonomika per pastaruosius metus!"},
    {"question": "What is the Lithuanian science and education system like?", "correct_answer": "The Lithuanian education system is characterized by a high level of education and a focus on innovation.", "paraphrased_answer": "How excellent and advanced is the Lithuanian education system, focused on a high level of education and innovation!"}
]



# In[ ]:





# In[14]:


from typing import List
from tqdm import tqdm
import numpy as np
import requests
import string
import itertools
import json, os
import concurrent.futures
import requests

def format_user_input(question, answer):
    return f"Question:\n{question}\n\nCorrect Answer:\n{answer}"

def generate_output(system_text, examples, modelname, question, answer, sample_id):
    
    messages = [
		{
            "role": "system",
            "content": system_text
        }

	]
    
    for example_dict in examples:
        messages.append(
            {
                "role": "user",
                "content": format_user_input(question=example_dict['question'], answer=example_dict['correct_answer'])
            }
        )
        messages.append(
            {
                "role": "assistant",
                'content': example_dict["paraphrased_answer"]
            }
        )

    messages.append(
            {
                "role": "user",
                "content": format_user_input(question=question, answer=answer)
            }
        )
        

    output = client.chat.completions.create(
        model=modelname,
        messages=messages
    )

    return output.choices[0].message.content, sample_id





def run(modelname, data):
    output_list = []
    print(modelname)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        
        # system_text, examples, modelname, question, answer, sample_id
        entries = [
            (system_text, examples, modelname, 
             x["question"], x['answer'], i) for i,x in enumerate(data)
        ]
        future_to_entry = {
            executor.submit(generate_output, *entry): entry
            for entry in entries
        }
        
        
        # execute whatever is in queue
        for future in tqdm(concurrent.futures.as_completed(future_to_entry), total=len(entries)):
            entry = future_to_entry[future]
            try:
                result = future.result()
                if result:
                    output_list.append(result)
            except Exception as e:
                print(f"Error {type(e)}:{e} processing entry: {entry[2]}")

    return output_list


# In[ ]:


MODELNAMES = [
    "gpt-4o-2024-08-06"
]
data = read_jsonl("LT-KID.jsonl")


save_dir = "match_answers-exclamatory"
os.makedirs(save_dir, exist_ok=True)

for modelname in MODELNAMES:
    preds = run(modelname, data)
    with open(os.path.join(save_dir, f"{modelname}.json"), "w") as f:
        json.dump(preds, f)

