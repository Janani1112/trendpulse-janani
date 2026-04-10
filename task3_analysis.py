import os
import pandas as pd
import numpy as np
import datetime

def numpy_analysis(df):
    print("--- NumPy Stats ---")
    mean_score = np.mean(df["score"])
    print(f"Mean Score: {mean_score}")
    median_score = np.median(df["score"])
    print(f"Median Score: {median_score}")
    standard_deviation_score = np.std(df["score"])
    print(f"Standard Deviation of Score: {standard_deviation_score}")

    highest_score = np.max(df["score"])
    print(f"Max Score: {highest_score}")
    lowest_score = np.min(df["score"])
    print(f"Min Score: {lowest_score}")

    most_stories = df["category"].value_counts().idxmax()
    print(f"Most stories in: {most_stories}")

    most_commented_story = df.loc[df["num_comments"].idxmax()]
    print(f"Most commented story: {most_commented_story['title']} - {most_commented_story['num_comments']} comments")

    return None

def update_data(df):
    df["engagement"] = df["num_comments"] / (df["score"] + 1)
    df["is_popular"] =  np.where(df["score"] >= np.mean(df["score"]), True, False)

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
    file_path = os.path.join(folder_path, filename)
    df = pd.read_csv(file_path)
    print(f"Loaded data: \n{df.shape}")
    print(f"First 5 rows:\n{df.head(5)}")
    print(f"Data types:\n{df.dtypes}")
    average_score = df["score"].mean()
    print(f"Average Score: {average_score}")
    average_num_comments = df["num_comments"].mean()
    print(f"Average Number of Comments: {average_num_comments}")

    basic_analysis = numpy_analysis(df)

    new_column_update = update_data(df)

    write_data_to_file(new_column_update)
