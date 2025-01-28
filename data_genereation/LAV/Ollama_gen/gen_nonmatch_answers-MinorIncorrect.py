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
You are given a question and a correct answer to it in Latvian. Generate INCORRECT version of the answer ONLY in Latvian based on the abswer text. Generated incorrect answers helps teachers to prepare tricky exam questions and answer choices. 
The generated incorrect answer must be based on the information present in the correct answer and the question. Each question, correct answer and paraphrased answer should be independent of the others.

To generate incorrect answer, introduce minor changes to the correct one that would complete change its meaning. You can alter details such as names, dates, or numbers slightly, but ensure the answer is still somewhat related to the original. This creates a subtle mistake without straying too far from the topic.

Return just a paraphrased answer in Latvian."""

examples = [
{
        "question": "Kad Latvija kļuva neatkarīga?",
        "correct_answer": "Latvija pasludināja neatkarību 1918. gadā.",
        "generated_answer": "Latvija pasludināja neatkarību 1920. gadā."
    },
    {
        "question": "Kas ir Rīgas pilsētas dibinātājs?",
        "correct_answer": "Rīgas dibinātājs bija Dēriķis, XIV gadsimtā.",
        "generated_answer": "Rīgas dibinātājs bija Vaidots, XIV gadsimtā."
    },
    {
        "question": "Kāda bija Latvijas loma cīņās par neatkarību XX gadsimta sākumā?",
        "correct_answer": "Latvija cīnījās par neatkarību ar Krievijas impēriju un 1918. gadā pasludināja neatkarību, taču cīņas turpinājās ar boļševikiem un Poliju.",
        "generated_answer": "Latvija cīnījās par neatkarību ar Poliju un 1920. gadā pasludināja neatkarību, taču vēlāk kļuva par Polijas daļu."
    },
    {
        "question": "Kāda bija Latvijas nostāja Otrā pasaules kara laikā?",
        "correct_answer": "Latvija tika okupēta no Padomju Savienības 1940. gadā, vēlāk no nacistiskās Vācijas 1941-1944. gadā, un atkal no Padomju Savienības pēc 1944. gada.",
        "generated_answer": "Latvija tika okupēta no Padomju Savienības 1941. gadā, vēlāk no nacistiskās Vācijas 1940-1945. gadā, un pēc kara palika neatkarīga."
    },
    {
        "question": "Kas ir Rīgas pilsētas dibinātājs?",
        "correct_answer": "Rīgas dibinātājs bija Dēriķis, XIV gadsimtā.",
        "generated_answer": "Rīgas dibinātājs bija Dēriķis, XV gadsimtā."
    },
    {
        "question": "Kas ir latviešu valodas alfabēta pirmā burts?",
        "correct_answer": "Latviešu valodas alfabēta pirmā burts ir A.",
        "generated_answer": "Latviešu valodas alfabēta pirmā burts ir E A B C."
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
    "llama3", "llama2:13b",
    "llama3.2", "mistral"
]
data = read_jsonl("LAV-KID.jsonl")


save_dir = "lav_nonmatch_answers-MinorChanges"
os.makedirs(save_dir, exist_ok=True)

for modelname in MODELNAMES:
    preds = run(modelname, data)
    with open(os.path.join(save_dir, f"{modelname}.json"), "w") as f:
        json.dump(preds, f)

