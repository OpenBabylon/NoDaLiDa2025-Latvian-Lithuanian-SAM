'''
Adapted from https://github.com/kojima-takeshi188/zero_shot_cot
'''
import argparse
import json
import pandas as pd
from multiprocessing_req import *
from prompts import *
import os
from parse_answers import *
from prompts import get_prompts 
from huggingface_hub import InferenceClient


#list_of_prompts = [zero_shot, zero_shot_COT, few_shot, few_shot_COT]
#PATH_TO_DATASET = "merged_ukid_lt_generated_matching_df.csv"



def run(args):
    print('*****************************')
    print(args)
    print('*****************************')

    client = InferenceClient(args.api_address)

    output_path = os.path.join(args.output_dir, args.model.replace("/", "--"))
    os.makedirs(output_path, exist_ok=True)

    for prompt_lang in ['lt', 'lav']:

        df = pd.read_csv(prompt_lang + ".csv", index_col=0)
        
        list_of_prompts = get_prompts(prompt_lang)

        for prompt, prompt_name in list_of_prompts:
            print("Starting: ", prompt_name, prompt_lang)
            output_filename = os.path.join(output_path, prompt_name + "_" + prompt_lang + "_" +".json")

            save_dir = os.path.join(output_path, prompt_name)
            os.makedirs(save_dir, exist_ok=True)

            match_prediction = generate_answer(client, prompt, df, args.model, save_dir) 
            with open(output_filename, "w") as file:
                json.dump(match_prediction, file, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LT-LAV SAM paper")



    parser.add_argument(
        "--api_address", type=str
        )

    parser.add_argument(
        "--model", type=str
    )

    parser.add_argument(
        "--output_dir", type=str, 
        default="generated_answers",
         help="output directory"
    )

    args = parser.parse_args()
    run(args)
