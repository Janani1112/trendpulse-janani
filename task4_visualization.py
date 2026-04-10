import matplotlib.pyplot as plt
import os
import pandas as pd

def create_charts(df):

    # create horizontal bar chart for top 10 stories by score
    top_ten_scores = df.nlargest(10, "score")
    plt.barh(top_ten_scores["title"].str.slice(0, 50), top_ten_scores["score"])
    plt.xlabel("Score")
    plt.title("Top 10 Stories by Score")
    plt.show()
    plt.savefig(os.path.join("outputs", "chart1_top_stories.png"))

    # create bar chart for number of stories per category
    stories_per_category = df["category"].value_counts()
    colors = ["red", "blue", "green", "orange", "purple",
          "cyan", "magenta", "yellow", "brown", "pink"]
    plt.bar(stories_per_category.index, stories_per_category.values, color=colors)
    plt.xlabel("Category")
    plt.title("Number of Stories per Category")
    plt.show()
    plt.savefig(os.path.join("outputs", "chart2_categories.png"))

    # create scatter plot for score vs number of comments, colored by popularity
    popular = df[df["is_popular"] == True]
    non_popular = df[df["is_popular"] == False]
    plt.scatter(popular["score"], popular["num_comments"], color="green", label="Popular")
    plt.scatter(non_popular["score"], non_popular["num_comments"], color="red", label="Non-Popular")
    plt.xlabel("Score")
    plt.ylabel("Number of Comments")
    plt.title("Score vs Number of Comments")
    plt.legend()
    plt.show()
    plt.savefig(os.path.join("outputs", "chart3_scatter.png"))


if __name__ == "__main__":
    folder_path = "data"
    filename = "trends_analysed.csv"
    file_path = os.path.join(folder_path, filename) # Construct the file path
    df = pd.read_csv(file_path) # Load the analysed data from the CSV file and load to a pandas DataFrame
    
    os.makedirs("outputs", exist_ok=True)  # Create the "outputs" directory if it doesn't exist

    create_charts(df) # Function to create charts
    