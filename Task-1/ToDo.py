from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
import os


class ToDo:
    def __init__(self, master, filename):
        self.filename = filename
        
        # Keep track of the number of created checkbuttons to ensure 
        # a unique ID in the dictionary 
        self.nrOfCheckbuttons = 0
        # A dictionary to store the checkbuttons
        self.containerCheckbuttons = {}
        self.master = master
        # If the user press Enter, it will add the item
        self.master.bind('<Return>', lambda e: self.addItem(self.entryItem.get()))

        # Setting a title, background and size to the master window
        self.master.title('ToDo')
        self.master.configure(background='lavender')
        self.master.geometry('800x800')
        self.master.resizable(False, False)

        # Configures the style (background) to the diffrent widgets used in the program 
        self.style = ttk.Style()
        self.style.configure('TFrame', background='lavender')
        self.style.configure('TCanvas', background='lavender')
        self.style.configure('TLabel', background='lavender')
        self.style.configure('TButton', background='lavender')
        self.style.configure('TCheckbutton', background='lavender')

        # Creating a frame for the header
        self.frameHeader = ttk.Frame(self.master)
        #self.frameHeader.configure(width=800, height=50, padx=15)
        self.frameHeader.pack()

        # Configure the title
        self.title = ttk.Label(self.frameHeader, text='ToDo-List', font=('Times New Roman', 24, 'bold'))
        self.title.grid(row=0, column=0, rowspan=4, pady=30)
        
        # Configure a frame for the buttons and the Entry-field
        self.frameManage = ttk.Frame(self.master)#, borderwidth=2, relief=RIDGE)
        self.frameManage.pack(pady=5)
        
        ttk.Label(self.frameManage, text='Describe new item:', 
                  font=('Times New Roman', 22)).grid(row=0, column=0, sticky=SW)
        self.entryItem = ttk.Entry(self.frameManage, width=50, font=('Times New Roman', 14))
        self.entryItem.grid(row=1, column=0, padx=5)

        ttk.Button(self.frameManage, text='Add new item', 
                   command=lambda: self.addItem(self.entryItem.get())).grid(row=1, column=3, padx=5)
        ttk.Button(self.frameManage, text='Delete completed items', 
                   command=self.deleteFinished).grid(row=1, column=4, padx=5)
        ttk.Button(self.frameManage, text='Delete All', 
                   command=self.deletaAll).grid(row=1, column=5, padx=5)


        self.canvasContent = Canvas(self.master, width=300, height=300, 
                                    background='lavender')
        self.canvasContent.pack(side=LEFT, anchor=W, padx=15, expand=True, fill=BOTH)

        # Menu bar
        self.master.option_add('*tearOff', False)
        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)
        self.file = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.file, label='File')
        self.file.add_command(label='New', command=self.newWindow)
        self.file.add_command(label='Save', command=self.saveToFile)
        self.file.add_command(label='Open...', command=self.askForDirectory)
        self.file.add_command(label='Rename', command=self.changeTitle)

        # If this is a window opened for a file, load in the specified file
        if self.filename != '':
            self.openFile()
        
    # The addItem() function will first check if the entry field is empty or contains an item that already exists
    # If so, an informational pop up will appear with this information.
    # Otherwisem a new checkbutton will be created with the specified item.
    # This function will be executed either by clicking the button 'Add new item' or by pressing Enter
    def addItem(self, item):
        if self.entryItem.get() == "":
            messagebox.showinfo('Missing input' ,"You have to insert an item!")
            return
        for entry in self.containerCheckbuttons.values():
            if item.lower() == entry.cget('text').lower():
                messagebox.showinfo('Already exists' ,"The item already exists!")
                self.entryItem.delete(0, END)  
                return
        self.checkbutton = ttk.Checkbutton(self.canvasContent, text=item, onvalue=1, offvalue=0)
        self.containerCheckbuttons[self.nrOfCheckbuttons] = self.checkbutton
        self.nrOfCheckbuttons = self.nrOfCheckbuttons + 1
        # This will make sure that the checkbuttons are not selected when created
        self.checkbutton.state(['!alternate'])
        self.checkbutton.pack(side=TOP, anchor=W, padx=15, pady=5)
        self.entryItem.delete(0, END)

    # Deletes att items that is selected (marked as finished).
    # This function is executed when clicking the button 'Delete completed items'.
    def deleteFinished(self):
        deletedItems = []
        for key, entry in self.containerCheckbuttons.items():
            if entry.state():
                entry.destroy()
                deletedItems.append(key)
        for item in deletedItems:
            if item in self.containerCheckbuttons:
                self.containerCheckbuttons.pop(item)

    # This function will delete all checkbuttons.
    # This function is executed when pressing the button 'Delete All'
    def deletaAll(self):
        if len(self.containerCheckbuttons) == 0:
            messagebox.showinfo('No entries' ,"There are no entries to delete")
        for entry in self.containerCheckbuttons.values():
            entry.destroy()
        self.containerCheckbuttons.clear()

    # This function will change the title.
    # Execited when navigating 'File -> Rename'
    def changeTitle(self):
        userInput = simpledialog.askstring(title='Enter new title', prompt='Enter the desired title', parent=self.master)
        self.title.configure(text=userInput)
        self.master.title(userInput)
    
    # Saves the information about the checkbuttons to a file 
    def saveToFile(self):
        
        #path = self.askForDirectory(0)
        title = filedialog.askdirectory() + '/' + self.title.cget('text') + ".txt"
        outputFile = open(title, 'w')
        for entry in self.containerCheckbuttons.values():
            if entry.state():
                outputFile.write(entry.cget('text') + '\t' + 'True' + '\n')
            else:
                outputFile.write(entry.cget('text') + '\t' + 'False' + '\n')
        outputFile.close()

    def askForDirectory(self):
        self.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select a file', 
                                                          filetypes=(('text files','*.txt'),))
        self.newWindow()

    # When creating a new window, if using newWindow=Toplevel()
    # this newWindow will close whenever the fist created window is closed.
    # For an new independent window, instead use independetNewWindow=Tk()
    def newWindow(self):
        newWindow = Tk()
        newToDo = ToDo(newWindow, self.filename)
        newWindow.mainloop()
    
    # Opens the specified file and recreating the checkbuttons
    def openFile(self):
        newTitle = self.filename.split('/')[-1].split('.', 1)[0]
        self.title.configure(text=newTitle)
        self.master.title(newTitle)
        inputFile = open(self.filename, 'r')
        content = []
        for line in inputFile:
            content = line.split('\t')
            self.checkbutton = ttk.Checkbutton(self.canvasContent, text=content[0], onvalue=1, offvalue=0)
            if content[1][:-1] == 'False':
                self.checkbutton.state(['!alternate'])
            self.checkbutton.pack(side=TOP, anchor=W, padx=15, pady=5)
            self.containerCheckbuttons[self.nrOfCheckbuttons] = self.checkbutton
            self.nrOfCheckbuttons = self.nrOfCheckbuttons + 1
            





def main():
    root = Tk()
    toDo = ToDo(root, '')
    root.mainloop()

if __name__ == "__main__": main()