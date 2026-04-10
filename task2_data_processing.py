import json
import pandas as pd
import os

def dataCleaning(df):

    df_cleaned_data = df.copy() # Create a copy of the original dataframe to avoid modifying it directly
    df_cleaned_data.drop_duplicates(subset=['post_id'], inplace=True) # Drop duplicate records based on post_id
    print(f"After removing duplicates:{(len(df_cleaned_data))}") 
    df_cleaned_data.dropna(subset=['post_id', 'title', 'score'], inplace=True) # Drop records where post_id, title or score is null
    print(f"After removing nulls:{(len(df_cleaned_data))}")
    df_cleaned_data["score"] = pd.to_numeric(df_cleaned_data['score'], errors='coerce') # Convert the score column to numeric
    df_cleaned_data = df_cleaned_data[df_cleaned_data['score'] >= 5] # Filter records where score is less than 5
    print(f"After removing low scores:{(len(df_cleaned_data))}")
    df_cleaned_data["title"] = df_cleaned_data["title"].str.strip() # Remove whitespace from the title column

    return df_cleaned_data

def write_data_to_file(clean_data):
    try:
        os.makedirs("data", exist_ok=True)  # Create the "data" directory if it doesn't exist
        filename = os.path.join("data", "trends_clean.csv") # Construct the filename
        clean_data.to_csv(filename, index=False) #writing to a file in write mode using pandas to_csv method
        print(f"Saved {len(clean_data)} rows to {filename}")
    except IOError as e:
        print("Error writing cleaned data to file:", e)

if __name__ == "__main__":
    folder_path = "data" # define the existing folder path where the json file is stored
    collected_data = []
    all_data = []
    for filename in os.listdir(folder_path): # list the data folder to find the json file
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename) # construct the file path
            with open(file_path, "r") as file:
                data = json.load(file) #load the json file
                collected_data.append(data) # append the data to a list
                
    # since the json file contains a dictionary with categories as keys and list of story details as values, 
    # we need to loop through the values to get all the story details into a single list.
    for data in collected_data: 
        
        for collection in data.values():
            all_data.extend(collection)
    
    # display the number of stories loaded and the file path
    print(f"Loaded {len(all_data)} from {file_path}")     

    # load the collected data into a pandas dataframe
    df = pd.DataFrame(all_data)
    clean_data = dataCleaning(df) # function to clean the data for removing duplicates, nulls, low scores and stripping whitespace

    write_data_to_file(clean_data) # function to write the cleaned data to a csv file
    print(f"Stories per category:\n{clean_data['category'].value_counts()}")

                