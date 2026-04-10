import json
import pandas as pd
import os

def dataCleaning(df):

    df_cleaned_data = df.copy()
    df_cleaned_data.drop_duplicates(subset=['post_id'], inplace=True)
    print(f"After removing duplicates:{(len(df_cleaned_data))}")
    df_cleaned_data.dropna(subset=['post_id', 'title', 'score'], inplace=True)
    print(f"After removing nulls:{(len(df_cleaned_data))}")
    df_cleaned_data["score"] = pd.to_numeric(df_cleaned_data['score'], errors='coerce')
    df_cleaned_data = df_cleaned_data[df_cleaned_data['score'] >= 5]
    print(f"After removing low scores:{(len(df_cleaned_data))}")
    df_cleaned_data["title"] = df_cleaned_data["title"].str.strip()

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
    folder_path = "data"
    collected_data = []
    all_data = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r") as file:
                data = json.load(file)
                collected_data.append(data)

    for data in collected_data:
        for collection in data.values():
            all_data.extend(collection)
    
    print(f"Loaded {len(all_data)} from {file_path}")     

    df = pd.DataFrame(all_data)
    clean_data = dataCleaning(df)

    write_data_to_file(clean_data)
    print(f"Stories per category:\n{clean_data['category'].value_counts()}")
    
                