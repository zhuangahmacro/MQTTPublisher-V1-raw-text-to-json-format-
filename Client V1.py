import pickle, time
from tkinter import *
import tkinter.messagebox as tkMessageBox
import socket
from tkinter import messagebox, ttk
import json
from collections import OrderedDict
import psycopg2
from PIL import ImageTk, Image
from genson import SchemaBuilder

file_data = OrderedDict()

root = Tk()
root.title("Foghorn Publisher")
width = 1000
height = 680
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
root.minsize(500, 300)
root.maxsize(500, 300)
p1 = ImageTk.PhotoImage(file = 'logo.png')

root.iconphoto(False, p1)

root.geometry("%dx%d+%d+%d" % (width, height, x, y))




# =======================================DB CONNECTION=====================================
con = psycopg2.connect(
    host= "localhost",
    database="Foghorn",
    user="postgres",
    password="584584"
)
global list_database,cursor
cursor = con.cursor()
cursor.execute("SELECT jsonprofilename from json")

list_database = cursor.fetchall()

# =======================================VARIABLES=====================================
global ipaddress
global your_port
ipaddress = StringVar()
your_port = StringVar()

# =======================================Declare ROOT left/right=====================================
global left
global right
left = Frame(root)
right = Frame(root)

left.pack(side="left", fill="y")
right.pack(side="right", fill="both", expand=True)

# =======================================Declare frames=====================================
global button_frame
button_frame = Frame(right)
button_frame.pack(side="top", fill="x")
button_frame.grid_columnconfigure((0, 1, 2), weight=1)


# ConnectINTERFACE
def ConnectForm():
    global connectFrame, lbl_result1
    connectFrame = Frame(right)
    connectFrame.pack(fill="both", expand=True)


    lbl_ipaddress = Label(connectFrame, text="IP Address :", font=('arial', 11), bd=11)
    lbl_ipaddress.place(x=90, y=50)
    lbl_port = Label(connectFrame, text="Port  :", font=('arial', 11), bd=11)
    lbl_port.place(x=130, y=90)
    lbl_result1 = Label(connectFrame, text="", font=('arial', 18))
    lbl_result1.place(x=90,y=400)
    entry_ip = ttk.Entry(connectFrame, font=('arial', 11), textvariable=ipaddress, width=18)
    entry_ip.place(x=190,y=59)
    v = StringVar(root, value='9999')
    entry_port = Entry(connectFrame, font=('arial', 11), textvariable=v, state=DISABLED, width=18, show="*")
    entry_port.place(x=190,y=100)
    btn_connect = Button(connectFrame, text="Connect", font=('arial', 11), width=10, command=Connect_to_server)
    btn_connect.place(x=210,y=140)

    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ConnectToServerMethod
def Connect_to_server():
    global target_ip
    target_ip = ipaddress.get()
    target_port = 9999
    try:
        s.connect((target_ip, int(target_port)))
        ToggleToMainMenu()
    except:
        tkMessageBox.showinfo("Error", "Unable connect to the server. please make sure the server is up and running.", icon="error")

def ToggleToMainMenu(event=None):
    root.minsize(1200, 680)
    root.maxsize(1200, 680)
    connectFrame.destroy()
    MainMenuForm()
#=======================Main Function Menu================
def MainMenuForm():
    global listbox, rb1, rb2, rb3
    list_label = Label(left, text=target_ip, fg="green",  font=("Calibri", 11, "bold"))
    listbox = Listbox(left)
    list_label.pack(side="top", fill="x")
    if not listbox.winfo_ismapped(): listbox.pack(side="bottom", fill="both", expand=True)
    ListboxContentrefresh()
    dropdownvalue()

    refresh_button = Button(root, text="refresh", command=refresh)
    refresh_button.place(x=130, y=17, width=50, height=22)

    var = StringVar(root)
    var.set(None)
    rb1 = Radiobutton(button_frame, text='JSON', bg="DarkOrange1", selectcolor="DarkOrange2", fg="white", value='jsonpage', font=("Calibri", 11, "bold"), indicatoron=0, width=10,
                      variable=var,
                      command=lambda: start(var.get()))
    rb2 = Radiobutton(button_frame, text='XML', bg="DarkOrange1", selectcolor="DarkOrange2", fg="white", value='xmlpage',  font=("Calibri", 11, "bold"),  indicatoron=0, width=10,
                      variable=var,
                      command=lambda: start(var.get()))
    rb3 = Radiobutton(button_frame, text='CSV', bg="DarkOrange1", fg="white",selectcolor="DarkOrange2", value='csvpage',  font=("Calibri", 11, "bold"), indicatoron=0, width=10,
                      variable=var, command=lambda: start(var.get()))

    rb1.grid(row=0, column=0)
    rb2.grid(row=0, column=1)
    rb3.grid(row=0, column=2)

    global text
    text = Text(root, bg='black', foreground="white", height="8", width="460")
    text.place(x=125, y=45)
    text.delete("1.0", END)
    text.insert(END, "Opps, not yet connect OR no files to be read....")

    global jsonframe
    jsonframe = Frame(right)
    jsonframe.pack(fill="both", expand=True)

    global xmlframe
    xmlframe = jsonframe
    global csvframe
    csvframe = jsonframe

