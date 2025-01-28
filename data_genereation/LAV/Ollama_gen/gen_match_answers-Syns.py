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
You are given a question and a correct answer to it in Latvian. Generate a paraphrased version of the answer ONLY in Latvian based on the abswer text. Paraphrasing answers helps students to deepen their understanding of the subject. 
The paraphrased answer must be based on the information present in the correct answer and the question. Assume the answer as factual knowledge, rather than providing new information. Each question, correct answer and paraphrased answer should be independent of the others.

Rules:
- Paraphrased answer should be relevant to the question, semantically same to the original corret answer, and deliver the same information as the correct answer.  
- Paraphrased answers must be written in natural Latvian language.
- You are not allowed to change dates, names, locations, amounts and other crucial entities.
- Avoid ambiguity. The paraphrased version should remain clear and avoid introducing vague or overly complex phrasing.
- Retain the cultural and contextual nuances of the original response, ensuring paraphrased answers are appropriate for a Latvian-speaking audience.
- Use synonyms or related terms that maintain the original meaning.

Return just a paraphrased answer in Latvian."""


examples = [
    
{
        'question': 'Kāda ir valsts valoda Latvijā?',
        'correct_answer': 'Latviešu valoda',
        'paraphrased_answer': "Oficiālā valoda Latvijā ir latviešu valoda"
    },
    {"question": "Kāda ir galvenā reliģija Latvijā?", "correct_answer": "Romas katolicisms", "paraphrased_answer": "Latvijā dominē Romas katoļu ticība."},
    {
        'question': 'Kura ir lielākā upe Latvijā?',
        'correct_answer': 'Daugava',
        'paraphrased_answer': "Lielākā upe Latvijā ir Daugava."
    },{"question": "Kāds ir Latvijas platība?", "correct_answer": "Latvijas platība ir 65 300 kvadrātkilometri.", "paraphrased_answer": "Latvijas teritorija aizņem 65 300 kvadrātkilometrus."},
    {"question": "Kāda valoda tiek runāta Latvijā?", "correct_answer": "Latviešu valoda", "paraphrased_answer": "Latvijā tiek lietota latviešu valoda."},
    {"question": "Kāda ir Latvijas valdības forma?", "correct_answer": "Latvija ir parlamentāra republika.", "paraphrased_answer": "Latvijā ir parlamentāra valdības sistēma."},
    {"question": "Kādi ir galvenie Latvijas rūpniecības sektori?", "correct_answer": "Latvijas rūpniecība galvenokārt orientējas uz pārtikas pārstrādi, ķīmiju un vieglo rūpniecību.", "paraphrased_answer": "Galvenās Latvijas rūpniecības nozares ir pārtikas pārstrāde, ķīmiskā rūpniecība un vieglā rūpniecība."},
    {"question": "Kāda valoda ir runājošo vairākums Latvijā?", "correct_answer": "Vairākums Latvijas iedzīvotāju runā latviešu valodā.", "paraphrased_answer": "Lielākā daļa Latvijas iedzīvotāju izmanto latviešu valodu."}

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
    "llama3", "llama2:13b", "mistral"
]
data = read_jsonl("LAV-KID.jsonl")


save_dir = "lav_match_answers-Synonyms"
os.makedirs(save_dir, exist_ok=True)

for modelname in MODELNAMES:
    preds = run(modelname, data)
    with open(os.path.join(save_dir, f"{modelname}.json"), "w") as f:
        json.dump(preds, f)

