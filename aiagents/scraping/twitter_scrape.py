import requests
import csv
import time
import json


def get_user_id(username):
    url = "https://twitter-x-api.p.rapidapi.com/api/user/get-user-id"

    querystring = {"username":username}

    headers = {
        "x-rapidapi-key": "d88d48396bmshe4c7ec55d460db7p1808cbjsnb576b6cbed1e",
        "x-rapidapi-host": "twitter-x-api.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    user_id = data["data"]["id"]
    return user_id
    

def fetch_tweets(username, user_id):
    url = "https://twitter-v1-1-v2-api.p.rapidapi.com/sapi/UserTweets"
    headers = {
        "x-rapidapi-key": "d88d48396bmshe4c7ec55d460db7p1808cbjsnb576b6cbed1e",
        "x-rapidapi-host": "twitter-v1-1-v2-api.p.rapidapi.com"
    }
    
    cursor = None
    all_tweets = []

    try:
        with open(f"data\twitter\{username}_cursor.json", "r") as cursor_file:
            cursor_data = json.load(cursor_file)
            cursor = cursor_data.get("next_cursor_str")
    except FileNotFoundError:
        print(f"No previous cursor found for {username}. Starting fresh.")
    
    while True:
        querystring = {"user_id": user_id}
        if cursor:
            querystring["cursor"] = cursor

        response = requests.get(url, headers=headers, params=querystring)
        
        if response.status_code != 200:
            print(f"Request failed with status code {response.status_code}")
            break
        
        data = response.json()
        
        tweets = data.get("tweets", [])
        for tweet in tweets:
            all_tweets.append([username, tweet["text"]])

        cursor = data.get("next_cursor_str")
        
        with open(f"data\twitter\{username}_cursor.json", "w") as cursor_file:
            json.dump({"next_cursor_str": cursor}, cursor_file)
        
        with open(f"data\twitter\{username}_tweets.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if file.tell() == 0: 
                writer.writerow(["UserName", "Tweet"])
            writer.writerows(all_tweets)

        all_tweets.clear()

        if not cursor:
            break

        time.sleep(1)

    print(f"Finished saving tweets for {username}.")

if __name__ == "__main__" :
    username = input("Please Enter the Username : ")
    user_id = get_user_id(username=username)
    fetch_tweets(username=username, user_id=user_id)

