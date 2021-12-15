from tkinter import *
from tkinter import ttk
import sqlite3
from main import Tradera

#-----------------------------------------------------------------------------------------------------
con = sqlite3.connect("category.db")
cur = con.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
cname = cur.fetchall()
categories = []
category_names = []
c = 1
for i in cname:
    categories.append([c, i[0]])
    category_names.append(i[0])
    c += 1

subcategories = {}

for category in categories:
    tablename = category[1].replace(" ","")
    if '&' in tablename:
        tablename = tablename.replace('&', '')
    if ',' in tablename:
        tablename = tablename.replace(',','')   
    if '-' in tablename:
        tablename = tablename.replace('-','')
    subcategory_data = cur.execute(f"SELECT * FROM {tablename}").fetchall()
    subcategories[category[1]] = subcategory_data

con.commit()
con.close()

#-----------------------------------------------------------------------------------------------------
con = sqlite3.connect('subcategory.db')
cur = con.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
d = cur.fetchall()

sscategory = []
for i in d:
    sscategory.append(i[0])

subsubcategory = {}
for j in sscategory:
    cur.execute(f"SELECT * FROM {j}")
    e = cur.fetchall()
    subsubcategory[j] = e

con.commit()
con.close()
#-----------------------------------------------------------------------------------------------------

con = sqlite3.connect('subsubcategory.db')
cur = con.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table'")

ssscategory = []
for k in cur.fetchall():
    ssscategory.append(k[0])

subsubsubcategories = {}
for l in ssscategory:
    cur.execute(f"SELECT * FROM {l}")
    f = cur.fetchall()
    subsubsubcategories[l] = f

con.commit()
con.close()

#-----------------------------------------------------------------------------------------------------
root = Tk()
root.title("Tradera Bot")
root.geometry("1800x500")

# Search thing
f1 = Frame(root)
sl = Label(f1, text="Search: ")
sl.grid(row=0,column=0)
search = Entry(f1)
search.config(width=100)
search.grid(row=0, column=1)
f1.pack()

# Cat Frame
f2 = Frame(root)
category_selected = ""
subcategory_selected = ""

def changesub(*args):
    global drop1
    clicked1 = StringVar()
    clicked1.set(subcategories[clicked.get()][0])
    drop1.destroy()
    s = subcategories[clicked.get()]
    drop1 = OptionMenu(f2, clicked1, *s)
    drop1.grid(row=0, column=1, padx=18)

def changesub1(*args):
    global drop2
    clicked2 = StringVar()
    clicked2.set(subsubcategory[f"{clicked.get()}{clicked1.get()}"][0][1].replace(' ', ''))
    drop2.destroy()
    ssj = subsubcategory[f"{clicked.get()}{clicked1.get()}"]
    ss = []
    for rr in ssj:
        ss.append(rr[1])
    drop2 = OptionMenu(f2, *ss)
    drop2.grid(row=0, column=2, padx=18)

def changesub2(*args):
    global drop3
    clicked3 = StringVar()
    a = clicked2.get()
    tablename = a
    if '&' in tablename:
        tablename = tablename.replace('&', '')
    if ',' in tablename:
        tablename = tablename.replace(',','')   
    if '-' in tablename:
        tablename = tablename.replace('-','')
    clicked3.set(subsubsubcategories[f"{clicked.get()}{clicked1.get()}{tablename}"][0])
    drop3.destroy()
    sss = subsubsubcategories[f"{clicked.get()}{clicked1.get()}{tablename}"]
    drop3 = OptionMenu(f2, *sss)
    drop3.grid(row=0, column=3, padx=18)
#---------------------------------------------------------------------------------------------------

clicked = StringVar(value="Accessoarer")
clicked.trace( "w", changesub )
drop = OptionMenu( f2 , clicked , *category_names )
drop.grid(row=0, column=0, padx=18)

#---------------------------------------------------------------------------------------------------

clicked1 = StringVar(value=subcategories[clicked.get()][0][1])
clicked1.trace('w', changesub1)
# clicked1.set(subcategories[clicked.get()][0][1])
sj = subcategories[clicked.get()]
s = []
for r in sj:
    s.append(r[1])
drop1 = OptionMenu(f2, clicked1, *s)
drop1.grid(row=0, column=1, padx=18)

#---------------------------------------------------------------------------------------------------

clicked2 = StringVar(value=subsubcategory[f"{clicked.get()}{clicked1.get()}"][0][1].replace(' ', ''))
clicked2.trace('w', changesub2)
# clicked2.set(subsubcategory[f"{clicked.get()}{clicked1.get()}"][0][1].replace(' ', ''))
ssj = subsubcategory[f"{clicked.get()}{clicked1.get()}"]
ss = []
for rr in ssj:
    ss.append(rr[1])
drop2 = OptionMenu(f2, *ss)
drop2.grid(row=0, column=2, padx=18)

#---------------------------------------------------------------------------------------------------

clicked3 = StringVar()
a = clicked2.get()
tablename = a
if '&' in tablename:
    tablename = tablename.replace('&', '')
if ',' in tablename:
    tablename = tablename.replace(',','')   
if '-' in tablename:
    tablename = tablename.replace('-','')
clicked3.set(subsubsubcategories[f"{clicked.get()}{clicked1.get()}{tablename}"][0])
sss = subsubsubcategories[f"{clicked.get()}{clicked1.get()}{tablename}"]
drop3 = OptionMenu(f2, *sss)
drop3.grid(row=0, column=3, padx=18)

#---------------------------------------------------------------------------------------------------
f2.pack(pady=9)
#---------------------------------------------------------------------------------------------------

f3 = Frame(root)

buy = Button(f3, text="Buy Now")
buy.grid(row=0, column=0, padx=18)

add = Button(f3, text="Add New Search")
add.grid(row=0, column=1, padx=18)

f3.pack(pady=9)

l = Label(root, text='Active Searches')
l.pack(pady=9)

cv = Canvas(root, width=500, height=250, bg='grey')
cv.pack()

root.mainloop()
