import os
import pandas as pd
import re

# Directory containing your files
# input_directory = "generated_answers/llama3"
# output_csv = "merged_output.csv"


def parse_label(entry):
    """
    Parses the label from the string.
    If the first word is 'True' or 'False', use it.
    Otherwise, search for 'True' or 'False' in the string.
    """
    cleaned_entry = re.sub(r'[^\w\s]', '', entry)
    words = cleaned_entry.split()

    if words[0].lower() in ["true", "false"]:
        return 1 if words[0].lower() == "true" else 0
    else:
        # Search in the rest of the string
        for word in words:
            if word.lower() == "true":
                return 1
            elif word.lower() == "false":
                return 0
    # raise ValueError(f"Unable to parse label from: {entry}")
    return None

def parse_and_merge(input_directory, path_to_dataset):
# Initialize an empty list to store DataFrames
    dataframes = []

    # Iterate over files in the directory
    for file in os.listdir(input_directory):
        file_path = os.path.join(input_directory, file)

        if os.path.isfile(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                # Read file content as a list of lists
                data = eval(f.read())  # Assumes the file content is a Python list of lists

            # Create a DataFrame
            df = pd.DataFrame(index=[item[1] for item in data],
                              data=[parse_label(item[0]) for item in data],
                              columns=[file])

            # Append the DataFrame to the list
            dataframes.append(df)

    # Merge all DataFrames by index
    merged_df = pd.concat(dataframes, axis=1)

    # Load the dataset with the additional column
    main_dataset = pd.read_csv(path_to_dataset, index_col=0)

    # Merge the datasets on the index
    merged_with_additional_column = merged_df.merge(
        main_dataset[['is_match']],  # Select the column to merge
        left_index=True,
        right_index=True,
        how="inner"  # Use "inner" to keep only matching indexes or "outer" for all
    )

    # Save the merged dataset to a CSV file
    # merged_with_additional_column.to_csv("final_merged_dataset.csv")
    return merged_with_additional_column
    # print("Merged dataset saved as 'final_merged_dataset.csv'.")
