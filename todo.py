import time
import threading
import re
from Tkinter import *
import tkMessageBox

def alarm():

    tkMessageBox.showinfo("Times Up!", message)

def loadfile():

    files = open("savefile.txt", "r+")
    alltext = files.read()
    alltext = re.split("\n", alltext)
    
    for i in range(0, len(alltext) - 1 ,4):
        
        text = alltext[i]
        hours = int( alltext[i + 1] )
        minets = int( alltext[i + 2] )
        AmPm = alltext[i + 3]

        localtime = time.asctime( time.localtime(time.time()) )
        minetsnow = int(localtime[14:16])

        minetsleft = minets - minetsnow

        if AmPm == "pm" or AmPm == "PM":
            
            hours = hours + 12
            
        localtime = time.asctime( time.localtime(time.time()) )
        hoursnow = int(localtime[11:13])

        hoursleft = hours - hoursnow

        if minetsleft < 0:

            hoursleft = hoursleft - 1
            minetsleft = minetsleft + 60

        listbox.insert(END, " - " + text + "      " + "hours left: " + str(hoursleft) + ":" + str(minetsleft))

        global message
        message = text
        timertime = hoursleft*3600.0 + minetsleft*60.0
        t = threading.Timer(timertime, alarm)
        t.start()
    
def timeget():
    
    localtime = time.asctime( time.localtime(time.time()) )
    timeHours = int(localtime[11:13])
    timeminets = int(localtime[14:16])
    
    return timeHours

def clock():

    localtime = time.asctime( time.localtime(time.time()) )
    minets = int(localtime[14:16])
    
    timeminets = int(timemin.get()) - minets

    if ampm.get() == "pm" or ampm.get() == "PM":

        timeh = int(timehours.get()) + 12

    else:

        timeh = int(timehours.get())
    
    localtime = time.asctime( time.localtime(time.time()) )
    Hours = int(localtime[11:13])
    
    timetill = timeh - Hours

    if timeminets < 0:

        timetill = timetill - 1
        timeminets = timeminets + 60
    
    return str(timetill) + ":" + str(timeminets) 

def killlist():

    save = open("savefile.txt", "wb")
    save.write("")
    save.close()
    
    listbox.delete(0, END)


def addnew():

    listbox.insert(END, " - " + todo.get() + "      " + "hours left: " + clock())
    save = open("savefile.txt","a")
    save.write(todo.get() + " \n " + timehours.get() + "\n" + timemin.get() + "\n" + ampm.get() + "\n")
    save.close()

    global message
    message = todo.get()
    
    hourminute = re.split(":", clock())
    timertime = float(hourminute[0])*3600.0 + float(hourminute[1])*60.0
    t = threading.Timer(timertime, alarm)
    t.start()
    clock()
    

def new():

       
    addnewtodo = Frame(root)
    addnewtodo.pack(side=LEFT, fill=Y, padx=2)

    top = Label(addnewtodo, text="add new entry:")
    top.pack(side=TOP)
    
    global todo
    
    todo = StringVar() 
    title = Entry(addnewtodo, textvariable=todo)
    title.pack(pady=10)

    frame4 = Frame(addnewtodo)
    frame4.pack()

    global ampm
    
    ampm = StringVar()
    pmam = Entry(frame4, textvariable=ampm, width=3)
    pmam.pack(side=RIGHT)
    
    global timemin
    
    timemin = StringVar()
    minets = Entry(frame4, textvariable=timemin, width=2)
    minets.pack(side=RIGHT)

    label = Label(frame4, text= " : ")
    label.pack(side=RIGHT)

    global timehours
    
    timehours = StringVar()
    hours = Entry(frame4, textvariable=timehours, width=2)
    hours.pack(side=RIGHT)

    label2 = Label(frame4, text="Time: ")
    label2.pack(side=RIGHT)
 
root = Tk()
root.title("ToDo")

applet = Frame(root)
applet.pack(side=LEFT, pady=1, padx=1)

frame1 = Frame(applet)
frame1.pack(fill=X)

bar = Scrollbar(frame1, orient=VERTICAL)
bar.pack(side=RIGHT, fill=Y)

listbox = Listbox(frame1, height=20, width=40)
listbox.pack(fill=X, side=RIGHT)

bar.configure(command=listbox.yview)
listbox.configure(yscrollcommand=bar.set)

frame2 = Frame(applet)
frame2.pack(fill=X)

new()

button = Button(frame2, text= "+", width=1, height=1, command=addnew)
button.pack(side=LEFT)

button2 = Button(frame2, text= "-", width=1, height=1, command=killlist)
button2.pack(side=LEFT)

loadfile()

root.mainloop()