def start(choice):
    if choice == 'jsonpage':
        hideallframe()

        JsonPresetLBL = Label(jsonframe, text="JSON Preset:", font=("Calibri", 11, "bold"), fg="black")
        JsonPresetLBL.place(x=260, y=172)
        global options, om1, ReviewJSON_button
        options = StringVar(jsonframe)
        options.set("Select")  # default value
        om1 = OptionMenu(jsonframe, options, *jsonprofileName, command=get)
        om1.place(x=350, y=170, width=100)

        ReviewJSON_button = Button(jsonframe, text="Review JSON", command=ReviewJson)
        ReviewJSON_button.place(x=495, y=170, width=90, height=29)
        global CreateNewJsonBtn
        CreateNewJsonBtn = Button(jsonframe, text="Create New", command=newjsonprofile, width=12)
        CreateNewJsonBtn.place(x=630, y=170, height=29)

       # ReviewJsonBtn = Button(jsonframe, text="Review JSON", command=ReviewJson, width=11)
       # ReviewJsonBtn.place(x=350, y=500)

#====================================Key,label,start,end interface ==========================================
        #==========labels only==================
        KeynameLbl = ttk.Label(jsonframe, text="Key Name : ", font=('Helvetica', 10))
        KeynameLbl.place(x=360, y=230)
        StartIndexLbl = ttk.Label(jsonframe, text="Start Index : ", font=('Helvetica', 10))
        StartIndexLbl.place(x=505, y=230)
        EndIndexLbl = ttk.Label(jsonframe, text="End Index: ", font=('Helvetica', 10))
        EndIndexLbl.place(x=640, y=230)
        Key1Lbl = ttk.Label(jsonframe, text="Key 1 : ",font=('Helvetica', 10))
        Key1Lbl.place(x=280, y=260)
        Key2Lbl = ttk.Label(jsonframe, text="Key 2 : ", font=('Helvetica', 10))
        Key2Lbl.place(x=280, y=310)
        Key3Lbl = ttk.Label(jsonframe, text="Key 3 : ", font=('Helvetica', 10))
        Key3Lbl.place(x=280, y=360)
        Key4Lbl = ttk.Label(jsonframe, text="Key 4 : ", font=('Helvetica', 10))
        Key4Lbl.place(x=280, y=410)
        Key5Lbl = ttk.Label(jsonframe, text="Key 5 : ", font=('Helvetica', 10))
        Key5Lbl.place(x=280, y=460)

        AllEntryBoxes()


    elif choice == 'xmlpage':
        hideallframe()
        CreateProfileBtnxml = Button(xmlframe, text="New XML Profile", height=1, width=15)
        CreateProfileBtnxml.place(x=250, y=170)
        DeleteProfileBtnxml = Button(xmlframe, text="Delete XML Profile", height=1, width=15)
        DeleteProfileBtnxml.place(x=400, y=170)

    elif choice == 'csvpage':
        hideallframe()

        CreateProfileBtncsv = Button(csvframe, text="New CSV Profile", height=1, width=15)
        CreateProfileBtncsv.place(x=250, y=170)
        DeleteProfileBtncsv = Button(csvframe, text="Delete CSV Profile", height=1, width=15)
        DeleteProfileBtncsv.place(x=400, y=170)

#Refresh mainfunction for listbox&dropdown
def refresh():

    ListboxContentrefresh()


