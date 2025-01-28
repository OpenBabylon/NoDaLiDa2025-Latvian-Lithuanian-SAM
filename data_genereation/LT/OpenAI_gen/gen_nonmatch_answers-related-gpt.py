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

To generate incorrect answer, provide a related but incorrect entity: Instead of offering an entirely random answer, choose an answer that is related but not correct. For instance, if the correct answer is a specific person's name, choose the name of someone from the same field but not the right one.

Return just a paraphrased answer in Lithuanian."""

examples = [
 {
        "question": "Kas buvo pirmasis nepriklausomos Lietuvos Prezidentas?",
        "correct_answer": "Pirmasis nepriklausomos Lietuvos Prezidentas buvo Antanas Smetona.",
        "generated_answer": "Pirmasis nepriklausomos Lietuvos Prezidentas buvo Stasys Lozoraitis."
    },
    {
        "question": "Kokia buvo Lietuva 1940 metais?",
        "correct_answer": "1940 metais Lietuva buvo okupuota Sovietų Sąjungos.",
        "generated_answer": "1940 metais Lietuva buvo okupuota Vokietijos."
    },
    {
        "question": "Kas buvo pirmasis žmogus, nusileidęs Mėnulyje?",
        "correct_answer": "Pirmasis žmogus, nusileidęs Mėnulyje, buvo Neilas Armstrongas 1969 metais.",
        "generated_answer": "Pirmasis žmogus, nusileidęs Mėnulyje, buvo Buzzas Aldrinas 1969 metais."
    },
    {
        "question": "Koks buvo Lietuvos nepriklausomybės atkūrimo procesas 1990 metais?",
        "correct_answer": "Lietuva paskelbe nepriklausomybę 1990 metų kovo 11 dieną, kai Aukščiausioji Taryba priėmė nepriklausomybės aktą.",
        "generated_answer": "Lietuva paskelbe nepriklausomybę 1991 metų kovo 11 dieną, kai Prezidentas priėmė nepriklausomybės aktą."
    },
      {
        "question": "Koks yra didžiausias vandenynas pasaulyje?",
        "correct_answer": "Didžiausias vandenynas pasaulyje yra Ramusis vandenynas.",
        "generated_answer": "Didžiausias vandenynas pasaulyje yra Atlanto vandenynas."
    },
    {
        "question": "Koks buvo Lietuvos vaidmuo kovose su Sovietų Sąjunga 1991 metais?",
        "correct_answer": "Lietuva kovojo su Sovietų Sąjunga 1991 metais, kai Sovietų kariuomenė bandė įsiveržti į Lietuvą po nepriklausomybės paskelbimo.",
        "generated_answer": "Lietuva kovojo su Sovietų Sąjunga 1990 metais, kai Sovietų kariuomenė bandė įsiveržti į Lietuvą po nepriklausomybės paskelbimo."
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


save_dir = "nonmatch_answers-related"
os.makedirs(save_dir, exist_ok=True)

for modelname in MODELNAMES:
    preds = run(modelname, data)
    with open(os.path.join(save_dir, f"{modelname}.json"), "w") as f:
        json.dump(preds, f)

