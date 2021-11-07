import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
from tweet_processing import *
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from wordcloud import WordCloud
import threading
import queue
import time


# TUTORIALS
# tutorial for matplotlib graph in tkinter https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/
# wordcloud with wine example https://www.datacamp.com/community/tutorials/wordcloud-python
# multi threading using https://stackoverflow.com/questions/15323574/how-to-connect-a-progress-bar-to-a-function/15323917#15323917
# auto scroll of listbox using https://stackoverflow.com/questions/3699104/how-to-add-autoscroll-on-insert-in-tkinter-listbox

# TODO:
# OPTIONAL allow user to enter additional stop words or add a comma separated doc of stop words they dont want
# make demo on GitHub with screenshots
# create .exe version


x = 10
y = 2


class Root(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("900x400")
        self.title("Word Cloud :) - by Polina Fokicheva")
        # threading
        self.queue = queue.Queue()

        self.entry_name = tk.Entry(self)
        self.entry_name.grid(row = 1, column = 1, padx = x, pady = y)

        self.button_submit = tk.Button(self, text = "Submit", command = lambda: self.spawn_thread(self.entry_name.get()))
        self.button_submit.grid(row = 1, column = 2, padx = x, pady = y)

        self.paste_button = tk.Button(self, text = "Paste from Clipboard", command = lambda: self.paste_to_entry())
        self.paste_button.grid(row = 2, column = 1, columnspan = 1, padx = x, pady = y)

        self.progressbar = ttk.Progressbar(self, orient = "horizontal", length = 200, mode = "determinate")
        self.progressbar.grid(row = 3, column = 1, columnspan = 2, padx = x, pady = y)

        self.frame = tk.Frame(self)
        self.frame.grid(row = 4, column = 1, columnspan = 2, padx = x, pady = y)

        self.listbox = tk.Listbox(self.frame, width = 35, height = 15)
        self.scrollbar = tk.Scrollbar(self.frame)
        # self.listbox.grid(row = 4, column = 1, columnspan = 2, padx = x, pady = y)

        self.listbox.pack(side = tk.LEFT, fill = tk.Y)
        self.scrollbar.pack(side = tk.RIGHT, fill = tk.Y)

        self.listbox.configure(yscrollcommand = self.scrollbar.set)
        self.scrollbar.configure(command = self.listbox.yview)

        self.save_button = tk.Button(self, text = "Save Image", command = lambda: self.save_image())
        self.save_button.grid(row = 1, column = 3, padx = x, pady = y)
        self.save_button.grid_remove()


    def spawn_thread(self, name):
        self.name = name
        self.button_submit.config(state = "disabled")
        self.save_button.config(state = "disabled")
        self.thread = ThreadedClient(self.queue, self.name)
        self.thread.start()
        self.periodic_call()


    def periodic_call(self):
        self.check_queue()
        if self.thread.is_alive():
            self.after(100, self.periodic_call)
        else:
            self.button_submit.config(state="active")
            self.save_button.config(state="active")


    def check_queue(self):
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                if isinstance(msg, WordCloud):
                    self.progressbar.step(0.1)
                    self.wordcloud = msg
                    self.show_wordcloud(msg)
                else:
                    self.listbox.insert('end', msg[0])
                    # Clear the current selected item
                    self.listbox.select_clear(self.listbox.size() - 2)
                    # Select the new item
                    self.listbox.select_set("end")
                    # Set the scrollbar to the end of the listbox
                    self.listbox.yview("end")
                    self.progressbar.step(msg[1])
            except:
                pass


    def show_wordcloud(self, wordcloud):
        self.fig = plt.figure(figsize=(5,3))
        self.im = plt.imshow(wordcloud, interpolation="bilinear")
        self.ax = plt.axis("off")
        plt.tight_layout(pad=0.5)
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row = 2, column = 3, rowspan = 100, padx = x, pady = y) #, columnspan = 7, rowspan = 100, padx = x + 20, pady = y)
        self.save_button.grid()


    def paste_to_entry(self):
        # get text from clipboard
        # text = "123"
        copy = tk.Tk()
        copy.withdraw()
        text = copy.clipboard_get()
        # set entry to text value
        self.entry_name.delete(0, "end")
        self.entry_name.insert(0, text)


    def save_image(self):
        file_opt = options = {}
        options['filetypes'] = [('PNG file', '.png')]
        filename = self.name + "_wordcloud.png"
        options['initialfile'] = filename
        savefile = filedialog.asksaveasfilename(defaultextension=".png", **file_opt)
        # print(savefile)
        self.wordcloud.to_file(savefile)



class ThreadedClient(threading.Thread):

    def __init__(self, queue, name):
        threading.Thread.__init__(self)
        self.queue = queue
        self.name = name

    def run(self):
        # name = "PFokicheva" # for now
        read_keys(API_PATH)
        api = get_api()
        # self.queue.put(["Downloading Tweets...", 10])
        tweets = self.get_tweets(api)
        if tweets:
            self.queue.put(["Generating Word Cloud...", 7])
            master_string = get_master_string(tweets)
            wordcloud = create_wordcloud_object(master_string)
            self.queue.put(["Done!", 3])
            self.queue.put(wordcloud)
        else:
            self.queue.put(["Error getting user tweets.", 10])

    def get_tweets(self, api):
        i = 0
        try:
            print(f"Getting tweets for {self.name}")
            self.queue.put([f"Getting tweets for {self.name}", 10])
            user_tweets = []
            # make initial request for most recent tweets (200 is the maximum allowed count)
            new_tweets = api.user_timeline(screen_name = self.name, count = 200, tweet_mode="extended")
            new_tweets = [x._json for x in new_tweets]
            # save most recent tweets
            user_tweets.extend(new_tweets)
            oldest = user_tweets[-1]["id"] - 1
            # keep grabbing tweets until there are no tweets left to grab
            while len(new_tweets) > 0:
                # all subsiquent requests use the max_id param to prevent duplicates
                new_tweets = api.user_timeline(screen_name = self.name ,count = 200, max_id = oldest, tweet_mode="extended")
                new_tweets = [x._json for x in new_tweets]
                # save most recent tweets
                user_tweets.extend(new_tweets)
                #update the id of the oldest tweet less one
                oldest = user_tweets[-1]["id"] - 1
                print(f"...{len(user_tweets)} tweets downloaded so far")
                self.queue.put([f"...{len(user_tweets)} tweets downloaded so far", 4])
                i = i + 4
            # print(json.dumps(user_tweets, indent=4))
            self.queue.put([f"...{len(user_tweets)} tweets downloaded so far", (80 - i)])
            return user_tweets
        except Exception as e:
            print("Error getting user tweets.")
            self.queue.put(["Error getting user tweets.", (80 - i)])
            print(e)
            return {}



def main():
    def on_closing():
       plt.close("all")
       root.destroy()
    root = Root()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