#Dropdown value
def dropdownvalue ():

    # ==========jsonProfileName================
    cur = con.cursor()
    sqlName = ("select jsonid, jsonprofilename from json")
    # call jsonProfileName
    global jsonprofileName
    jsonprofileName = []
    try:
        cur.execute(sqlName)
        results = cur.fetchall()
        for a in results:
            global data
            data = (a[1])
            jsonprofileName.append(data)

    except:
        messagebox.showinfo("ERROR", "Unable to fetch data.")

#Dropdown refresh function
def DropdownDatabaserefresh():
    dropdownvalue()
    om1.destroy()
    newom1 = OptionMenu(jsonframe, options, *jsonprofileName, command = get)
    newom1.place(x=350, y=170, width=100)


#Listbox refresh function
def ListboxContentrefresh():
    #==========Listbox================
    # THE ITEMS INSERTED WITH A LOOP
    s.send(('flist~s').encode("utf-8"))
    arr = pickle.loads(s.recv(1024))
    listbox.delete(0, END)  # clear listbox
    for i in arr:
        listbox.insert(END, i)

    def mouseHover(event):
        global x
        x = listbox.curselection()[0]
        file = listbox.get(x)

        ext = (".txt", ".csv")
        if file.endswith(ext):
            s.send(("fdown~" + file).encode("utf-8"))  # must have
            data = s.recv(1024).decode("utf-8")
            if data[:6] == 'EXISTS':
                filesize = data[6:]
                s.send("OK".encode("utf-8"))
                f = open(file, 'wb')  # must have
                data = (s.recv(1024))
                totalRecv = len(data)
                f.write(data)
                while int(totalRecv) < int(filesize):
                    data = s.recv(1024)
                    totalRecv += len(data)
                    f.write(data)

                    sys.stdout.write("\r|" + "█" * int((totalRecv / float(filesize)) * 50) + "|{0:.2f}".format(
                        (totalRecv / float(filesize)) * 100) + "%  ")
                    sys.stdout.flush()

                    time.sleep(0.01)
                print("\nDownload Complete!")
                f.close()
                global data2
                data2 = open(file).read().splitlines()

                joined_string = "\n".join(data2)
                text.delete("1.0", END)

                text.insert(END, joined_string)

        else:
            messagebox.showinfo("WARNING", "Currently only .txt/csv file is supported.")

    listbox.bind("<<ListboxSelect>>", mouseHover)

#Get value inside the dropdown value
def get(choice):
    if (jsonprofileName == ""):
        tkMessageBox.showinfo("ERROR", "Fail to retrieve value. Try again later", icon="error")
    else:
        cursor = con.cursor()

        cursor.execute("select * from json where jsonprofilename='" +options.get() + "'")

        rows = cursor.fetchall()

        deleteAllEntry()
    global row
    for row in rows:
        insertAllEntry()

    try:
    #Delete submit button when select existing value
        CreateJsonBtn.destroy()
        CreateNewJsonBtn.configure(state=NORMAL)
        profilenameLbl.destroy()
        ProfileNameEntry.destroy()
    except:
        pass

    global UpdateJsonBtn
    UpdateJsonBtn = Button(jsonframe, text="Update", command=updatetodb, width=11)
    UpdateJsonBtn.place(x=450, y=510)

    global DeleteJsonBtn
    DeleteJsonBtn = Button(jsonframe, text="Delete", command=deletetodb, width=11)
    DeleteJsonBtn.place(x=550, y=510)

def updatetodb():
    getAllEntryBoxes()
    areusureupdate = tkMessageBox.askquestion("Update","Are you sure want to update" + " " + options.get()+ "?",icon='warning')
    if areusureupdate== 'yes':
        if (key1name == "" or key1start == "" or key1end == ""):
            tkMessageBox.showinfo("Error", "The first key  cannot be empty !", icon="error")
        else:

            cursor.execute(
                "update json set jsonkey1 = '" + key1name + "',  jsonstart1 = '" + key1start + "',  jsonend1 = '" + key1end + "', jsonkey2 = '" + key2name + "',  jsonstart2 = '" + key2start + "',  jsonend2 = '" + key2end + "', jsonkey3 = '" + key3name + "',  jsonstart3 = '" + key3start + "',  jsonend3 = '" + key3end + "', jsonkey4 = '" + key4name + "',  jsonstart4 = '" + key4start + "',  jsonend4 = '" + key4end + "', jsonkey5 = '" + key5name + "',  jsonstart5 = '" + key5start + "',  jsonend5 = '" + key5end + "' where jsonprofilename='" + options.get() + "'")
            con.commit()
            tkMessageBox.showinfo("Update success",
                                  "Successfully update records to" + " " + options.get() + " " + "profile")
            DropdownDatabaserefresh()

    else:
        pass


