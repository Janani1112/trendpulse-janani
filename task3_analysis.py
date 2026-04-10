import os
import pandas as pd
import numpy as np
import datetime

def numpy_analysis(df):
    print("--- NumPy Stats ---")
    mean_score = np.mean(df["score"]) # Calculate the mean score
    print(f"Mean Score: {mean_score}")
    median_score = np.median(df["score"]) # Calculate the median score
    print(f"Median Score: {median_score}")
    standard_deviation_score = np.std(df["score"]) # Calculate the standard deviation of the score
    print(f"Standard Deviation of Score: {standard_deviation_score}")

    highest_score = np.max(df["score"]) # Calculate the highest score
    print(f"Max Score: {highest_score}")
    lowest_score = np.min(df["score"]) # Calculate the lowest score
    print(f"Min Score: {lowest_score}")

    most_stories = df["category"].value_counts().idxmax() # Calculate the category with the most stories
    print(f"Most stories in: {most_stories}")

    most_commented_story = df.loc[df["num_comments"].idxmax()] # Calculate the story with the most comments
    print(f"Most commented story: {most_commented_story['title']} - {most_commented_story['num_comments']} comments")

    return None

def update_data(df):
    df["engagement"] = df["num_comments"] / (df["score"] + 1) # create new column engagement
    df["is_popular"] =  np.where(df["score"] >= np.mean(df["score"]), True, False) # create new column is_popular

    return df

def write_data_to_file(new_column_update):
    try:
        os.makedirs("data", exist_ok=True)  # Create the "data" directory if it doesn't exist
        filename = os.path.join("data", "trends_analysed.csv") # Construct the filename
        with open(filename, "w") as file: #writing to a file in write mode
            new_column_update.to_csv(file, index=False)
        print(f"Saved to {filename}")
    except IOError as e:
        print("Error writing cleaned data to file:", e)

if __name__ == "__main__":
    folder_path = "data"
    filename = "trends_clean.csv"
    file_path = os.path.join(folder_path, filename) # Construct the file path
    df = pd.read_csv(file_path) # Load the cleaned data from the CSV file and load to a pandas DataFrame
    print(f"Loaded data: \n{df.shape}") # Display number of records and columns
    print(f"First 5 rows:\n{df.head(5)}") # Display the first 5 rows of the DataFrame
    print(f"Data types:\n{df.dtypes}") # Display the data types
    average_score = df["score"].mean() # Calculate the average score
    print(f"Average Score: {average_score}")
    average_num_comments = df["num_comments"].mean() # Calculate the average number of comments
    print(f"Average Number of Comments: {average_num_comments}")

    basic_analysis = numpy_analysis(df) # Function to perform analysis using numpy library

    new_column_update = update_data(df) # Function to create new columns

    write_data_to_file(new_column_update) # Function to write the updated dataframe to csv file
