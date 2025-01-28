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
You are given a question and a correct answer to it in Lithuanian. Generate INCORRECT version of the answer ONLY in Lithuanian based on the abswer text. Generated incorrect answers helps teachers to prepare tricky exam questions and answer choices. 
The generated incorrect answer must be based on the information present in the correct answer and the question. Each question, correct answer and paraphrased answer should be independent of the others.

To generate incorrect answer, introduce minor changes to the correct one that would complete change its meaning. You can alter details such as names, dates, or numbers slightly, but ensure the answer is still somewhat related to the original. This creates a subtle mistake without straying too far from the topic.

Return just a paraphrased answer in Lithuanian."""

examples = [
    {
        "question": "Kada Lietuva tapo nepriklausoma?",
        "correct_answer": "Lietuva paskelbe nepriklausomybę 1918 metais.",
        "generated_answer": "Lietuva paskelbe nepriklausomybę 1920 metais."
    },
    {
        "question": "Kas yra Vilniaus miesto įkūrėjas?",
        "correct_answer": "Vilniaus įkūrėjas buvo Gediminas, XIV amžiuje.",
        "generated_answer": "Vilniaus įkūrėjas buvo Vytautas, XIV amžiuje."
    },
     {
        "question": "Koks buvo Lietuvos vaidmuo kovose už nepriklausomybę XX amžiaus pradžioje?",
        "correct_answer": "Lietuva kovėsi už nepriklausomybę su Rusijos imperija ir 1918 metais paskelbe nepriklausomybę, tačiau kovos tęsėsi su bolševikais ir Lenkija.",
        "generated_answer": "Lietuva kovėsi už nepriklausomybę su Lenkija ir 1920 metais paskelbe nepriklausomybę, tačiau vėliau tapo Lenkijos dalimi."
    },
    {
        "question": "Kokia buvo Lietuvos pozicija Antrojo pasaulinio karo metu?",
        "correct_answer": "Lietuva buvo okupuota Sovietų Sąjungos 1940 metais, vėliau ir nacių Vokietijos 1941-1944 metais, ir vėl Sovietų Sąjungos po 1944 metų.",
        "generated_answer": "Lietuva buvo okupuota Sovietų Sąjungos 1941 metais, vėliau ir nacių Vokietijos 1940-1945 metais, ir po karo liko nepriklausoma."
    },
    {
        "question": "Kas yra Vilniaus miesto įkūrėjas?",
        "correct_answer": "Vilniaus įkūrėjas buvo Gediminas, XIV amžiuje.",
        "generated_answer": "Vilniaus įkūrėjas buvo Gediminas, XV amžiuje."
    },
      {
        "question": "Kas yra lietuvių kalbos abėcėlės pirmas raidė?",
        "correct_answer": "Lietuvių kalbos abėcėlės pirmas raidė yra A.",
        "generated_answer": "Lietuvių kalbos abėcėlės pirmas raidė yra E A B C."
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
                'content': example_dict["generated_answer"]
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


save_dir = "nonmatch_answers-MinorChanges"
os.makedirs(save_dir, exist_ok=True)

for modelname in MODELNAMES:
    preds = run(modelname, data)
    with open(os.path.join(save_dir, f"{modelname}.json"), "w") as f:
        json.dump(preds, f)