def deletetodb():
    areusuredelete = tkMessageBox.askquestion("Delete", "Are you sure want to delete" + " " + options.get() + "?", icon='warning')
    if areusuredelete == 'yes':
        if (options.get == ""):
            tkMessageBox.showinfo("Error", "You must select a profile to be delete.",  icon='error')
        else:
            cursor = con.cursor()

            cursor.execute("delete from json where jsonprofilename='" + options.get() + "'")
            cursor.execute("commit");
            tkMessageBox.showinfo("Success", "Delete successfully")
            deleteAllEntry()
            options.set("Select")  # default value
            DropdownDatabaserefresh()


def newjsonprofile():
    deleteAllEntry()
    global CreateJsonBtn, profilenameLbl, ProfileNameEntry
    CreateJsonBtn = Button(jsonframe, text="Submit", command=submit, width=11)
    try:
        options.set("Select")  # default value
        CreateJsonBtn.place(x=495, y=550)
        CreateNewJsonBtn.configure(state=DISABLED)
        global profilenameLbl, ProfileNameEntry
        # label & entrybox for profilename
        profilenameLbl = Label(jsonframe, text="Profile Name: ", font=('Helvetica', 10, 'bold'), bd=18)
        profilenameLbl.place(x=360, y=492)
        ProfileNameEntry = Entry(jsonframe)
        ProfileNameEntry.place(x=480, y=510)
    except:
        pass

    for widget in jsonframe.winfo_children():
        if isinstance(widget, Button):
            if widget['text'] == 'Update':
                widget.destroy()

    for widget2 in jsonframe.winfo_children():
        if isinstance(widget2, Button):
            if widget2['text'] == 'Delete':
                widget2.destroy()

#Delete all entry input
def deleteAllEntry():
    try:
        ProfileNameEntry.delete(0, 'end')
    except:
        pass
    key1EntryName.delete(0, 'end')
    key2EntryName.delete(0, 'end')
    key3EntryName.delete(0, 'end')
    key4EntryName.delete(0, 'end')
    key5EntryName.delete(0, 'end')

    key1EntryStartIndex.delete(0, 'end')
    key2EntryStartIndex.delete(0, 'end')
    key3EntryStartIndex.delete(0, 'end')
    key4EntryStartIndex.delete(0, 'end')
    key5EntryStartIndex.delete(0, 'end')

    key1EntryEndIndex.delete(0, 'end')
    key2EntryEndIndex.delete(0, 'end')
    key3EntryEndIndex.delete(0, 'end')
    key4EntryEndIndex.delete(0, 'end')
    key5EntryEndIndex.delete(0, 'end')

#Insert all entry input
def insertAllEntry():
    try:
        ProfileNameEntry.insert(0, row[1])
    except:
        pass
    key1EntryName.insert(0, row[2])
    key2EntryName.insert(0, row[3])
    key3EntryName.insert(0, row[4])
    key4EntryName.insert(0, row[5])
    key5EntryName.insert(0, row[6])

    key1EntryStartIndex.insert(0, row[7])
    key2EntryStartIndex.insert(0, row[8])
    key3EntryStartIndex.insert(0, row[9])
    key4EntryStartIndex.insert(0, row[10])
    key5EntryStartIndex.insert(0, row[11])

    key1EntryEndIndex.insert(0, row[12])
    key2EntryEndIndex.insert(0, row[13])
    key3EntryEndIndex.insert(0, row[14])
    key4EntryEndIndex.insert(0, row[15])
    key5EntryEndIndex.insert(0, row[16])

