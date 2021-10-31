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

        wordcloud = get_wordcloud("harpertonik")
        fig = plt.figure(figsize=(7,5))
        im = plt.imshow(wordcloud, interpolation="bilinear")
        ax = plt.axis("off")
        plt.tight_layout(pad=0.5)
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row = 1, column = 1) #, columnspan = 7, rowspan = 100, padx = x + 20, pady = y)





def main():
    def on_closing():
       plt.close("all")
       root.destroy()
    root = Root()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
