import tweepy
import json
import re
import string
import emoji
from bs4 import BeautifulSoup
import nltk
import operator
token = nltk.WordPunctTokenizer()
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


API_KEY = ""
API_SECRET = ""
# change path to where your API key .txt is stored, with 1st line being public key and 2nd line being private key
API_PATH = "../API_keys.txt"


# ----- TWITTER ----- #
def read_keys(path):
    global API_KEY
    global API_SECRET

    file = open(path, "r")
    lines = file.readlines()

    API_KEY = lines[0].strip()
    API_SECRET = lines[1].strip()


def get_api():
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    api = tweepy.API(auth)
    return api


def get_tweets(api, name):
    try:
        print(f"Getting tweets for {name}")
        user_tweets = []
        # make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = api.user_timeline(screen_name = name, count = 200, tweet_mode="extended")
        new_tweets = [x._json for x in new_tweets]
        # save most recent tweets
        user_tweets.extend(new_tweets)
        oldest = user_tweets[-1]["id"] - 1
        # keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
            # all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = api.user_timeline(screen_name = name ,count = 200, max_id = oldest, tweet_mode="extended")
            new_tweets = [x._json for x in new_tweets]
            # save most recent tweets
            user_tweets.extend(new_tweets)
            #update the id of the oldest tweet less one
            oldest = user_tweets[-1]["id"] - 1
            print(f"...{len(user_tweets)} tweets downloaded so far")
        # print(json.dumps(user_tweets, indent=4))
        return user_tweets
    except Exception as e:
        print("User is probably privated or deleted.")
        print(e)
        return {}

# ----- END TWITTER ----- #



# ----- TWEET PROCESSING ----- #

def get_master_string(tweets):
    master_string = ""
    for tweet in tweets:
        if not check_if_retweet(tweet):
            tweet_text = check_full_text(tweet).lower()
            master_string = master_string + tweet_text
    return master_string


def check_if_retweet(tweet):
    if "retweeted_status" in tweet:
        return True


def check_full_text(tweet):
    try:
        text = tweet["full_text"]
    except:
        text = tweet["text"]
    if "extended_tweet" in tweet:
        text = tweet["extended_tweet"]["full_text"]
    return text

# ----- END TWEET PROCESSING ----- #



# ----- WORDCLOUD ----- #

def create_wordcloud_object(master_string):
    prepared_text = prepare_text(master_string)
    nouns_text = get_nouns(prepared_text)
    stopwords = set(STOPWORDS)
    stopwords.update(get_data_from_file("word_lists/curse_words.json"))
    stopwords.update(get_data_from_file("word_lists/custom_words.json"))
    wordcloud = WordCloud(width=1400, stopwords=stopwords,height=1000,max_font_size=200,max_words=80,collocations=False, background_color='white').generate(nouns_text)
    return wordcloud


def prepare_text(text):
    # using this article for data cleaning https://medium.com/codex/making-wordcloud-of-tweets-using-python-ca114b7a4ef4
    # remove html characters
    del_amp = BeautifulSoup(text, 'lxml')
    del_amp_text = del_amp.get_text()
    # remove mentions and hashes
    re_list = ["@[A-Za-z0–9_]+", "#"]
    combined_re = re.compile( '|'.join( re_list) )
    del_link_mentions = re.sub(combined_re, '', del_amp_text)
    # remove emojis
    del_emoji = emoji.get_emoji_regexp().sub("", del_link_mentions)
    # # remove links
    re_links = re.compile(r'(https?:\/\/)?(www\.)?(\w+\.)?(\w+)(\.\w+)(\/\S+)?')
    del_links = re.sub(re_links, "", del_emoji)
    # make lower case
    lower_case = del_links.lower()
    # tokenize
    words = token.tokenize(lower_case)
    # get rid of words below length 2
    result_words = [x for x in words if (len(x) > 2) and (len(x) < 15)]
    # return (" ".join(result_words)).strip()
    return result_words


def get_nouns(words):
    tagged_text = nltk.pos_tag(words)
    nouns_text = []
    for word in tagged_text:
        if word[1] == "NN":
            nouns_text.append(word[0])
    return (" ".join(nouns_text)).strip()

# ----- END WORDCLOUD ----- #



# ----- GENERAL METHODS ----- #

def get_data_from_file(filename):
    with open(filename) as f_in:
        data = json.loads(f_in.read())
        return data


def get_wordcloud(name):
    read_keys(API_PATH)
    api = get_api()
    tweets = get_tweets(api, name)
    master_string = get_master_string(tweets)
    wordcloud = create_wordcloud_object(master_string)
    return wordcloud

# ----- END GENERAL METHODS ----- #


if __name__ == "__main__":
    get_wordcloud("PFokicheva")