def getAllEntryBoxes():
    global profilename, key1name,key2name,key3name,key4name,key5name,key1start,key2start,key3start,key4start,key5start, key1end,key2end,key3end,key4end,key5end
    try:
        profilename = ProfileNameEntry.get()
    except:
        pass
    key1name = key1EntryName.get()
    key1start = key1EntryStartIndex.get()
    key1end = key1EntryEndIndex.get()

    key2name = key2EntryName.get()
    key2start = key2EntryStartIndex.get()
    key2end = key2EntryEndIndex.get()

    key3name = key3EntryName.get()
    key3start = key3EntryStartIndex.get()
    key3end = key3EntryEndIndex.get()

    key4name = key4EntryName.get()
    key4start = key4EntryStartIndex.get()
    key4end = key4EntryEndIndex.get()

    key5name = key5EntryName.get()
    key5start = key5EntryStartIndex.get()
    key5end = key5EntryEndIndex.get()


#Declare all entryboxes (Stupid but its worked. Going to loop it after everything completed)
def AllEntryBoxes():
    # ==========Key 1 entries boxes only==================
    global key1EntryName, key2EntryName, key3EntryName, key4EntryName, key5EntryName, key1EntryStartIndex, key2EntryStartIndex, key3EntryStartIndex, key4EntryStartIndex, key5EntryStartIndex, key1EntryEndIndex, key2EntryEndIndex, key3EntryEndIndex, key4EntryEndIndex, key5EntryEndIndex

    key1EntryName = Entry(jsonframe)
    key1EntryName.place(x=340, y=262)
    key1EntryStartIndex = Entry(jsonframe)
    key1EntryStartIndex.place(x=480, y=262)
    key1EntryEndIndex = Entry(jsonframe)
    key1EntryEndIndex.place(x=620, y=262)

    # ==========Key 2 entries boxes only==================
    key2EntryName = Entry(jsonframe)
    key2EntryName.place(x=340, y=310)
    key2EntryStartIndex = Entry(jsonframe)
    key2EntryStartIndex.place(x=480, y=310)
    key2EntryEndIndex = Entry(jsonframe)
    key2EntryEndIndex.place(x=620, y=310)

    # ==========Key 3 entries boxes only==================
    key3EntryName = Entry(jsonframe)
    key3EntryName.place(x=340, y=362)
    key3EntryStartIndex = Entry(jsonframe)
    key3EntryStartIndex.place(x=480, y=362)
    key3EntryEndIndex = Entry(jsonframe)
    key3EntryEndIndex.place(x=620, y=362)

    # ==========Key 4 entries boxes only==================
    key4EntryName = Entry(jsonframe)
    key4EntryName.place(x=340, y=410)
    key4EntryStartIndex = Entry(jsonframe)
    key4EntryStartIndex.place(x=480, y=410)
    key4EntryEndIndex = Entry(jsonframe)
    key4EntryEndIndex.place(x=620, y=410)

    # ==========Key 5 entries boxes only==================
    key5EntryName = Entry(jsonframe)
    key5EntryName.place(x=340, y=462)
    key5EntryStartIndex = Entry(jsonframe)
    key5EntryStartIndex.place(x=480, y=462)
    key5EntryEndIndex = Entry(jsonframe)
    key5EntryEndIndex.place(x=620, y=462)

#hide frame after other radiobutton is pressed
def hideallframe():
    for widget in jsonframe.winfo_children():
        widget.destroy()
    for widget in xmlframe.winfo_children():
        widget.destroy()
    for widget in csvframe.winfo_children():
        widget.destroy()

#Insert/submit value to database
def submit():
    getAllEntryBoxes()
    areusureinsert = tkMessageBox.askquestion("Submit", "Are you sure want to insert"+" "+profilename+" " +"to database?", icon='warning')
    if areusureinsert == 'yes':

        if (key1name == "" or key1start == "" or key1end == "" or profilename == ""):
                tkMessageBox.showinfo("Erorr", "The first key or profile name cannot be empty !", icon="error")
        elif (profilename,) in list_database:  # check profile exist in database or not
                tkMessageBox.showinfo("Error", "The profile name already exists", icon="error")
        elif (len(profilename)) < 5:
                tkMessageBox.showinfo("Error", "The minimum length of profile name is 5 character", icon="error")
        else:
                cursor = con.cursor()
                cursor.execute("insert into json(jsonprofilename, jsonkey1,jsonstart1,jsonend1,jsonkey2,jsonstart2,jsonend2, jsonkey3,jsonstart3,jsonend3, jsonkey4,jsonstart4,jsonend4, jsonkey5,jsonstart5,jsonend5) values ( '" + profilename + "','" + key1name + "','" + key1start + "','" + key1end + "','" + key2name + "','" + key2start + "','" + key2end + "','" + key3name + "','" + key3start + "','" + key3end + "','" + key4name + "','" + key4start + "','" + key4end + "','" + key5name + "','" + key5start + "','" + key5end + "')")
                cursor.execute("commit");
                tkMessageBox.showinfo("Success",
                          "Successfully insert" + " " + profilename + " " + " to database.")

                deleteAllEntry()
                options.set("Select")  # default value
                DropdownDatabaserefresh()
                ProfileNameEntry.delete(0, 'end')

    else:
        pass

