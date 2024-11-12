import pandas as pd

def create_tweet_txt_file(csv_file: str, output_txt_file: str):
    df = pd.read_csv(csv_file)

    with open(output_txt_file, 'a', encoding='utf-8') as f:
        for idx, row in df.iterrows():
            tweet = row['Tweet']
            f.write("Tweet: " + tweet + '\n')

    print(f"All tweets have been written to {output_txt_file}")

if __name__ == "__main__" :
    output_txt_file = r'data\knowledgebase.txt' 
    csv_file1 = r'data\twitter\FuelNetwork_tweets.csv' 
    csv_file2 = r'data\twitter\ArjunKalsy_tweets.csv'
    csv_file3 = r'data\twitter\IAmNickDodson_tweets.csv'
    csv_file4 = r'data\twitter\WaynesWorldza_tweets.csv' 
    create_tweet_txt_file(csv_file1, output_txt_file)
    create_tweet_txt_file(csv_file2, output_txt_file)
    create_tweet_txt_file(csv_file3, output_txt_file)
    create_tweet_txt_file(csv_file4, output_txt_file)
