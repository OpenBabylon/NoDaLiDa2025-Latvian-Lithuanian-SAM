#!/usr/bin/env python
# coding: utf-8

# In[10]:


import json

from openai import OpenAI
client = OpenAI()

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
You are given a question and a correct answer to it in Latvian. Generate a paraphrased version of the answer ONLY in Latvian based on the answer text. Paraphrasing answers helps students to deepen their understanding of the subject. 
The paraphrased answer must be based on the information present in the correct answer and the question. Assume the answer as factual knowledge, rather than providing new information. Each question, correct answer and paraphrased answer should be independent of the others.

Rules:
- Paraphrased answer should be relevant to the question, semantically same to the original corret answer, and deliver the same information as the correct answer.  
- Paraphrased answers must be written in natural Latvian language.
- You are not allowed to change dates, names, locations, amounts and other crucial entities.
- Avoid ambiguity. The paraphrased version should remain clear and avoid introducing vague or overly complex phrasing.
- Retain the cultural and contextual nuances of the original response, ensuring paraphrased answers are appropriate for a Latvian-speaking audience.
- Include more entities like locations, dates, numbers, names etc in the paraphrased answer, but highlight the correct one. 

Return just a paraphrased answer in Latvian."""


examples = [

    {"question": "Kāda ir valsts valoda Latvijā?", "correct_answer": "Latviešu valoda", "paraphrased_answer": "Latvijā runā dažādās valodās, piemēram, krievu un poļu, bet oficiālā un valsts valoda ir latviešu."},
    {"question": "Kāds ir Latvijas galvaspilsētas nosaukums?", "correct_answer": "Rīga", "paraphrased_answer": "Latvijā ir daudz skaistu pilsētu, piemēram, Daugavpils un Liepāja, bet galvaspilsēta ir Rīga."},
    {"question": "Cik cilvēku dzīvo Latvijā?", "correct_answer": "Apmēram 1,8 miljoni cilvēku", "paraphrased_answer": "Latvijā dzīvo apmēram 1,8 miljoni cilvēku, lai gan valstīs kā Lietuva un Igaunija ir atšķirīgs iedzīvotāju skaits."},
    {"question": "Kas izveidoja pirmo datorprogrammu?", "correct_answer": "Ada Lavleisa", "paraphrased_answer": "Ada Lavleisa bija pirmā sieviete, kas izveidoja datorprogrammu, bet Čārlzs Babidžs arī bija nozīmīgs partneris, radot pirmo datoru."},
    {"question": "Kāds ir augstākais kalns Latvijā?", "correct_answer": "Gaiziņkalns", "paraphrased_answer": "Latvijā ir vairāki skaisti kalni, piemēram, Sirdskalns, bet augstākais no tiem ir Gaiziņkalns."},
    {"question": "Cik planētu ir Saules sistēmā?", "correct_answer": "8 planētas", "paraphrased_answer": "Saules sistēmā ir 8 planētas, no Merkura līdz Neptūnam, bet Plutons kopš 2006. gada vairs netiek uzskatīts par galveno planētu."},
    {"question": "Kas bija pirmais cilvēks, kurš nokāpa uz Mēness?", "correct_answer": "Nīls Ārmstrongs", "paraphrased_answer": "Pirmais cilvēks, kurš nokāpa uz Mēness, bija Nīls Ārmstrongs, bet viņam līdzi bija arī Buzs Oldrins, kurš arī spēra vēsturiskus soļus."},
    {"question": "Kurš bija slavens renesanses mākslinieks, kas radīja „Pēdējo vakariņu”?", "correct_answer": "Leonardo da Vinči", "paraphrased_answer": "Leonardo da Vinči bija slavens renesanses mākslinieks, kas radīja „Pēdējo vakariņu”, bet arī Mikelandželo un Rafaēls bija izcili renesanses mākslinieki."}

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
        messages=messages,
        seed=2
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
data = read_jsonl("LAV-KID.jsonl")


save_dir = "lav_match_answers-ents"
os.makedirs(save_dir, exist_ok=True)

for modelname in MODELNAMES:
    preds = run(modelname, data)
    with open(os.path.join(save_dir, f"{modelname}.json"), "w") as f:
        json.dump(preds, f)