#Review JSON format
def ReviewJson():

    #if no selection is choosed
    if x == 183.0:
        tkMessageBox.showinfo("Error", "You must select a file before can review.", icon="error")
    else:
        # ========valdiate buttons for create new profile
        try:

            ReviewJSON_button.configure(state=DISABLED)
            # Delete submit button when select existing value
            CreateJsonBtn.destroy()
            CreateNewJsonBtn.configure(state=NORMAL)
        except:
            pass
        global reviewjson, window
        window = Toplevel(root)
        window.minsize(800, 600)
        window.maxsize(800, 600)
        window.title("Foghorn Publisher - Review Json" + " " + "(" + options.get() + ")")
        window.protocol('WM_DELETE_WINDOW', destroyReviewJSON)
        reviewjson = Text(window, bg='black', foreground="white", height="20", width="500")
        reviewjson.pack()
        reviewjson.config(state=NORMAL)
        reviewjson.delete("1.0", "end")
        file_data.clear()
        global content
        num = 0
        try:
            for content in data2:
                num += 1
                validateAndShowContent()
                OutputToJson()
                DisplayJSON = "" + "Result" + " " + str(num) + " :" + "\n" + tmp + "\n" + "\n"
                reviewjson.insert(END, DisplayJSON)


            global viewJSONSchema_button
            viewJSONSchema_button = Button(window, text="View JSON Schema", command=ViewJsonSchema)
            viewJSONSchema_button.place(x=250, y=400, width=110, height=29)

        except:
            raise


def ViewJsonSchema():
                num = 0
                reviewjson.delete("1.0", "end")
                for content in data2:

                    num += 1
                    validateAndShowContent()
                    OutputToJson()
                    DisplayJSON = "" + "Result" + " " + str(num) + " :" + "\n" + tmp + "\n" + "\n"
                    reviewjson.insert(END, dataofjsonschema)
                    viewJSONSchema_button.configure(text='View Data', command=ReturnToViewJson)

def ReturnToViewJson():
                window.destroy()
                ReviewJson()
