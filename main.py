import tweepy

# TODO:
# normalise data for word cloud
# generate word cloud
# calibrate stop words
    # elim curse words
# simple GUI to enter name + placeholder for word cloud
# connect name entering to word cloud to look up custom profiles
# code in error cases i.e. profile doesn't exist or is private
# OPTIONAL allow user to save word cloud as jpeg
# OPTIONAL allow user to enter additional stop words or add a comma separated doc of stop words they dont want


API_KEY = ""
API_SECRET = ""
# change path to where your API key .txt is stored, with 1st line being public key and 2nd line being private key
API_PATH = "../API_keys.txt"

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



if __name__ == "__main__":
    read_keys(API_PATH)
    api = get_api()
    tweets = get_tweets(api, "PFokicheva")
    print(get_master_string(tweets))
