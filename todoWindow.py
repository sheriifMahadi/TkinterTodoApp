import datetime
import time
import notify2
import pickle
from tkinter import *
from tkinter import ttk
import tkinter.messagebox




class Mainwindow():
    def __init__(self, master):
        self.master = master
        master.title("Simple Todo App")
        self.master.geometry("350x500")
        self.master.columnconfigure(0, weight=1)
        self.master.minsize(350, 500)
        self.master.maxsize(600, 500)

        self.setDate = StringVar()
        self.setTime = StringVar()



    def entry(self):
        """method to handle entry task description"""
        #text label
        self.textLbl = Label(self.master, text="TASK DESCRIPTION",
                             font=("Bold", 12))
        self.textLbl.grid(row=0, column=0, sticky=(N, W), padx=10)

        # text
        self.text = Text(self.master, height=5, bg="white", borderwidth=2)
        self.text.grid(row=1, column=0, sticky=(N, S, E, W), padx=10, pady=10)


        # Frame for text entry
        self.entryFrame = Frame(self.master)
        self.entryFrame.grid(row=2, column=0, sticky=(N, S, E, W), padx=10, pady=10)

        #Date
        self.dateEntry = Entry(self.entryFrame,width=8, bg="Grey", textvariable=self.setDate)
        self.dateEntry.grid(row=0, column=1, padx=5, pady=5)
        self.dateEntry.insert(0, datetime.datetime.now().strftime("%d/%m/%y"))


        self.timeEntry = Entry(self.entryFrame, width=5, bg="Grey", textvariable=self.setTime)
        self.timeEntry.grid(row=0, column=2, padx=5, pady=5)
        self.timeEntry.insert(0, time.strftime("%H:%M"))



        self.timeBox = ttk.Combobox(self.entryFrame, width=3, state="readonly", values=('AM', 'PM'))
        self.timeBox.current(0)
        self.timeBox.grid(row=0, column=3, padx=5, pady=5)

        self.notifier = Checkbutton(self.entryFrame, text="Notify me", bg="Grey")
        self.notifier.grid(row=0, column=0, sticky=(N, W), padx=5, pady=5)

        self.entryFrame.rowconfigure(0, weight=1)
        self.entryFrame.columnconfigure(0, weight=1)

    def create_listBox(self):
        """A list box to display tasks"""
        self.listBoxFrame = Frame(self.master)
        self.listBoxFrame.grid(row=3, column=0, sticky=(N, S, E, W), padx=5, pady=5)
        self.tasks_listBox = Listbox(self.listBoxFrame, height=10, width=100, bg="white")
        self.tasks_listBox.grid(row=0, column=0, sticky=(N, S, E, W), padx=10, pady=10)

        # create a scroll bar
        self.tasksScrollBar = Scrollbar(self.listBoxFrame)
        self.tasksScrollBar.grid(row=0, column=1, sticky=(N, S))

        self.tasks_listBox.config(yscrollcommand=self.tasksScrollBar.set)
        self.tasksScrollBar.config(command=self.tasks_listBox.yview)

        # create button
        self.addButton = Button(self.listBoxFrame, text='add \ntask', width=5, bg="green", command=self.add_task)
        self.addButton.grid(row=3, column=0, sticky=(E, S), padx=10, pady=10)

        self.deleteButton = Button(self.listBoxFrame, text='delete \ntask', width=5, bg="red", command=self.delete_task)
        self.deleteButton.grid(row=3, column=0, sticky=(W, S), padx=10, pady=10)

        self.listBoxFrame.rowconfigure(0, weight=1)
        self.listBoxFrame.columnconfigure(0, weight=1)

    # adding tasks
    def add_task(self):
        self.add = self.text.get(1.0, END).rstrip("\n")
        if self.add != "":
            self.tasks_listBox.insert(END, self.add)
            self.text.delete(1.0, END)

            # save the task
            self.tasks = self.tasks_listBox.get(0, self.tasks_listBox.size())
            pickle.dump(self.tasks, open("toDo.dat", "wb"))

        else:
            tkinter.messagebox.showwarning(title="Warning", message="Task not entered.")
            tkinter.tcl

    def load_tasks(self):
        try:
            self.open = pickle.load(open("toDo.dat", "rb"))
            self.tasks_listBox.delete(0, END)
            for self.opened in self.open:
                self.tasks_listBox.insert(END, self.opened)
        except:
            FileNotFoundError

    # deleting task
    def delete_task(self):
        try:
            self.delete = self.tasks_listBox.curselection()[0]
            self.tasks_listBox.delete(self.delete)

            # deleting from file
            self.pickleString = list(self.open)
            print(self.pickleString)
            for self.item in self.pickleString:
                self.pickleString.pop(self.delete)
                pickle.dump(self.pickleString, open("toDo.dat", "wb"))
        except:
            tkinter.messagebox.showwarning(title="Warning!", message="Task not selected")

    # activate notification
    def notify(self):
        self.currentTime = self.setTime.get()
        self.currentDate = self.setDate.get()
        if self.currentTime == time.strftime("%H:%M"):
            if self.currentDate == datetime.datetime.now().strftime("%d/%m/%y"):
                notify2.init("Task due for completion")
                n = notify2.Notification("Animepahe")
                n.set_urgency(notify2.URGENCY_NORMAL)
                n.set_timeout(10000)
                n.update(n.update("Update"))
                



window = Tk()
app = Mainwindow(window)
app.entry()
app.create_listBox()
app.load_tasks()
app.notify()
window.mainloop()

