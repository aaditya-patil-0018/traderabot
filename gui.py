from tkinter import *
from tkinter import ttk
import sqlite3
from main import Tradera

con = sqlite3.connect("category.db")
cur = con.cursor()

cur.execute("SELECT * FROM categories")
categories = cur.fetchall()

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

root = Tk()
root.title("Tradera Bot")
root.geometry("700x500")

category_selected = ""
subcategory_selected = ""

def selectItem(a):
    global tree1
    global category_selected
    curItem = tree.focus()
    category_selected = tree.item(curItem)['values'][1]
    tree1 = ttk.Treeview(root, height=20)
    tree1['columns'] = ('ID', 'CATEGORY')
    tree1.column("#0", width=0, minwidth=0)
    tree1.column("ID", anchor=CENTER, width=100)
    tree1.column("CATEGORY", anchor=W, width=240)
    tree1.heading("#0", text="")
    tree1.heading("ID", text="ID", anchor=CENTER)
    tree1.heading("CATEGORY", text="CATEGORY", anchor=W)
    if category_selected != "":
        count = 0
        for key in subcategories[category_selected]:
            tree1.insert(parent='', index='end', iid=count, text="Parent", values=(str(count+1),key[1]))
            count += 1
    tree1.grid(column=1, row=0)

tree = ttk.Treeview(root, height=20)
tree['columns'] = ('ID', 'CATEGORY')
tree.column("#0", width=0, minwidth=0)
tree.column("ID", anchor=CENTER, width=100)
tree.column("CATEGORY", anchor=W, width=240)
tree.heading("#0", text="")
tree.heading("ID", text="ID", anchor=CENTER)
tree.heading("CATEGORY", text="CATEGORY", anchor=W)
tree.bind('<ButtonRelease-1>', selectItem)
count = 0
for key in subcategories:
    tree.insert(parent='', index='end', iid=count, text="Parent", values=(str(count+1),key))
    count += 1
tree.grid(column=0, row=0)

l1 = Label(root, text="CATEGORY ID").grid(row=1, column=0)
category_box = Entry(root, width=20)
category_box.grid(row=1, column=1)

l2 = Label(root, text="SUBCATEGORY ID").grid(row=2, column=0)
subcategory_box = Entry(root, width=20)
subcategory_box.grid(row=2, column=1)

def run():
    cb =category_box.get()
    sb = subcategory_box.get()
    trade = Tradera(cb, sb)

submit = Button(root, text="Run", command=run)
submit.grid(row=3, column=0)

root.mainloop()
