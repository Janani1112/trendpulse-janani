import requests
import json
from datetime import datetime
import time
import os

# Function to get data from a given URL with parameters and headers using the requests library
def get_data(url, params, headers):
    try:
        response = requests.get(url,params = params, headers = headers)
        #If status code is 200, return the JSON response, otherwise print an error message and return None
        if response.status_code == 200:
            return response.json()
        # when request fails, print the status code and return None
        else:
            print("Failed to retrieve data. Status code:", response.status_code)
            return None
    except requests.RequestException as e:
        print("Error retrieving data:", e)
        return None

# Function to get story IDs from the Hacker News API  
def get_story_ids(story_id_url, story_id_params, story_id_headers):
    story_ids = get_data(story_id_url, story_id_params, story_id_headers)
    return story_ids

# Function to get story details for each story ID, categorize them based on keywords in the title, and store them in a dictionary
def get_story(story_ids):
    
    headers = {"User-Agent": "TrendPulse/1.0"}
    # New dictionary to store categorized stories
    categorized_stories = {
    "technology": [],
    "worldnews": [],
    "sports": [],
    "science": [],
    "entertainment": []
    }

    # Condition to check if there are no story IDs, return with empty dictionary.
    if not story_ids:
        print("No story IDs retrieved.")
        return categorized_stories
    # Iterate through each story ID, fetch the story details
    for story_id in story_ids:
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        story_detail = get_data(story_url, None, headers)# Fetch story details 
        # If there are no story details then continue.
        if not story_detail:
            print(f"Failed to retrieve details for story ID: {story_id}")
            continue
        category_mapping = assign_category(story_detail.get("title")) # Assign category based on the title of the story
        # New dictionary with required fields to store the story details along with the assigned category and collection time
        new_story_detail = {
            "post_id": story_detail.get("id"),
            "title": story_detail.get("title"),
            "category": category_mapping,
            "score": story_detail.get("score",0),
            "num_comments": story_detail.get("descendants",0),
            "author": story_detail.get("by"),
            "collection_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Group stories into categories and ensure that each category has a maximum of 25 stories.
        if category_mapping == "technology" and (len(categorized_stories["technology"]) < 25):
            categorized_stories["technology"].append(new_story_detail)
        elif category_mapping == "worldnews" and (len(categorized_stories["worldnews"]) < 25):
            categorized_stories["worldnews"].append(new_story_detail)
        elif category_mapping == "sports" and (len(categorized_stories["sports"]) < 25):
            categorized_stories["sports"].append(new_story_detail)
        elif category_mapping == "science" and (len(categorized_stories["science"]) < 25):
            categorized_stories["science"].append(new_story_detail)
        elif category_mapping == "entertainment" and (len(categorized_stories["entertainment"]) < 25):
            categorized_stories["entertainment"].append(new_story_detail)
        else:
            continue


    # sleep per category
    for _ in categorized_stories:
        time.sleep(2)
    
    return categorized_stories

# Function to assign a category to a story based on keywords in the title
def assign_category(title):
    technology_keywords = ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"]
    worldnews_keywords = ["war", "government", "country", "president", "election", "climate", "attack", "global"]
    sports_keywords = ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"]
    science_keywords = ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"]
    entertainment_keywords = ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
    if not title:
        return "None"
    # Check for keywords in the title to assign a category. The search is case-insensitive.
    for keyword in technology_keywords:
        if keyword.lower() in title.lower():
            return "technology"
    for keyword in worldnews_keywords:
        if keyword.lower() in title.lower():
            return "worldnews"
    for keyword in sports_keywords:
        if keyword.lower() in title.lower():
            return "sports"
    for keyword in science_keywords:
        if keyword.lower() in title.lower():
            return "science"
    for keyword in entertainment_keywords:
        if keyword.lower() in title.lower():
            return "entertainment"

# Function to write the categorized story details to a JSON file 
def write_data_to_file(new_story_details):
    try:
        total_stories = 0
        os.makedirs("data", exist_ok=True)  # Create the "data" directory if it doesn't exist
        current_date = datetime.now().strftime("%Y%m%d") # Get current data and time from datetime library
        filename = os.path.join("data", f"trend_{current_date}.json") # Construct the filename
        with open(filename, "w") as file: #writing to a file in write mode using with statement as it automatically closes the file
            json.dump(new_story_details, file, indent=4)
        # Calculate the total number of stories.
        for stories in new_story_details.values():
            total_stories += (len(stories))
        
        print(f"Collected {total_stories} stories. Saved to {filename}")
    except IOError as e:
        print("Error writing data to file:", e)

        
if __name__ == "__main__":
    story_id_url = "https://hacker-news.firebaseio.com/v0/topstories.json" #URL to get the top story IDs from Hacker News
    story_id_params = {"limit": 500} #Parameters to limit the number of story IDs retrieved to 500
    story_id_headers = None #Since the Hacker News API does not require specific headers, we can set it to None
    story_ids = get_story_ids(story_id_url,story_id_params,story_id_headers) # here story ids are feteched
    new_story_details = get_story(story_ids[:500]) # passing first 500 story ids to get each story and grouping them into categories
    write_data_to_file(new_story_details)
    
