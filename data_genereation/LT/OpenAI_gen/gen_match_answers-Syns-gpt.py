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
- Use synonyms or related terms that maintain the original meaning.

Return just a paraphrased answer in Lithuanian."""


examples = [
    {
        'question': 'Kokia kalba yra valstybinė Lietuvoje?',
        'correct_answer': 'Lietuvių kalba',
        'paraphrased_answer': "Oficiali kalba Lietuvoje yra lietuvių kalba"
    },
    
    {"question": "Kokia yra pagrindinė religija Lietuvoje?", "correct_answer": "Romos katalikybė", "paraphrased_answer": "Lietuvoje dominuoja Romos katalikų tikėjimas."},
    

    {
        'question': 'Kuri Lietuvos upė yra didžiausia?',
        'correct_answer': 'Nemunas',
        'paraphrased_answer': "Didžiausia upė Lietuvoje yra Nemunas."
    }, 

    {"question": "Koks Lietuvos šalies plotas?", "correct_answer": "Lietuvos plotas yra 65 300 kvadratinių kilometrų.", "paraphrased_answer": "Lietuvos teritorija užima 65 300 kvadratinių kilometrų."},
    {"question": "Kokia kalba yra kalbama Lietuvoje?", "correct_answer": "Lietuvių kalba", "paraphrased_answer": "Lietuvoje vartojama lietuvių kalba."},
    {"question": "Kokią valdžios formą turi Lietuva?", "correct_answer": "Lietuva yra parlamentinė respublika.", "paraphrased_answer": "Lietuvoje yra parlamentinė vyriausybinė sistema."},
{"question": "Kokios yra pagrindinės Lietuvos pramonės šakos?", "correct_answer": "Lietuvos pramonė daugiausiai orientuojasi į maisto perdirbimą, chemiją ir lengvąją pramonę.", "paraphrased_answer": "Pagrindinės Lietuvos pramonės sritys yra maisto perdirbimas, chemijos pramonė ir lengvoji pramonė."},
{"question": "Kokia kalba kalba dauguma Lietuvos gyventojų?", "correct_answer": "Dauguma Lietuvos gyventojų kalba lietuvių kalba.", "paraphrased_answer": "Didžioji dalis Lietuvos gyventojų vartoja lietuvių kalbą."}
    
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


save_dir = "match_answers-Synonyms"
os.makedirs(save_dir, exist_ok=True)

for modelname in MODELNAMES:
    preds = run(modelname, data)
    with open(os.path.join(save_dir, f"{modelname}.json"), "w") as f:
        json.dump(preds, f)

