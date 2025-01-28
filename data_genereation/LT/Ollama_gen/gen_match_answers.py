#!/usr/bin/env python
# coding: utf-8

# In[10]:


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
- You can use synonyms or related terms that maintain the original meaning.
- You can change the sentence structure such as turning a direct answer into a statement, question, or exclamatory format
- You can alternate between formal and informal styles, use a mix of complete sentence answers and shorter, more concise phrases.
- Avoid Ambiguity. The paraphrased version should remain clear and avoid introducing vague or overly complex phrasing.
- Retain the cultural and contextual nuances of the original response, ensuring paraphrased answers are appropriate for a Lithuanian-speaking audience.

Return just a paraphrased answer in Lithuanian."""


examples = [
    {
        'question': 'Kokia kalba yra valstybinė Lietuvoje?',
        'correct_answer': 'Lietuvių kalba',
        'paraphrased_answer': "Ar žinote, kokia yra Lietuvos valstybinė kalba? Tai lietuvių kalba!"
    },
    
    {
        'question': 'Kas buvo pirmasis Lietuvos prezidentas?',
        'correct_answer': 'Antanas Smetona',
        'paraphrased_answer': "Pirmuoju Lietuvos prezidentu buvo Antanas Smetona – įsimintinas Lietuvos istorijos veikėjas."
    },
    

    {
        'question': 'Kuri Lietuvos upė yra didžiausia?',
        'correct_answer': 'Nemunas',
        'paraphrased_answer': "Didžiausia upė Lietuvoje yra Nemunas."
    }, 

    {
        'question': 'Koks miestas yra didžiausias Lietuvoje pagal gyventojų skaičių?',
        'correct_answer': 'Vilnius',
        'paraphrased_answer': "Didžiausias Lietuvos miestas? Aišku, Vilnius!"
    },
    {
        'question': 'Kada buvo įkurta Lietuvos valstybė?',
        'correct_answer': 'XIII amžiuje',
        'paraphrased_answer': "Lietuvos valstybė buvo įkurta dar XIII amžiuje – svarbus istorinis laikotarpis."
    },
    {
        'question': 'Kokios spalvos yra Lietuvos vėliava?',
        'correct_answer': 'Geltona, žalia ir raudona',
        'paraphrased_answer': "Lietuvos vėliava – trispalvė: geltona, žalia, raudona."
    }
    
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
        

    output = requests.post(
        "http://127.0.0.1:11434/api/chat/",
        json = {
            "model": modelname,
            "messages": messages,
            "stream": False,
            "options": {"seed": 2}
        }
    ).json()

    return output["message"]["content"], sample_id





# output_list will be populated with generated outputs as soon as they are available
output_list = []

def run(modelname, data):
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
    "llama3", "llama2:13b",
    "llama3.2", "mistral"
]
data = read_jsonl("LT-KID.jsonl")


save_dir = "match_answers"
os.makedirs(save_dir, exist_ok=True)

for modelname in MODELNAMES:
    preds = run(modelname, data)
    with open(os.path.join(save_dir, f"{modelname}.json"), "w") as f:
        json.dump(preds, f)

