import tweepy

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




if __name__ == "__main__":
    read_keys(API_PATH)
    
