from tkinter import *
import json
from pygame import mixer
from shutil import copyfile
import os

ERR = "media/err.wav"
PATH = "data/lists/"
ILIST = PATH + "itemlist.json"
ICOUNT = PATH + "itemcount.json"
ITYPE = PATH + "itemtype.json"

def errsnd():
    mixer.init()
    mixer.music.load(ERR)
    mixer.music.play()

class importWindow(object):
    def __init__(self, master):
        OPTIONS = []
        for d in os.walk("data"):
            OPTIONS.append(d[0])
        OPTIONS.pop(0)
        listlist = []
        for d in OPTIONS:
            y = d.replace('data/','')
            listlist.append(y)
        top=self.top=Toplevel(master)
        self.l=Label(top, text="Import")
        self.l.pack()
        self.variable = StringVar(top)
        self.variable.set(listlist[0])
        self.w = OptionMenu(top, self.variable, *listlist)
        self.w.pack()
        def imp(test=None):
            self.importf()

    def cleanup(self):
        self.top.destroy()

    def importf(self):
        copyfile()
        self.cleanup()

class exportWindow(object):
    #TODO make "Export" button in main window open this window, add binding for enter to run export function
    def __init__(self, master):
        top=self.top=Toplevel(master)
        self.l=Label(top, text="Export")
        self.l.pack()
        self.e=Entry(top)
        self.e.pack()
        def exp(test=None):
            self.export()
        self.e.bind('<Return>', exp)


    def cleanup(self):
        self.top.destroy()

    def export(self):
        if self.e.get() != "":
            os.makedirs("data/" + self.e.get())
            copyfile(ILIST, "data/" + self.e.get() + "/itemlist.json")
            copyfile(ICOUNT, "data/" + self.e.get() + "/itemcount.json")
            copyfile(ITYPE, "data/" + self.e.get() + "/itemtype.json")
            self.cleanup()
        else:
            return

