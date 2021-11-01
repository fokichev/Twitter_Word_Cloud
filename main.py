import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from tweet_processing import *
# tutorial for matplotlib graph in tkinter https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# multi threading using https://stackoverflow.com/questions/15323574/how-to-connect-a-progress-bar-to-a-function/15323917#15323917
import threading
import queue
import time

# TODO:
# add area for app feedback to user
# code in error cases i.e. profile doesn't exist or is private
# make it so app doesn't freeze while processing
# add some form of progress report to user while cloud is generating
# OPTIONAL allow user to save word cloud as jpeg
# OPTIONAL allow user to enter additional stop words or add a comma separated doc of stop words they dont want


class Root(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("700x600")
        self.title("Word Cloud :)")
        # threading
        self.queue = queue.Queue()

        self.entry_name = tk.Entry(self)
        self.entry_name.grid(row = 1, column = 1)

        # button_submit = tk.Button(self, text = "Submit", command = lambda: self.show_wordcloud(entry_name.get()))
        self.button_submit = tk.Button(self, text = "Submit", command = lambda: self.spawnthread())
        self.button_submit.grid(row = 2, column = 1)

        self.listbox = tk.Listbox(self, width = 30, height = 5)
        self.listbox.grid(row = 3, column = 1)

        self.progressbar = ttk.Progressbar(self, orient = "horizontal", length = 300, mode = "determinate")
        self.progressbar.grid(row = 4, column = 1)


    def spawnthread(self):
        self.button_submit.config(state = "disabled")
        self.thread = ThreadedClient(self.queue)
        self.thread.start()
        self.periodiccall()


    def periodiccall(self):
        self.checkqueue()
        if self.thread.is_alive():
            self.after(100, self.periodiccall)
        else:
            self.button_submit.config(state="active")


    def checkqueue(self):
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                self.listbox.insert('end', msg)
                self.progressbar.step(25)
            except Queue.Empty:
                pass


    def show_wordcloud(self, name):
        wordcloud = get_wordcloud(name)
        fig = plt.figure(figsize=(6,4))
        im = plt.imshow(wordcloud, interpolation="bilinear")
        ax = plt.axis("off")
        plt.tight_layout(pad=0.5)
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row = 10, column = 1) #, columnspan = 7, rowspan = 100, padx = x + 20, pady = y)


class ThreadedClient(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        name = "PFokicheva" # for now
        read_keys(API_PATH)
        api = get_api()
        self.queue.put("Downloading Tweets...")
        tweets = get_tweets(api, name)
        print("test")
        self.queue.put("Generating Word Cloud...")
        master_string = get_master_string(tweets)
        wordcloud = create_wordcloud_object(master_string)
        self.queue.put("Done!")
        # return wordcloud


def main():
    def on_closing():
       plt.close("all")
       root.destroy()
    root = Root()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
