from tkinter import *

class AutoScrollListBox_demo:
    def __init__(self, master):
        frame = Frame(master, width=500, height=400, bd=1)
        frame.pack()

        self.listbox_log = Listbox(frame, height=4)
        self.scrollbar_log = Scrollbar(frame)

        self.scrollbar_log.pack(side=RIGHT, fill=Y)
        self.listbox_log.pack(side=LEFT,fill=Y)

        self.listbox_log.configure(yscrollcommand = self.scrollbar_log.set)
        self.scrollbar_log.configure(command = self.listbox_log.yview)

        b = Button(text="Add", command=self.onAdd)
        b.pack()

        #Just to show unique items in the list
        self.item_num = 0

    def onAdd(self):
        self.listbox_log.insert(END, "test %s" %(str(self.item_num)))       #Insert a new item at the end of the list

        self.listbox_log.select_clear(self.listbox_log.size() - 2)   #Clear the current selected item
        self.listbox_log.select_set(END)                             #Select the new item
        self.listbox_log.yview(END)                                  #Set the scrollbar to the end of the listbox

        self.item_num += 1


root = Tk()
all = AutoScrollListBox_demo(root)
root.title('AutoScroll ListBox Demo')
root.mainloop()