def validateAndShowContent():
    # Key1name cant be empty
    if (key1EntryName.get() == ""):
        window.destroy()
        ReviewJSON_button.configure(state=NORMAL)
        tkMessageBox.showinfo("Error", "First key name cannot be empty", icon="error")
    # start index and end index cannot be empty after name is been declared
    elif (key1EntryName.get() != 0) and (key1EntryStartIndex.get() == "") and (key1EntryEndIndex.get() == ""):
        window.destroy()
        ReviewJSON_button.configure(state=NORMAL)
        tkMessageBox.showinfo("Error", "Start index and end index cannot be empty after declaration of key name",
                              icon="error")
    # check 1: check start to EOS
    elif (key1EntryEndIndex.get()) == "":
        file_data[key1EntryName.get()] = content[int(key1EntryStartIndex.get()):]
    # check 1: check EOS to start
    elif (key1EntryStartIndex.get()) == "":
        file_data[key1EntryName.get()] = content[:int(key1EntryEndIndex.get())]
    # check 1: normal status
    else:
        file_data[key1EntryName.get()] = content[int(key1EntryStartIndex.get()):int(key1EntryEndIndex.get())]
    ######################Check 2 ################################
    # check 2: If all empty jiu dont call this part
    if (key2EntryName.get() or key2EntryStartIndex.get() or key2EntryEndIndex.get()) == "":
        pass
    # check 2: start index and end index cannot be empty after name is been declared
    elif (key2EntryName.get() != 0) and (key2EntryStartIndex.get() == "") and (key2EntryEndIndex.get() == ""):
        window.destroy()
        ReviewJSON_button.configure(state=NORMAL)
        tkMessageBox.showinfo("Error", "Start index and end index cannot be empty after declaration of key name",
                              icon="error")
    elif (key2EntryName.get() == "") and (key2EntryStartIndex.get() != 0) and (
            key2EntryEndIndex.get() == ""):
        window.destroy()
        ReviewJSON_button.configure(state=NORMAL)
        tkMessageBox.showinfo("Error", "Key name cannot be empty after declaration of start index",
                              icon="error")
    elif (key2EntryName.get() == "") and (key2EntryStartIndex.get() == "") and (
            key2EntryEndIndex.get() != 0):
        window.destroy()
        ReviewJSON_button.configure(state=NORMAL)
        tkMessageBox.showinfo("Error", "Key name cannot be empty after declaration of end index",
                              icon="error")
    elif (key2EntryName.get() == "") and (key2EntryStartIndex.get() != 0) and (
            key2EntryEndIndex.get() != 0):
        window.destroy()
        ReviewJSON_button.configure(state=NORMAL)
        tkMessageBox.showinfo("Error", "Key name cannot be empty after declaration of start & end index", icon="error")
    # check 2: check start to EOS
    elif (key2EntryEndIndex.get()) == "":
        file_data[key2EntryName.get()] = content[int(key2EntryStartIndex.get()):]
    # check 2: check EOS to start
    elif (key2EntryStartIndex.get()) == "":
        file_data[key2EntryName.get()] = content[:int(key2EntryEndIndex.get())]
    # check 2: normal status
    else:
        file_data[key2EntryName.get()] = content[int(key2EntryStartIndex.get()):int(key2EntryEndIndex.get())]

    ######################Check 3 ################################
    # check 3: If all empty jiu dont call this part
    if (key3EntryName.get() or key3EntryStartIndex.get() or key3EntryEndIndex.get()) == "":
        pass
    # check 3: start index and end index cannot be empty after name is been declared
    elif (key3EntryName.get() != 0) and (key3EntryStartIndex.get() == "") and (
            key3EntryEndIndex.get() == ""):
        window.destroy()
        ReviewJSON_button.configure(state=NORMAL)
        tkMessageBox.showinfo("Error",
                              "Start index and end index cannot be empty after declaration of key name",
                              icon="error")
    elif (key3EntryName.get() == "") and (key3EntryStartIndex.get() != 0) and (
            key3EntryEndIndex.get() == ""):
        window.destroy()
        ReviewJSON_button.configure(state=NORMAL)
        tkMessageBox.showinfo("Error", "Key name cannot be empty after declaration of start index",
                              icon="error")
    elif (key3EntryName.get() == "") and (key3EntryStartIndex.get() == "") and (
            key3EntryEndIndex.get() != 0):
        window.destroy()
        ReviewJSON_button.configure(state=NORMAL)
        tkMessageBox.showinfo("Error", "Key name cannot be empty after declaration of end index",
                              icon="error")
    elif (key3EntryName.get() == "") and (key3EntryStartIndex.get() != 0) and (
            key3EntryEndIndex.get() != 0):
        window.destroy()
        ReviewJSON_button.configure(state=NORMAL)
        tkMessageBox.showinfo("Error",
                              "Key name cannot be empty after declaration of start & end index",
                              icon="error")
    # check 3: check start to EOS
    elif (key3EntryEndIndex.get()) == "":
        file_data[key3EntryName.get()] = content[int(key3EntryStartIndex.get()):]
    # check 3: check EOS to start
    elif (key3EntryStartIndex.get()) == "":
        file_data[key3EntryName.get()] = content[:int(key3EntryEndIndex.get())]
    # check 3: normal status
    else:
        file_data[key3EntryName.get()] = content[
                                         int(key3EntryStartIndex.get()):int(key3EntryEndIndex.get())]

    ######################Check 4 ################################
    # check 4: If all empty jiu dont call this part
    if (key4EntryName.get() or key4EntryStartIndex.get() or key4EntryEndIndex.get()) == "":
        pass
    # check 4: start index and end index cannot be empty after name is been declared
    elif (key4EntryName.get() != 0) and (key4EntryStartIndex.get() == "") and (
            key4EntryEndIndex.get() == ""):
        window.destroy()
        ReviewJSON_button.configure(state=NORMAL)
        tkMessageBox.showinfo("Error",
                              "Start index and end index cannot be empty after declaration of key name",
                              icon="error")
    elif (key4EntryName.get() == "") and (key4EntryStartIndex.get() != 0) and (
            key4EntryEndIndex.get() == ""):
        window.destroy()
        ReviewJSON_button.configure(state=NORMAL)
        tkMessageBox.showinfo("Error", "Key name cannot be empty after declaration of start index",
                              icon="error")
    elif (key4EntryName.get() == "") and (key4EntryStartIndex.get() == "") and (
            key2EntryEndIndex.get() != 0):
        window.destroy()
        ReviewJSON_button.configure(state=NORMAL)
        tkMessageBox.showinfo("Error", "Key name cannot be empty after declaration of end index",
                              icon="error")
    elif (key4EntryName.get() == "") and (key4EntryStartIndex.get() != 0) and (
            key4EntryEndIndex.get() != 0):
        window.destroy()
        ReviewJSON_button.configure(state=NORMAL)
        tkMessageBox.showinfo("Error",
                              "Key name cannot be empty after declaration of start & end index",
                              icon="error")
    # check 4: check start to EOS
    elif (key4EntryEndIndex.get()) == "":
        file_data[key4EntryName.get()] = content[int(key4EntryStartIndex.get()):]
    # check 4: check EOS to start
    elif (key4EntryStartIndex.get()) == "":
        file_data[key4EntryName.get()] = content[:int(key4EntryEndIndex.get())]
    # check 4: normal status
    else:
        file_data[key4EntryName.get()] = content[int(key4EntryStartIndex.get()):int(
            key4EntryEndIndex.get())]

        ######################Check 5 ################################
        # check 5: If all empty jiu dont call this part
    if (key5EntryName.get() or key5EntryStartIndex.get() or key5EntryEndIndex.get()) == "":
        pass
    # check 5: start index and end index cannot be empty after name is been declared
    elif (key5EntryName.get() != 0) and (key5EntryStartIndex.get() == "") and (
            key5EntryEndIndex.get() == ""):
        window.destroy()
        ReviewJSON_button.configure(state=NORMAL)
        tkMessageBox.showinfo("Error",
                              "Start index and end index cannot be empty after declaration of key name",
                              icon="error")
    elif (key5EntryName.get() == "") and (key5EntryStartIndex.get() != 0) and (
            key5EntryEndIndex.get() == ""):
        window.destroy()
        ReviewJSON_button.configure(state=NORMAL)
        tkMessageBox.showinfo("Error",
                              "Key name cannot be empty after declaration of start index",
                              icon="error")
    elif (key5EntryName.get() == "") and (key5EntryStartIndex.get() == "") and (
            key5EntryEndIndex.get() != 0):
        window.destroy()
        ReviewJSON_button.configure(state=NORMAL)
        tkMessageBox.showinfo("Error",
                              "Key name cannot be empty after declaration of end index",
                              icon="error")
    elif (key5EntryName.get() == "") and (key5EntryStartIndex.get() != 0) and (
            key5EntryEndIndex.get() != 0):
        window.destroy()
        ReviewJSON_button.configure(state=NORMAL)
        tkMessageBox.showinfo("Error",
                              "Key name cannot be empty after declaration of start & end index",
                              icon="error")
    # check 5: check start to EOS
    elif (key5EntryEndIndex.get()) == "":
        file_data[key5EntryName.get()] = content[int(key5EntryStartIndex.get()):]
    # check 5: check EOS to start
    elif (key5EntryStartIndex.get()) == "":
        file_data[key5EntryName.get()] = content[:int(key5EntryEndIndex.get())]
    # check 5: normal status
    else:
        file_data[key5EntryName.get()] = content[int(key5EntryStartIndex.get()):int(
            key5EntryEndIndex.get())]


def OutputToJson():
    # output to JSON
    global tmp, dataofjsonschema, DisplayJSON
    tmp = json.dumps(file_data, ensure_ascii=False, indent="\t")
    builder = SchemaBuilder()
    datastore = json.loads(tmp)
    # print(datastore)
    builder.add_object(datastore)
    dataofjsonschema = builder.to_schema()
    # print(dataofjsonschema)



def destroyReviewJSON():
    ReviewJSON_button.configure(state=NORMAL)
    window.destroy()




# ========================================Open Window==================================
ConnectForm()


# ========================================INITIALIZATION===================================
if __name__ == '__main__':

    root.mainloop()