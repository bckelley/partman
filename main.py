from email import message
from select import select
from tkinter import *
from tkinter import messagebox
from db import Database





db = Database('store.db')

def populate_list():
    part_list.delete(0, END)
    for row in db.fetch():
        part_list.insert(END, row)

def add_part():
    if part_txt.get() == '' or customer_txt.get() == '' or retailer_txt.get() == '' or price_txt.get() == '':
        messagebox.showerror('required Fields', 'Please include all fields')
        return
    
    db.insert(part_txt.get(), 
              customer_txt.get(), 
              retailer_txt.get(), 
              price_txt.get())
    part_list.delete(0, END)
    part_list.insert(END, 
              part_txt.get(), 
              customer_txt.get(), 
              retailer_txt.get(), 
              price_txt.get())
    populate_list() 
    
def select_item(event):
    try:
        
        global selected_item
        index = part_list.curselection()[0]
        selected_item = part_list.get(index)
        
        part_entry.delete(0, END)
        part_entry.insert(END, selected_item[1])
        customer_entry.delete(0, END)
        customer_entry.insert(END, selected_item[2])
        retailer_entry.delete(0, END)
        retailer_entry.insert(END, selected_item[3])
        price_entry.delete(0, END)
        price_entry.insert(END, selected_item[4])
        
    except IndexError:
        pass
    

def remove_part():
    db.remove(selected_item[0])
    clear_txt()
    populate_list()
    
def update_part():
    db.update(selected_item[0], 
              part_txt.get(), 
              customer_txt.get(), 
              retailer_txt.get(), 
              price_txt.get())
    populate_list()
    
def clear_txt():
    part_entry.delete(0, END)
    customer_entry.delete(0, END)
    retailer_entry.delete(0, END)
    price_entry.delete(0, END)

#  create window object
app = Tk()

# Part
part_txt = StringVar()
part_lbl = Label(app, text='Part Name', font=('bold', 14), pady=20).grid(row=0, column=0, sticky=W)
part_entry = Entry(app, textvariable=part_txt)
part_entry.grid(row=0, column=1)

# Customer
customer_txt = StringVar()
customer_lbl = Label(app, text='Customer', font=('bold', 14)).grid(row=0, column=2, sticky=W)
customer_entry = Entry(app, textvariable=customer_txt)
customer_entry.grid(row=0, column=3)

# Retailer
retailer_txt = StringVar()
retailer_lbl = Label(app, text='Retailer', font=('bold', 14)).grid(row=1, column=0, sticky=W)
retailer_entry = Entry(app, textvariable=retailer_txt)
retailer_entry.grid(row=1, column=1)

# Price
price_txt = StringVar()
price_lbl = Label(app, text='Price', font=('bold', 14)).grid(row=1, column=2, sticky=W)
price_entry = Entry(app, textvariable=price_txt)
price_entry.grid(row=1, column=3)

# Part List
part_list = Listbox(app, height=8, width=50, border=0)
part_list.grid(row=3, column=0, columnspan=3, rowspan=6, pady=20, padx=20)

# Create scrollbar
scrollbar = Scrollbar(app)
scrollbar.grid(row=3, column=3)

# Set scroll to listbox
part_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=part_list.yview)

# Bind Select
part_list.bind('<<ListboxSelect>>', select_item)

# Buttons
add_btn = Button(app, text='Add Part', width=12, command=add_part)
add_btn.grid(row=2, column=0, pady=20)

remove_btn = Button(app, text='Remove Part', width=12, command=remove_part)
remove_btn.grid(row=2, column=1)

update_btn = Button(app, text='Update Part', width=12, command=update_part)
update_btn.grid(row=2, column=2)

clear_btn = Button(app, text='Clear Input', width=12, command=clear_txt)
clear_btn.grid(row=2, column=3)




app.title("Part Manager")
app.geometry('700x350')

# Populate List
populate_list()


#  start
app.mainloop()