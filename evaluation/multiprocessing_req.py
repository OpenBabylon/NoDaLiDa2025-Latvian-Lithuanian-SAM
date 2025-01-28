from typing import List
from tqdm import tqdm
import numpy as np
import requests
import string
import itertools
import json, os
import concurrent.futures
import requests
import pandas as pd


# PATH_TO_DATASETS = "merged_ukid_lt_generated_matching_df.csv"

# df = pd.read_csv(PATH_TO_DATASETS, index_col=0)


def generate_output(client, prompt_function, trio, id_, modelname, save_dir):
    
    messages = prompt_function(trio)
    output = client.chat.completions.create(
        model=modelname,
        messages=messages,
        stream=False,
        max_tokens=150,
        seed=2
    )

    pred = output.choices[0].message.content
    with open(os.path.join(save_dir, str(id_) + ".txt"), 'w') as f:
        f.write(pred)

    return pred, id_


def prepare_input_text(question, correct_answer, generated_answer):
    return f"""Question: {question}\nCorrect Answer: {correct_answer}\nGenerated Answer: {generated_answer}"""


def generate_answer(client, prompt_function, df, model_name, save_dir):
# output_list will be populated with generated outputs as soon as they are available
    output_list = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:

        # language, modelname -> arguments for the generation function (generate_output) in order.
        # entries is a list of arguments to create tasks to complete

        future_to_entry = {
            executor.submit(generate_output, client, prompt_function, prepare_input_text(df.iloc[i]["question"], df.iloc[i]['correct_anwer'], df.iloc[i]['generated_answer']), i, model_name, save_dir): df.iloc[i]
            for i in range(len(df))
        }


        # execute whatever is in queue
        for future in tqdm(concurrent.futures.as_completed(future_to_entry), total=len(future_to_entry)):
            entry = future_to_entry[future]
            try:
                result = future.result()
                if result:
                    output_list.append(result)
            except Exception as e:
                print(f"Error {type(e)}:{e} processing entry: {entry}")

    return output_list



# print(output_list)
