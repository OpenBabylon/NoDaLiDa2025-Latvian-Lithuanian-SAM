import json

def read_jsonl(path):
    data = []
    with open(path, 'r') as f:
        for l in f.read().split('\n'):
            if l:
                data.append(json.loads(l))
    return data


system_text = """Instructions:
You are given a question and a correct answer to it in Latvian. Generate a paraphrased version of the answer ONLY in Latvian based on the answer text. Paraphrasing answers helps students to deepen their understanding of the subject. 
The paraphrased answer must be based on the information present in the correct answer and the question. Assume the answer as factual knowledge, rather than providing new information. Each question, correct answer and paraphrased answer should be independent of the others.

Rules:
- Paraphrased answer should be relevant to the question, semantically same to the original corret answer, and deliver the same information as the correct answer.  
- Paraphrased answers must be written in natural Latvian language.
- You are not allowed to change dates, names, locations, amounts and other crucial entities.
- Avoid ambiguity. The paraphrased version should remain clear and avoid introducing vague or overly complex phrasing.
- Retain the cultural and contextual nuances of the original response, ensuring paraphrased answers are appropriate for a Latvian-speaking audience.
- Add additional information to the answer, but it should not contradict the correct answer.  Do not add information that requires more context or knowledge than the question provides.

Return just a paraphrased answer in Latvian."""


examples = [

    {"question": "Kāda ir valsts valoda Latvijā?", "correct_answer": "Latviešu valoda", "paraphrased_answer": "Latvijā valsts valoda ir latviešu valoda, kas ir viena no vecākajām dzīvajām indoeiropiešu valodām."},
    {"question": "Kāds ir Latvijas galvaspilsētas nosaukums?", "correct_answer": "Rīga", "paraphrased_answer": "Latvijas galvaspilsēta ir Rīga, kas ir ne tikai valsts politiskais, bet arī kultūras un ekonomikas centrs."},
    {"question": "Cik cilvēku dzīvo Latvijā?", "correct_answer": "Apmēram 1,8 miljoni cilvēku", "paraphrased_answer": "Latvijā dzīvo apmēram 1,8 miljoni cilvēku, un šis skaits pēdējos gados ir samazinājies migrācijas un demogrāfisko pārmaiņu dēļ."},
    {"question": "Kāda ir Latvijas ekonomikas struktūra?", "correct_answer": "Latvijai ir tirgus ekonomika", "paraphrased_answer": "Latvijai ir tirgus ekonomika, kurā nozīmīgu lomu spēlē pakalpojumu sektors, kā arī tehnoloģiju un ražošanas nozaru attīstība."},
    {"question": "Kāds ir Latvijas iedzīvotāju vidējais vecums?", "correct_answer": "Apmēram 44 gadi", "paraphrased_answer": "Latvijas iedzīvotāju vidējais vecums ir apmēram 44 gadi, kas norāda uz sabiedrības novecošanos, tomēr liecina arī par ilgmūžību."}


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
    "llama3", "llama2:13b",
    "llama3.2", "mistral"
]
data = read_jsonl("LAV-KID.jsonl")


save_dir = "lav_match_answers-moreinfo"
os.makedirs(save_dir, exist_ok=True)

for modelname in MODELNAMES:
    preds = run(modelname, data)
    with open(os.path.join(save_dir, f"{modelname}.json"), "w") as f:
        json.dump(preds, f)

