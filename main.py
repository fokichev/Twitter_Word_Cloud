import tweepy

# TODO:
# word cloud with set profile
# simple GUI to enter name + placeholder for word cloud
# connect name entering to word cloud to look up custom profiles
# code in error cases i.e. profile doesn't exist or is private
# OPTIONAL allow user to save word cloud as jpeg


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




if __name__ == "__main__":
    read_keys(API_PATH)
    api = get_api()
    new_tweets = api.user_timeline(screen_name = "DethVeggie", count = 200, tweet_mode="extended")
    print(new_tweets)
