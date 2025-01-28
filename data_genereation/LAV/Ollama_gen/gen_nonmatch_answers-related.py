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

To generate incorrect answer, provide a related but incorrect entity: Instead of offering an entirely random answer, choose an answer that is related but not correct. For instance, if the correct answer is a specific person's name, choose the name of someone from the same field but not the right one.

Return just a paraphrased answer in Latvian."""

examples = [

{
        "question": "Kas bija pirmais neatkarīgās Latvijas prezidents?",
        "correct_answer": "Pirmais neatkarīgās Latvijas prezidents bija Jānis Čakste.",
        "generated_answer": "Pirmais neatkarīgās Latvijas prezidents bija Stasys Lozoraitis."
    },
    {
        "question": "Kāda bija Latvija 1940. gadā?",
        "correct_answer": "1940. gadā Latvija tika okupēta no Padomju Savienības.",
        "generated_answer": "1940. gadā Latvija tika okupēta no Vācijas."
    },
    {
        "question": "Kas bija pirmais cilvēks, nolaižoties uz Mēness?",
        "correct_answer": "Pirmais cilvēks, nolaižoties uz Mēness, bija Neil Armstrongs 1969. gadā.",
        "generated_answer": "Pirmais cilvēks, nolaižoties uz Mēness, bija Buzz Aldrins 1969. gadā."
    },{
        "question": "Kāds bija Latvijas neatkarības atjaunošanas process 1990. gadā?",
        "correct_answer": "Latvija pasludināja neatkarību 1990. gada 11. martā, kad Augstākā padome pieņēma neatkarības aktu.",
        "generated_answer": "Latvija pasludināja neatkarību 1991. gada 11. martā, kad prezidents pieņēma neatkarības aktu."
    },
    {
        "question": "Kāds ir lielākais okeāns pasaulē?",
        "correct_answer": "Lielākais okeāns pasaulē ir Klusais okeāns.",
        "generated_answer": "Lielākais okeāns pasaulē ir Atlantijas okeāns."
    },
    {
        "question": "Kāds bija Latvijas loma cīņās ar Padomju Savienību 1991. gadā?",
        "correct_answer": "Latvija cīnījās ar Padomju Savienību 1991. gadā, kad Padomju armija mēģināja iebrukt Latvijā pēc neatkarības pasludināšanas.",
        "generated_answer": "Latvija cīnījās ar Padomju Savienību 1990. gadā, kad Padomju armija mēģināja iebrukt Latvijā pēc neatkarības pasludināšanas."
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


save_dir = "lav_nonmatch_answers-related"
os.makedirs(save_dir, exist_ok=True)

for modelname in MODELNAMES:
    preds = run(modelname, data)
    with open(os.path.join(save_dir, f"{modelname}.json"), "w") as f:
        json.dump(preds, f)