class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def updatejson(self, data, list):
        with open(data, 'w') as outfile:
            json.dump(list, outfile)

    def init_window(self):
        invlist = []

        def yview(*args):
            itemlist.yview(*args)
            itemcount.yview(*args)
            itemtype.yview(*args)

        def yscroll1(*args):
            if itemlist.yview() != itemcount.yview():
                itemcount.yview_moveto(args[0])
            if itemlist.yview() != itemtype.yview():
                itemtype.yview_moveto(args[0])
            ilscrollbar.set(*args)

        def yscroll2(*args):
            if itemcount.yview() != itemlist.yview():
                itemlist.yview_moveto(args[0])
            if itemcount.yview() != itemtype.yview():
                itemtype.yview_moveto(args[0])
            ilscrollbar.set(*args)

        def yscroll3(*args):
            if itemtype.yview() != itemlist.yview():
                itemlist.yview_moveto(args[0])
            if itemtype.yview() != itemcount.yview():
                itemcount.yview_moveto(args[0])
            ilscrollbar.set(*args)

        def status(text, time: int=None):
            if time != None:
                statusbox.config(text=text)
                time = time*1000
                statusbox.after(time, resetstatus)
            else:
                statusbox.config(text=text)
                statusbox.after(5000, resetstatus)

        def resetstatus():
            statusbox.config(text="")

        def sort():
            print("DEBUG")
            sortlst = []
            n = 0
            #TODO create alphabetical sorting function
            for i in itemlist.get(0, itemlist.size()):
                sortlst.append((i, itemcount.get(n), itemtype.get(n)))
                n = n + 1

            sortedlist = sorted(sortlst)

            items = []
            count = []
            type = []

            for i in sortedlist:
                items.append(i[0])
                count.append(i[1])
                type.append(i[2])

            self.updatejson(ILIST, items)
            self.updatejson(ICOUNT, count)
            self.updatejson(ITYPE, type)

            updatelist(ILIST, itemlist)
            updatelist(ICOUNT, itemcount)
            updatelist(ITYPE, itemtype)

            print(items)
            print(count)
            print(type)


        def saveall():
            items = []
            count = []
            type = []
            for i in itemlist.get(0, itemlist.size()):
                items.append(i)
            for i in itemcount.get(0, itemcount.size()):
                count.append(i)
            for i in itemtype.get(0, itemtype.size()):
                type.append(i)
            self.updatejson(ILIST, items)
            self.updatejson(ICOUNT, count)
            self.updatejson(ITYPE, type)
            status("Saved...", 5)

        def floaterror():
            errsnd()
            status("Invalid Item Count", 5)

        def emptyerror():
            errsnd()
            status("Empty entry field.")

        def selectionerror():
            errsnd()
            status("No value selected.")

        def duplicate_error():
            errsnd()
            status("Item already in list")

        def printlist():
            print(itemlist.get(0, 1000*1000))

        def fillitemcount():
            yay = 0
            for item in itemlist.get(0, itemlist.size()):
                if itemcount.size() < itemlist.size():
                    itemcount.insert(END, yay)
                    yay = yay + 1
                elif itemcount.size() > itemlist.size():
                    itemcount.delete(END)
                else:
                    return

        def fillitemtype():
            for item in itemlist.get(0, itemlist.size()):
                if itemtype.size() < itemlist.size():
                    itemtype.insert(END, "N/A")
                elif itemtype.size() > itemlist.size():
                    itemcount.delete(END)
                else:
                    return

        def checkjson(listfile):
            if check_folders(test=True) and check_files(test=True):
                with open(listfile, 'r') as f:
                    array = json.load(f)
                    invlist = array
                return invlist

        def updatelist(datafile, list):
            list.delete(0, list.size())
            for i in checkjson(datafile):
                list.insert(END, i)

        def getid(list, active=None):
            id = 0
            if active == True:
                for item in list.get(0, list.size()):
                    if item == list.get(ACTIVE):
                        return id
                    else:
                        id = id + 1
            elif active != True:
                for item in list.get(0, list.size()):
                    if item == list.get(list.curselection()):
                        return id
                    else:
                        id = id + 1

        def tprint(event):
            if itementry.get() == "":
                emptyerror()
                return
            for item in itemlist.get(0, itemlist.size()):
                if itementry.get().lower() == item.lower():
                    duplicate_error()
                    itementry.delete(0, 10000)
                    return
            itemlist.insert(END, itementry.get())
            invlist = itemlist.get(0, 1000*1000)
            itementry.delete(0, 1000)
            self.updatejson(ILIST, invlist)
            fillitemcount()
            fillitemtype()
            print(invlist)

        def tprint2(event):
            if itementry.get() != None:
                if itemcount.curselection() == ():
                    selectionerror()
                    return
                try:
                    float(countentry.get())
                except:
                    floaterror()
                    countentry.delete(0, 1000)
                    return
                lid = getid(itemcount)
                itemcount.delete(lid)
                itemcount.insert(lid, countentry.get())
                for i in itemcount.get(0, itemcount.size()):
                    invlist.append(float(i))
                self.updatejson(ICOUNT, invlist)
                countentry.delete(0, 1000)
            else:
                emptyerror()
                itementry.delete(0, 1000)
                print("1")
                return

        def tprint3(event):
            if typeentry.get() == "":
                emptyerror()
                return
            if itemtype.curselection() == ():
                selectionerror()
                return
            lid = itemtype.curselection()
            itemtype.delete(lid)
            itemtype.insert(lid, typeentry.get())
            invlist = itemtype.get(0, itemtype.size())
            self.updatejson(ITYPE, invlist)
            typeentry.delete(0, 1000)

        def selectid(id, list):
            list.select_clear(0, list.size())
            list.selection_set(id)

        def delete(event=None):
            if itemcount.curselection() != ():
                print("test")
                lid = getid(itemcount)
                itemcount.delete(lid)
                itemcount.insert(lid, "0")
            elif itemtype.curselection() != ():
                lid = itemtype.curselection()
                itemtype.delete(lid)
                itemtype.insert(lid, 'N/A')
            elif itemlist.curselection() != ():
                lid = getid(itemlist)
                itemcount.delete(lid)
                itemtype.delete(lid)
                itemlist.delete(itemlist.curselection())
                saveall()
            else:
                lid = getid(itemlist, True)
                itemcount.delete(lid)
                itemtype.delete(lid)
                itemlist.delete(lid)
                saveall()

        #set the title of the window
        self.master.title("Sheets")

        #allow the widget to fill the inter root window
        self.pack(fill=X)

        #create menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)

        #create file object
        file = Menu(menu)

        def startexport():
            exportWindow(master=self.master)

        def startimport():
            importWindow(master=self.master)

        #adds a command to the menu option, calling it to exit
        #and the command it runs on event is client_exit
        file.add_command(label="Exit", command=self.client_exit)
        file.add_command(label="Export", command=startexport)
        file.add_command(label="Import", command=startimport)
        file.add_command(label="Save", command=saveall)

        #add "File" to our menu
        menu.add_cascade(label="File", menu=file)

        #Create edit object
        edit = Menu(menu)

        edit.add_command(label="Sort Alphabetically", command=sort)

        menu.add_cascade(label="Edit", menu=edit)

        statusbox = Button(root)
        statusbox.config(state=DISABLED, relief=FLAT, text="", disabledforeground="black")

        statusbox.pack(side=TOP, anchor=W)

        entrybox = Entry(root)

        itementry = Entry(entrybox)
        countentry = Entry(entrybox)
        typeentry = Entry(entrybox)

        entrybox.pack(side=TOP, anchor=W, pady=10)

        itementry.bind("<Return>", tprint)
        itementry.pack(side=LEFT, anchor=W)
        typeentry.bind("<Return>", tprint3)
        typeentry.pack(side=RIGHT, anchor=W)
        countentry.bind("<Return>", tprint2)
        countentry.pack(side=RIGHT, anchor=W)
        res = Label(root)
        box = Listbox(root)
        box.pack(side=TOP, fill=Y, anchor=W, expand=YES)
        itemlist = Listbox(box)
        itemcount = Listbox(box)
        itemtype = Listbox(box)
        dummybox = Listbox(box)

        ilscrollbar = Scrollbar(dummybox)
        ilscrollbar.config(command=yview)
        ilscrollbar.pack(side=LEFT, fill=Y)

        dummybox.pack(side=RIGHT, fill=Y, anchor=W, expand=YES)
        itemlist.config(yscrollcommand=yscroll1)
        itemlist.pack(side=LEFT, fill=Y, anchor=W, expand=YES)
        itemtype.config(exportselection=False, yscrollcommand=yscroll3)
        itemtype.pack(side=RIGHT, fill=Y, anchor=W, expand=YES)
        itemcount.config(exportselection=False, yscrollcommand=yscroll2)
        itemcount.pack(side=RIGHT, fill=Y, anchor=W, expand=YES)
        for i in checkjson(ILIST):
            itemlist.insert(END, i)
        for i in checkjson(ICOUNT):
            itemcount.insert(END, i)
        for i in checkjson(ITYPE):
            itemtype.insert(END, i)

        fillitemcount()
        fillitemtype()


        def cleariselect(test=None):
            itemlist.selection_clear(0, itemlist.size())
            itemlist.select_clear(ACTIVE)

        res.pack()
        itemlist.bind("<Escape>", cleariselect)
        root.bind("<Delete>", delete)




    def client_exit(self):
        exit()


def check_folders(test=None):
    if not os.path.exists(PATH):
        print("Creating empty data/invlists folder...")
        os.makedirs(PATH)
        print("Done.")
        if test is not None:
            return True
    if test is not None:
        return True

def check_files(test = None):
    if not os.path.isfile(ILIST):
        with open(ILIST, 'w') as outfile:
            json.dump([], outfile)
        if test is not None:
            return True
    if not os.path.isfile(ICOUNT):
        with open(ICOUNT, 'w') as outfile:
            json.dump([], outfile)
        if test is not None:
            return True
    if not os.path.isfile(ITYPE):
        with open(ITYPE, 'w') as outfile:
            json.dump([], outfile)
    if test is not None:
        return True


check_folders()
check_files()

root = Tk()

#size of the window
root.geometry("400x300")

app = Window(root)

root.mainloop()