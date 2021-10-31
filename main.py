import tkinter as tk
from PIL import ImageTk, Image
from tweet_processing import *
# tutorial for matplotlib graph in tkinter https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class Root(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("700x600")
        self.title("Word Cloud :)")


        entry_name = tk.Entry(self)
        entry_name.grid(row = 1, column = 1)

        button_submit = tk.Button(self, text = "Submit", command = lambda: self.show_wordcloud(entry_name.get()))
        button_submit.grid(row = 2, column = 1)


    def show_wordcloud(self, name):
        wordcloud = get_wordcloud(name)
        fig = plt.figure(figsize=(7,5))
        im = plt.imshow(wordcloud, interpolation="bilinear")
        ax = plt.axis("off")
        plt.tight_layout(pad=0.5)
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row = 3, column = 1) #, columnspan = 7, rowspan = 100, padx = x + 20, pady = y)





def main():
    def on_closing():
       plt.close("all")
       root.destroy()
    root = Root()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
