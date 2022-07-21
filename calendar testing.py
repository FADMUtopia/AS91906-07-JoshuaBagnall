import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
import tkcalendar
from tkcalendar import Calendar, DateEntry
import datetime

root = tk.Tk()

events={'2018-09-28':('London','meeting'),\
    '2018-08-15':('Paris','meeting'),\
    '2018-07-30':('New York','meeting')}

cal = Calendar(root, selectmode='day', year=2018, month=8)

for k in events.keys():
    date=datetime.datetime.strptime(k,"%Y-%m-%d").date()
    cal.calevent_create(date, events[k][0], events[k][1])

cal.tag_config('meeting', background='red', foreground='yellow')
cal.pack(fill="both", expand=True)

root.mainloop()