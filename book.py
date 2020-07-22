# Importing modules
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from tkinter import messagebox
import mysql.connector as mysql
from tkcalendar import Calendar
import datetime
import webbrowser
from datetime import datetime as dt
from PIL import Image, ImageTk
import Pmw
import pygame
import time


# Main window and initialization of modules
root = Tk()
root.title('Library')
root.geometry('469x390+300+300')
root.iconbitmap('images/main.ico')
root.resizable(False,False)
root.focus_force()
pygame.mixer.init()
pygame.mixer.music.load('audio/main open.mp3')
pygame.mixer.music.play()

# Assigning font for the GUI 
font_text = Font(family='helvetica', size='11')


# Function to show all logs
def all_logs():

    log = Toplevel(root)
    log.title('View all Visitors')
    log.focus_force()
    log.iconbitmap('images/all_log.ico')
    log.geometry('+150+200')
    log.resizable(False,False)

    def out():
        pygame.mixer.music.load('audio/main open.mp3')
        pygame.mixer.music.play()
        time.sleep(0.3)
        log.destroy()

    # Number of data fetched
    cone = mysql.connect(host='', user='',
                        password='', database='')
    ca = cone.cursor()
    sql_command_01 = 'SELECT * FROM borrow;'
    ca.execute(sql_command_01)
    result = ca.fetchall()

    # setup treeview
    columns = (('ID', 80), ('S_ID', 80), ('S_NAME', 300), ('Title of the book', 500), ('Accession no. of book', 80),
               ('Date Taken', 100), ('Due Date', 100), ('Date_Returned', 100), ('Status', 80))
    tree = ttk.Treeview(log, height=20, columns=[
                        x[0] for x in columns], show='headings')
    tree.grid(row=0, column=0, sticky='news')

    # setup columns attributes
    for col, width in columns:
        tree.heading(col, text=col)
        tree.column(col, width=width, anchor=tk.CENTER)

    # fetch data
    con = mysql.connect(host='', user='',
                        password='', database='')
    c = con.cursor()
    sql_command_1 = 'SELECT * FROM borrow;'
    c.execute(sql_command_1)

    # populate data to treeview
    for rec in c:
        tree.insert('', 'end', value=rec)

    pygame.mixer.music.load('audio/pop_open.mp3')
    pygame.mixer.music.play()

    def pop_menu(event):
        global column
        tree.identify_row(event.y)
        column = tree.identify_column(event.x)
        popup1.post(event.x_root,event.y_root)

    def copy():
        row_id = tree.selection()
        column_no = column
        select = tree.set(row_id,column_no)
        log.clipboard_append(select)
        log.update()
        
    popup1 = Menu(log,tearoff=0)
    popup1.add_command(label='Copy',command=copy)

    tree.bind('<Button-3>',pop_menu)

    # scrollbar
    sb = tk.Scrollbar(log, orient=tk.VERTICAL, command=tree.yview)
    sb.grid(row=0, column=1, sticky='ns')
    tree.config(yscrollcommand=sb.set)
    a = tree.item(tree.focus())['values']

    btn = tk.Button(log, text='Close', command=out,
                    width=20, bd=2, fg='red',font=font_text)
    btn.grid(row=2, column=0, columnspan=2, sticky=E+W)
    status = Label(log,text=f'Total records fetched: {len(result)}',bd=1,relief=SUNKEN,anchor=W)
    status.grid(row=1,columnspan=2,sticky=E+W)
    con.close()
    cone.close()

# Fuction to show specific logs
def sp_logs():
    
    global q_mark_new
    master = Toplevel(root)
    master.title('Search Book')
    master.focus_force()
    master.geometry('+500+200')
    master.resizable(False,False)
    master.iconbitmap('images/visitors.ico')
    Pmw.initialise(master)
    pygame.mixer.music.load('audio/pop_open.mp3')
    pygame.mixer.music.play()

    e_sch = Entry(master)
    drop = ttk.Combobox(master, value=['Search by....', 'Sl.no.', 'Student ID', 'Student Name',
                                       'Title', 'Accession no. of book', 'Date Taken', 'Due Date', 'Date Returned','Approximate Accession no.','Approximate Sl.no.', 'Status'], state='readonly')
    drop.current(0)

    def dbase(event=None):
        a = drop.get()

        if a == 'Search by....':
            messagebox.showerror(
                'No choice given', 'Please choose a valid option to search by....',parent=master)
            master.focus_force()

        elif a == 'Sl.no.' or a == 'Date Taken' or a == 'Date Returned' or a == 'Due Date' or a == 'Accession no. of book':
            if e_sch.get() == '':
                messagebox.showerror(
                'No data enter', 'Please enter a data in the box to search',parent=master)
                master.focus_force()
           
            else:
                con = mysql.connect(host='', user='',
                                    password='', database='')
                c = con.cursor()
                sql_command_2 = 'SELECT * from borrow where `{}` = %s;'
                sql_command_2 = sql_command_2.format(a)
                values = (e_sch.get(),)
                c.execute(sql_command_2,values)
                recs = c.fetchall()

                if recs == []:
                    messagebox.showerror('Does not exist', "No such data found here, make sure you've entered the correct information",parent=master)
                    master.focus_force()

                else:
                    log = Toplevel(root)
                    log.title('View all Visitors')
                    log.focus_force()
                    log.iconbitmap('images/all_log.ico')
                    log.resizable(False,False)
                    log.geometry('+150+200')
                    pygame.mixer.music.load('audio/pop_open.mp3')
                    pygame.mixer.music.play()

                    def out():
                        pygame.mixer.music.load('audio/main open.mp3')
                        pygame.mixer.music.play()
                        time.sleep(0.3)
                        log.destroy()

                    # setup treeview
                    columns = (('Sl.no', 80), ('S_ID', 80), ('S_NAME', 300), ('Title of the book', 500), ('Accession no. of book', 80),
                            ('Date Taken', 100), ('Due Date', 100), ('Date_Returned', 100), ('Status', 80))
                    tree = ttk.Treeview(log, height=20, columns=[
                                        x[0] for x in columns], show='headings')
                    tree.grid(row=0, column=0, sticky='news')

                    # setup columns attributes
                    for col, width in columns:
                        tree.heading(col, text=col)
                        tree.column(col, width=width, anchor=tk.CENTER)

                    # fetch data
                    con = mysql.connect(host='', user='',
                                        password='', database='')
                    c = con.cursor()
                    sql_command_3 = f'SELECT * from borrow where `{a}` = "{e_sch.get()}";'
                    c.execute(sql_command_3)

                    # populate data to treeview
                    for rec in c:
                        tree.insert('', 'end', value=rec)
                    
                    def pop_menu(event):
                        global column
                        tree.identify_row(event.y)
                        column = tree.identify_column(event.x)
                        popup1.post(event.x_root,event.y_root)

                    def copy():
                        row_id = tree.selection()
                        column_no = column
                        select = tree.set(row_id,column_no)
                        log.clipboard_append(select)
                        log.update()
                        
                    popup1 = Menu(log,tearoff=0)
                    popup1.add_command(label='Copy',command=copy)

                    tree.bind('<Button-3>',pop_menu)
                    
                    # scrollbar
                    sb = tk.Scrollbar(log, orient=tk.VERTICAL, command=tree.yview)
                    sb.grid(row=0, column=1, sticky='ns')
                    tree.config(yscrollcommand=sb.set)
                    a = tree.item(tree.focus())['values']

                    btn = tk.Button(log, text='Close', command=out,
                                    width=20, bd=2, fg='red',font=font_text)
                    btn.grid(row=2, column=0, columnspan=2, sticky=E+W)
                    status = Label(log,text=f'Total records fetched: {len(recs)}',bd=1,relief=SUNKEN,anchor=W)
                    status.grid(row=1,columnspan=2,sticky=E+W)
                    con.close()
                    e_sch.delete(0,END)

        elif a == 'Approximate Accession no.':
            if e_sch.get() == '':
                messagebox.showerror(
                    'No data enter', 'Please enter a data in the box to search',parent=master)
                master.focus_force()
            
            else:
                con = mysql.connect(host='', user='',
                                    password='', database='')
                c = con.cursor()
                sql_command_28 = 'SELECT * from borrow where `Accession no. of book` REGEXP %s;'
                values_28 = (e_sch.get(),)
                c.execute(sql_command_28,values_28)
                recs = c.fetchall()

                if recs == []:
                    messagebox.showerror('Does not exist', "No such data found here, make sure you've entered the correct information",parent=master)
                    master.focus_force()

                else:
                    log = Toplevel(root)
                    log.title('View all Visitors')
                    log.focus_force()
                    log.iconbitmap('images/all_log.ico')
                    log.geometry('+150+200')
                    log.resizable(False,False)
                    pygame.mixer.music.load('audio/pop_open.mp3')
                    pygame.mixer.music.play()

                    def out():
                        pygame.mixer.music.load('audio/main open.mp3')
                        pygame.mixer.music.play()
                        time.sleep(0.3)
                        log.destroy()

                    # setup treeview
                    columns = (('Sl.no', 80), ('S_ID', 80), ('S_NAME', 300), ('Title of the book', 500), ('Accession no. of book', 80),
                            ('Date Taken', 100), ('Due Date', 100), ('Date_Returned', 100), ('Status', 80))
                    tree = ttk.Treeview(log, height=20, columns=[
                                        x[0] for x in columns], show='headings')
                    tree.grid(row=0, column=0, sticky='news')

                    # setup columns attributes
                    for col, width in columns:
                        tree.heading(col, text=col)
                        tree.column(col, width=width, anchor=tk.CENTER)

                    # fetch data
                    con = mysql.connect(host='', user='',
                                        password='', database='')
                    c = con.cursor()
                    sql_command_29 = f'SELECT * from borrow where `Accession no. of book` REGEXP %s;'
                    values_29 = (e_sch.get(),)
                    c.execute(sql_command_29,values_29)

                    # populate data to treeview
                    for rec in c:
                        tree.insert('', 'end', value=rec)
                    
                    def pop_menu(event):
                        global column
                        tree.identify_row(event.y)
                        column = tree.identify_column(event.x)
                        popup1.post(event.x_root,event.y_root)

                    def copy():
                        row_id = tree.selection()
                        column_no = column
                        select = tree.set(row_id,column_no)
                        log.clipboard_append(select)
                        log.update()
                        
                    popup1 = Menu(log,tearoff=0)
                    popup1.add_command(label='Copy',command=copy)

                    tree.bind('<Button-3>',pop_menu)
                    
                    # scrollbar
                    sb = tk.Scrollbar(log, orient=tk.VERTICAL, command=tree.yview)
                    sb.grid(row=0, column=1, sticky='ns')
                    tree.config(yscrollcommand=sb.set)
                    a = tree.item(tree.focus())['values']

                    btn = tk.Button(log, text='Close', command=out,
                                    width=20, bd=2, fg='red',font=font_text)
                    btn.grid(row=2, column=0, columnspan=2, sticky=E+W)
                    status = Label(log,text=f'Total records fetched: {len(recs)}',bd=1,relief=SUNKEN,anchor=W)
                    status.grid(row=1,columnspan=2,sticky=E+W)
                    con.close()
                    e_sch.delete(0,END)

        elif a == 'Approximate Sl.no.':
            if e_sch.get() == '':
                messagebox.showerror(
                'No data entered', 'Please enter a data in the box to search',parent=master)
                master.focus_force()
           
            else:
                con = mysql.connect(host='', user='',
                                    password='', database='')
                c = con.cursor()
                sql_command_30 = 'SELECT * from borrow where `sl.no.` REGEXP %s;'
                values_30 = (e_sch.get(),)
                c.execute(sql_command_30,values_30)
                recs = c.fetchall()

                if recs == []:
                    messagebox.showerror('Does not exist', "No such data found here, make sure you've entered the correct information",parent=master)
                    master.focus_force()

                else:
                    log = Toplevel(root)
                    log.title('View all Visitors')
                    log.focus_force()
                    log.iconbitmap('images/all_log.ico')                    
                    log.geometry('+150+200')
                    log.resizable(False,False)
                    pygame.mixer.music.load('audio/pop_open.mp3')
                    pygame.mixer.music.play()

                    def out():
                        pygame.mixer.music.load('audio/main open.mp3')
                        pygame.mixer.music.play()
                        time.sleep(0.3)
                        log.destroy()

                    # setup treeview
                    columns = (('Sl.no', 80), ('S_ID', 80), ('S_NAME', 300), ('Title of the book', 500), ('Accession no. of book', 80),
                            ('Date Taken', 100), ('Due Date', 100), ('Date_Returned', 100), ('Status', 80))
                    tree = ttk.Treeview(log, height=20, columns=[
                                        x[0] for x in columns], show='headings')
                    tree.grid(row=0, column=0, sticky='news')

                    # setup columns attributes
                    for col, width in columns:
                        tree.heading(col, text=col)
                        tree.column(col, width=width, anchor=tk.CENTER)

                    # fetch data
                    con = mysql.connect(host='', user='',
                                        password='', database='')
                    c = con.cursor()
                    sql_command_31 = f'SELECT * from borrow where `sl.no.` REGEXP %s;'
                    values_31 = (e_sch.get(),)
                    c.execute(sql_command_31,values_31)

                    # populate data to treeview
                    for rec in c:
                        tree.insert('', 'end', value=rec)
                    
                    def pop_menu(event):
                        global column
                        tree.identify_row(event.y)
                        column = tree.identify_column(event.x)
                        popup1.post(event.x_root,event.y_root)

                    def copy():
                        row_id = tree.selection()
                        column_no = column
                        select = tree.set(row_id,column_no)
                        log.clipboard_append(select)
                        log.update()
                        
                    popup1 = Menu(log,tearoff=0)
                    popup1.add_command(label='Copy',command=copy)

                    tree.bind('<Button-3>',pop_menu)
                    
                    # scrollbar
                    sb = tk.Scrollbar(log, orient=tk.VERTICAL, command=tree.yview)
                    sb.grid(row=0, column=1, sticky='ns')
                    tree.config(yscrollcommand=sb.set)
                    a = tree.item(tree.focus())['values']

                    btn = tk.Button(log, text='Close', command=out,
                                    width=20, bd=2, fg='red',font=font_text)
                    btn.grid(row=2, column=0, columnspan=2, sticky=E+W)
                    status = Label(log,text=f'Total records fetched: {len(recs)}',bd=1,relief=SUNKEN,anchor=W)
                    status.grid(row=1,columnspan=2,sticky=E+W)
                    con.close()
                    e_sch.delete(0,END)

        else:
            if e_sch.get() == '':
                messagebox.showerror(
                'No data enter', 'Please enter a data in the box to search',parent=master)
                master.focus_force()
            
            else:
                con = mysql.connect(host='', user='',
                                    password='', database='')
                c = con.cursor()
                sql_command_4 = 'SELECT * from borrow where `{}` REGEXP %s;'
                sql_command_4 = sql_command_4.format(a)
                values_4 = (e_sch.get(),)
                c.execute(sql_command_4,values_4)
                recs = c.fetchall()

                if recs == []:
                    messagebox.showerror('Does not exist', "No such data found here, make sure you've entered the write information",parent=master)
                    master.focus_force()

                else:
                    log = Toplevel(root)
                    log.title('View all Visitors')
                    log.focus_force()
                    log.iconbitmap('images/all_log.ico')
                    log.geometry('+150+200')
                    log.resizable(False,False)
                    pygame.mixer.music.load('audio/pop_open.mp3')
                    pygame.mixer.music.play()

                    def out():
                        pygame.mixer.music.load('audio/main open.mp3')
                        pygame.mixer.music.play()
                        time.sleep(0.3)
                        log.destroy()

                    # setup treeview
                    columns = (('Sl.no', 80), ('S_ID', 80), ('S_NAME', 300), ('Title of the book', 500), ('Accession no. of book', 80),
                            ('Date Taken', 100), ('Due Date', 100), ('Date_Returned', 100), ('Status', 80))
                    tree = ttk.Treeview(log, height=20, columns=[
                                        x[0] for x in columns], show='headings')
                    tree.grid(row=0, column=0, sticky='news')

                    # setup columns attributes
                    for col, width in columns:
                        tree.heading(col, text=col)
                        tree.column(col, width=width, anchor=tk.CENTER)

                    # fetch data
                    sql_command_5 = 'SELECT * from borrow where `{}` REGEXP %s;'
                    sql_command_5 = sql_command_5.format(a)
                    values_5 = (e_sch.get(),)
                    c.execute(sql_command_5,values_5)

                    # populate data to treeview
                    for rec in c:
                        tree.insert('', 'end', value=rec)

                    def pop_menu(event):
                        global column
                        tree.identify_row(event.y)
                        column = tree.identify_column(event.x)
                        popup1.post(event.x_root,event.y_root)

                    def copy():
                        row_id = tree.selection()
                        column_no = column
                        select = tree.set(row_id,column_no)
                        log.clipboard_append(select)
                        log.update()
                        
                    popup1 = Menu(log,tearoff=0)
                    popup1.add_command(label='Copy',command=copy)

                    tree.bind('<Button-3>',pop_menu)    

                    # scrollbar
                    sb = tk.Scrollbar(log, orient=tk.VERTICAL, command=tree.yview)
                    sb.grid(row=0, column=1, sticky='ns')
                    tree.config(yscrollcommand=sb.set)
                    a = tree.item(tree.focus())['values']

                    btn = tk.Button(log, text='Close', command=out,
                                    width=20, bd=2, fg='red',font=font_text)
                    btn.grid(row=2, column=0, columnspan=2, sticky=E+W)
                    status = Label(log,text=f'Total records fetched: {len(recs)}',bd=1,relief=SUNKEN,anchor=W)
                    status.grid(row=1,columnspan=2,sticky=E+W)
                    con.close()
                    e_sch.delete(0,END)

    def out():
        pygame.mixer.music.load('audio/main open.mp3')
        pygame.mixer.music.play()
        time.sleep(0.3)
        master.destroy()

    def key_pressed(event):
        pygame.mixer.music.load('audio/type.mp3')
        pygame.mixer.music.play()

    def clicker(event):
        pygame.mixer.music.load('audio/click.mp3')
        pygame.mixer.music.play()

    l = Label(master, text='Search Visitors',
              font=Font(family='helvetica', size='20'))
    l2 = Label(master, text='Enter', font=font_text)
    l3 = Label(master, text='NOTE: Enter date only in yyyy-mm-dd format ',
               font=font_text, fg='red')
    btn_log = Button(master, text='Show', font=font_text, command=dbase)
    btn_ext = Button(master, text='Close', font=font_text,
                     command=out, fg='red')
    l.grid(row=0, columnspan=3, pady=20, padx=20)
    l2.grid(row=2, column=0, pady=20, padx=20)
    l3.grid(row=3, column=0, pady=20, padx=20, columnspan=3, sticky=E+W)
    btn_log.grid(row=4, columnspan=3, sticky=E+W, pady=(20, 0), ipadx=200)
    btn_ext.grid(row=5, columnspan=3, sticky=E+W, ipadx=200)
    drop.grid(row=1, column=0, columnspan=3, pady=20, padx=20, ipady=5)
    e_sch.grid(row=2, column=1, pady=20, padx=20, ipady=5)
    e_sch.bind_all('<Key>',key_pressed)
    e_sch.bind_all('<Return>',dbase)
    btn_log.bind('<Button-1>',clicker) 
    e_sch.focus_force()

    # Creating ? icons
    q_mark = Image.open('images/question_mark.png')
    q_mark_re = q_mark.resize((15, 15), Image.ANTIALIAS)
    q_mark_new = ImageTk.PhotoImage(q_mark_re)

    q_mark_1 = Label(master, image=q_mark_new)
    q_mark_1.grid(row=1, column=2, padx=(0, 10),sticky=W)
    q_mark_2 = Label(master, image=q_mark_new)
    q_mark_2.grid(row=2, column=2, padx=(0, 10),sticky=W)

    # Creating a tooltip for each ? icon
    nametooltip_1 = Pmw.Balloon(master)
    nametooltip_1.bind(q_mark_1, 'Select by:\nChoose how you want to search for visitors')
    nametooltip_2 = Pmw.Balloon(master)
    nametooltip_2.bind(q_mark_2, 'Book:\nEnter the corresponding information of the visitor or the book borrowed\nMake sure to enter date in yyyy-mm-dd format if chosen')

# Function to return the book
def return_b():
    
    global q_mark_new
    returner = Toplevel(root)
    returner.title('Return a book')
    returner.focus_force()
    returner.iconbitmap('images/retbor.ico')    
    returner.geometry('+700+200')
    returner.resizable(False,False)
    Pmw.initialise(returner)
    pygame.mixer.music.load('audio/pop_open.mp3')
    pygame.mixer.music.play()

    def dates():
        global cal
        global a

        def date():
            global cal
            a = cal.selection_get()

        top = Toplevel(root)
        top.iconbitmap('images/calendar.ico')
        top.title('Choose Date')
        cal = Calendar(top, font="Arial 14", selectmode='day', year=int(datetime.datetime.now().strftime(
            "%Y")), month=int(datetime.datetime.now().strftime("%m")), day=int(datetime.datetime.now().strftime("%d")))
        cal.pack(fill="both", expand=True)
        Button(top, text="OK", command=top.destroy,
               font=font_text).pack(fill='both')

    def dbase():
        a = drop.get()

        if a == 'Select by....':
            messagebox.showerror(
                'No choice given', 'Please choose a valid option to select by....',parent=returner)
            returner.focus_force()

        elif a == 'Sl.no.':
            
            if e_sch.get() == '' or e_bok.get() == '':
                messagebox.showerror('Fill all the blanks','Make sure to fill in all the blanks',parent=returner)
                returner.focus_force()

            else:
                try:
                    # Searching book details
                    con = mysql.connect(host='', user='',
                                        password='', database='')
                    c = con.cursor()
                    sql_command_6 = "SELECT * FROM books where `sl.no.` = %s;"
                    values_6 = (e_bok.get(),)
                    c.execute(sql_command_6,values_6)
                    rec = c.fetchall()
                    b = rec[0][1]
                    accession = rec[0][3]

                    # Getting records of borrower
                    sql_command_7 = 'SELECT * FROM borrow where `Accession no. of book` = %s ORDER BY `sl.no.` DESC LIMIT 1;'
                    values_7 = (accession,)
                    c.execute(sql_command_7,values_7)
                    records = c.fetchall()
                    status = records[0][8]
                    title = records[0][3]
                    s_id = records[0][1]

                    if status == 'Borrowing' and s_id == e_sch.get():
                        
                        choice = messagebox.askyesno('Are you sure',f'Are you sure you want to return {title} taken by ID: {s_id}',parent=returner)
                        returner.focus_force()

                        if choice == 1:
                            try:
                                sql_command_8 = 'UPDATE borrow set `status`="Returned",`date returned`=%s WHERE `STUDENT ID`=%s and `Accession no. of book`=%s ORDER BY `Sl.no.` DESC LIMIT 1;'
                                values_8 = str(cal.selection_get()),e_sch.get(),accession
                                c.execute(sql_command_8,values_8)
                                c.execute('commit')
                                con.close()
                                messagebox.showinfo(
                                    'Success', f"'{title}' has been returned successfully",parent=returner)
                                returner.focus_force()
                                con = mysql.connect(host='', user='',
                                                    password='', database='')
                                c = con.cursor()
                                sql_command_9 = 'UPDATE books set `availability`="Yes" WHERE `Accession no.`=%s;'
                                values_9 = (accession,)
                                c.execute(sql_command_9,values_9)
                                c.execute('commit')
                                con.close()
                                e_sch.delete(0, END)
                                e_bok.delete(0, END)
                                drop.current(0)
                            
                            except NameError:
                                messagebox.showerror('Choose the date','Make sure to choose the date of returning',parent=returner)
                                returner.focus_force()

                        else:
                            returner.focus_force()

                    else:
                        messagebox.showerror(
                            'Error', f'No such book is being borrowed by ID: {e_sch.get()}',parent=returner)
                        returner.focus_force()

                except IndexError:
                    messagebox.showerror(
                        'Error', f'No such book is being borrowed by ID: {e_sch.get()}',parent=returner)
                    returner.focus_force()

        elif a == 'Accession no.':
            
            if e_sch.get() == '' or e_bok.get() == '':
                messagebox.showerror('Fill all the blanks','Make sure to fill in all the blanks',parent=returner)
                returner.focus_force()

            else:
                try:
                    # Searching book details
                    con = mysql.connect(host='', user='',
                                        password='', database='')
                    c = con.cursor()
                    sql_command_10 = "SELECT * FROM books where `Accession no.` = %s;"
                    values_10 = (e_bok.get(),)
                    c.execute(sql_command_10,values_10)
                    rec = c.fetchall()
                    b = rec[0][1]
                    accession = rec[0][3]
                    
                    # Getting records of borrower
                    sql_command_11 = 'SELECT * FROM borrow where `Accession no. of book` = %s ORDER BY `sl.no.` DESC LIMIT 1;'
                    values_11 = (accession,)
                    c.execute(sql_command_11,values_11)
                    records = c.fetchall()
                    status = records[0][8]
                    title = records[0][3]
                    s_id = records[0][1]

                    if status == 'Borrowing' and s_id == e_sch.get():
                        
                        choice = messagebox.askyesno('Are you sure',f'Are you sure you want to return {title} taken by ID: {s_id}',parent=returner)
                        returner.focus_force()

                        if choice == 1:
                            try:
                                sql_command_12 = 'UPDATE borrow set `status`="Returned",`date returned`=%s WHERE `STUDENT ID`=%s and `Accession no. of book`=%s ORDER BY `Sl.no.` DESC LIMIT 1;'
                                values_12 = str(cal.selection_get()),e_sch.get(),accession
                                c.execute(sql_command_12,values_12)
                                c.execute('commit')
                                con.close()
                                messagebox.showinfo(
                                    'Success', f'"{title}" has been returned successfully',parent=returner)
                                returner.focus_force()
                                con = mysql.connect(host='', user='',
                                                    password='', database='')
                                c = con.cursor()
                                sql_command_13 = 'UPDATE books set `availability`="Yes" WHERE `Accession no.`=%s;'
                                values_13 = (accession,)
                                c.execute(sql_command_13,values_13)
                                c.execute('commit')
                                con.close()
                                e_sch.delete(0, END)
                                e_bok.delete(0, END)
                                drop.current(0)
                            
                            except NameError:
                                messagebox.showerror('Choose the date','Make sure to choose the date of returning',parent=returner)
                                returner.focus_force()

                        else:
                            returner.focus_force()

                    else:
                        messagebox.showinfo(
                            'Error', f'No such book is being borrowed by ID: {e_sch.get()}',parent=returner)
                        returner.focus_force()

                except IndexError:
                    messagebox.showinfo(
                        'Error', f'No such book is being borrowed by ID: {e_sch.get()}',parent=returner)
                    returner.focus_force()

    def out():
        pygame.mixer.music.load('audio/main open.mp3')
        pygame.mixer.music.play()
        time.sleep(0.3)
        returner.destroy()

    def key_pressed(event):
        pygame.mixer.music.load('audio/type.mp3')
        pygame.mixer.music.play()

    def clicker(event):
        pygame.mixer.music.load('audio/click.mp3')
        pygame.mixer.music.play()

    drop = ttk.Combobox(
        returner, value=['Select by....', 'Sl.no.', 'Accession no.'], state='readonly')
    drop.current(0)
    l0 = Label(returner, text='Return a book',
               font=Font(family='helvetica', size='20'))
    l1 = Label(returner, text='Student ID', font=font_text)
    e_sch = Entry(returner)
    l2 = Label(returner, text='Choose Date of Returning', font=font_text)
    l3 = Label(returner, text='Enter', font=font_text)
    e_bok = Entry(returner)
    b_cal = Button(returner, text='Choose Date', command=dates, font=font_text)
    b_ret = Button(returner, text='Return book', command=dbase, font=font_text)
    b_ext = Button(returner, text='Close',
                   command=out, font=font_text)

    l0.grid(row=0, columnspan=3, pady=20)
    l1.grid(row=1, column=0, padx=30, pady=(10, 0), sticky=W)
    e_sch.grid(row=1, column=1, padx=30, ipady=5, pady=(10, 0))
    l2.grid(row=4, column=0, padx=30, sticky=W)
    drop.grid(row=2, columnspan=3, pady=20, ipadx=10, ipady=5)
    l3.grid(row=3, column=0, padx=30, sticky=W)
    e_bok.grid(row=3, column=1, padx=30, ipady=5, pady=10)
    b_cal.grid(row=4, column=1, ipadx=16, pady=10)
    b_ret.grid(row=6, columnspan=2, sticky=E+W, padx=30, pady=10)
    b_ext.grid(row=7, columnspan=2, sticky=E+W, padx=30, pady=10)
    e_sch.bind_all('<Key>',key_pressed)
    e_bok.bind_all('<Key>',key_pressed)
    b_ret.bind('<Button-1>',clicker)

    # Creating ? icon
    q_mark = Image.open('images/question_mark.png')
    q_mark_re = q_mark.resize((15, 15), Image.ANTIALIAS)
    q_mark_new = ImageTk.PhotoImage(q_mark_re)

    q_mark_1 = Label(returner, image=q_mark_new)
    q_mark_1.grid(row=1, column=2, padx=(0, 10))
    q_mark_2 = Label(returner, image=q_mark_new)
    q_mark_2.grid(row=2, column=2, padx=(0, 10))
    q_mark_3 = Label(returner, image=q_mark_new)
    q_mark_3.grid(row=3, column=2, padx=(0, 10))
    q_mark_4 = Label(returner, image=q_mark_new)
    q_mark_4.grid(row=4, column=2, padx=(0, 10))
    q_mark_5 = Label(returner, image=q_mark_new)
    q_mark_5.grid(row=6, column=2, padx=(0, 10))
    
    # Creating a tooltip for each ? icon
    nametooltip_1 = Pmw.Balloon(returner)
    nametooltip_1.bind(q_mark_1, "Student ID:\nEnter your valid student ID")
    nametooltip_2 = Pmw.Balloon(returner)
    nametooltip_2.bind(q_mark_2, 'Select by:\nChoose how you want to select your book')
    nametooltip_3 = Pmw.Balloon(returner)
    nametooltip_3.bind(q_mark_3, 'Book:\nEnter the corresponding information of the book')
    nametooltip_4 = Pmw.Balloon(returner)
    nametooltip_4.bind(q_mark_4, 'Date of returning:\nClick to choose the date of returning')
    nametooltip_5 = Pmw.Balloon(returner)
    nametooltip_5.bind(q_mark_5, 'Return Book:\nClick to return the book')

# Function to borrow the book
def borrow():
    global q_mark_new
    borrower = Toplevel(root)
    Pmw.initialise(borrower)
    borrower.title('Borrow a book')
    borrower.iconbitmap('images/retbor.ico')
    borrower.resizable(False,False)
    borrower.geometry('+600+200')
    borrower.focus_force()
    pygame.mixer.music.load('audio/pop_open.mp3')
    pygame.mixer.music.play()

    def dbase(): 
        a = drop.get()

        if a == 'Select by....':
            messagebox.showerror(
                'No choice given', 'Please choose a valid option to select by....',parent=borrower)
            borrower.focus_force()

        elif a == 'Sl.no.':
            if e_bok.get() == '' or e_nme.get() == '' or e_sch.get() == '':
                messagebox.showerror('Fill all the blanks','Make sure to fill in all the blanks',parent=borrower)
                borrower.focus_force()
            
            else:
                if int(e_bok.get()) > 5563:
                    messagebox.showerror('Book does not exist',
                                        'Sorry, no such book is found here',parent=borrower)
                    borrower.focus_force()

                else:
                    con = mysql.connect(host='', user='',
                                        password='', database='')
                    c = con.cursor()
                    sql_command_14 = "SELECT * FROM books where `Sl.no.` = %s;"
                    values_14 = (e_bok.get(),)
                    c.execute(sql_command_14,values_14)
                    rec = c.fetchall()
                    avail = rec[0][5]
                    b = rec[0][1]
                    accession = rec[0][3]

                    if avail == 'No':
                        sql_command_15 = "SELECT `Due Date` FROM borrow where `Accession no. of book` = %s;"
                        values_15 = (accession,)
                        c.execute(sql_command_15,values_15)
                        recs = c.fetchall()
                        dateb = recs[0][0]
                        new_date = dt.strptime(dateb, '%Y-%m-%d')
                        messagebox.showerror(
                            'Book Taken', f'Sorry, the book has already been taken. It will be returned back on {new_date.strftime("%A, %d %b %Y")}',parent=borrower)
                        borrower.focus_force()

                    else:
                        try:
                            date_1 = cal.selection_get()
                            date_2 = cals.selection_get()                            
                            choice = messagebox.askyesno('Are you sure',f'Are you sure you want to borrow "{b}" to {e_nme.get()} till {date_2}',parent=borrower)
                            
                            if choice == 1:
                                con = mysql.connect(host='', user='',
                                            password='', database='')
                                c = con.cursor()
                                sql_command_16 = "Insert into borrow(`STUDENT ID`,`STUDENT NAME`,`TITLE`,`Accession no. of book`,`DATE TAKEN`,`DUE DATE`,`STATUS`) VALUES(%s,%s,%s,%s,%s,%s,%s)"
                                values_16 = (e_sch.get(),e_nme.get(),b,str(accession),str(date_1),str(date_2),'Borrowing')
                                c.execute(sql_command_16,values_16)
                                c.execute('commit')
                                con.close()
                                messagebox.showinfo(
                                    'Success', f'"{b}" has been succesfully borrowed by {e_nme.get()}',parent=borrower)
                                borrower.focus_force()

                                con = mysql.connect(host='', user='',
                                                    password='', database='')
                                c = con.cursor()
                                sql_command_17 = "UPDATE books set `availability`= 'No' WHERE `sl.no.`=%s or `Accession no.`=%s;"
                                values_17 = (e_bok.get(),e_bok.get())
                                c.execute(sql_command_17,values_17)
                                c.execute('commit')
                                con.close()

                                e_sch.delete(0, END)
                                e_bok.delete(0, END)
                                e_nme.delete(0, END)
                                drop.current(0)
                            
                            else:
                                borrower.focus_force()
                        
                        except NameError:
                            messagebox.showerror('Choose the date','Make sure to choose the date of borrowing and due date',parent=borrower)
                            borrower.focus_force()
                        
        elif a == 'Accession no.':
            if e_bok.get() == '' or e_nme.get() == '' or e_sch.get() == '':
                messagebox.showerror('Fill all the blanks','Make sure to fill in all the blanks',parent=borrower)
                borrower.focus_force()
            
            else:
                con = mysql.connect(host='', user='',
                                    password='', database='')
                c = con.cursor()
                sql_command_18 = "SELECT `accession no.` FROM books;"
                c.execute(sql_command_18)
                records = c.fetchall()

                real_acc = []
                for nums in range(5553):
                    recs = records[nums][0]
                    real_acc.append(recs)

                if int(e_bok.get()) not in real_acc:
                    
                    messagebox.showerror(
                        'Does not exist', 'Sorry, such book does not exist. Please try someother book',parent=borrower)
                    borrower.focus_force()

                else:
                    con = mysql.connect(host='', user='',
                                        password='', database='')
                    c = con.cursor()
                    sql_command_19 = "SELECT * FROM books where `Accession no.` = %s;"
                    values_19 = (e_bok.get(),)
                    c.execute(sql_command_19,values_19)
                    rec = c.fetchall()
                    avail = rec[0][5]
                    b = rec[0][1]
                    accession = rec[0][3]

                    if avail == 'No':
                        sql_command_20 = "SELECT `Due Date` FROM borrow where `Accession no. of book` = %s;"
                        values_20 = (accession,)
                        c.execute(sql_command_20,values_20)
                        recs = c.fetchall()
                        c = recs[0][0]
                        new_date = dt.strptime(c, '%Y-%m-%d')
                        messagebox.showerror(
                            'Book Taken', f'Sorry, the book has already been taken. It will be returned back on {new_date.strftime("%A, %d %b %Y")}',parent=borrower)
                        borrower.focus_force()

                    else:
                        try:
                            date_1 = cal.selection_get()
                            date_2 = cals.selection_get()                            
                            choice = messagebox.askyesno('Are you sure',f'Are you sure you want to borrow "{b}" to {e_nme.get()} till {date_2}',parent=borrower)

                            if choice == 1:
                                sql_command_21 = "Insert into borrow(`STUDENT ID`,`STUDENT NAME`,`TITLE`,`Accession no. of book`,`DATE TAKEN`,`DUE DATE`,`STATUS`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                                values_21 = (e_sch.get(),e_nme.get(),b,str(accession),str(date_1),str(date_2),'Borrowing')
                                c.execute(sql_command_21,values_21)
                                c.execute('commit')
                                con.close()
                                messagebox.showinfo(
                                    'Success', f'"{b}" has been succesfully borrowed by {e_nme.get()}',parent=borrower)
                                borrower.focus_force()
                                con = mysql.connect(host='', user='',
                                                    password='', database='')
                                c = con.cursor()
                                sql_command_22 = "UPDATE books set `availability`= 'No' WHERE `Accession no.`=%s;"
                                values_22 = (e_bok.get(),)
                                c.execute(sql_command_22,values_22)
                                c.execute('commit')
                                con.close()

                                e_sch.delete(0, END)
                                e_bok.delete(0, END)
                                e_nme.delete(0, END)
                                drop.current(0)
                            
                            else:
                                borrower.focus_force()
                        
                        except NameError:
                            messagebox.showerror('Choose the date','Make sure to choose the date of borrowing and the due date',parent=borrower)
                            borrower.focus_force()
                        
    def dates():
        global cal
        global a

        def date():
            global cal
            a = cal.selection_get()

        top = Toplevel(root)
        top.iconbitmap('images/calendar.ico')
        top.title('Choose Date')
        cal = Calendar(top, font="Arial 14", selectmode='day', year=int(datetime.datetime.now().strftime(
            "%Y")), month=int(datetime.datetime.now().strftime("%m")), day=int(datetime.datetime.now().strftime("%d")))
        cal.pack(fill="both", expand=True)
        Button(top, text="OK", command=top.destroy,
               font=font_text).pack(fill='both')

        l0.grid(row=0, columnspan=3, pady=20)

    def dates_2():
        global cals
        top = Toplevel(root)
        top.iconbitmap('images/calendar.ico')
        top.title('Choose Date')
        cals = Calendar(top, font="Arial 14", selectmode='day', year=int(datetime.datetime.now().strftime(
            "%Y")), month=int(datetime.datetime.now().strftime("%m")), day=int(datetime.datetime.now().strftime("%d")))
        cals.pack(fill="both", expand=True)
        Button(top, text="OK", command=top.destroy,
               font=font_text).pack(fill='both')

        l0.grid(row=0, columnspan=3, pady=20)

    def out():
        pygame.mixer.music.load('audio/main open.mp3')
        pygame.mixer.music.play()
        time.sleep(0.3)
        borrower.destroy()

    def key_pressed(event):
        pygame.mixer.music.load('audio/type.mp3')
        pygame.mixer.music.play()

    def clicker(event):
        pygame.mixer.music.load('audio/click.mp3')
        pygame.mixer.music.play()

    drop = ttk.Combobox(
        borrower, value=['Select by....', 'Sl.no.', 'Accession no.'], state='readonly')
    drop.current(0)
    l0 = Label(borrower, text='Borrow a book',
               font=Font(family='helvetica', size='20'))
    l1 = Label(borrower, text='Student ID', font=font_text)
    l4 = Label(borrower, text='Student Name', font=font_text)
    e_sch = Entry(borrower)
    e_nme = Entry(borrower)
    l2 = Label(borrower, text='Enter', font=font_text)
    e_bok = Entry(borrower)
    b_giv = Button(borrower, text='Give book', command=dbase, font=font_text)
    b_ext = Button(borrower, text='Close',
                   command=out, font=font_text)
    l3 = Label(borrower, text='Choose Date of Borrowing', font=font_text)
    l5 = Label(borrower, text='Choose Due Date', font=font_text)
    b_cal = Button(borrower, text='Choose Date', command=dates, font=font_text)
    b_cal_2 = Button(borrower, text='Choose Date',
                     command=dates_2, font=font_text)

    l5.grid(row=6, column=0, padx=30, sticky=W)
    b_cal_2.grid(row=6, column=1, ipadx=16, pady=10)
    drop.grid(row=3, columnspan=3, pady=20, ipadx=10, ipady=5)
    l0.grid(row=0, columnspan=3, pady=20)
    l1.grid(row=1, column=0, padx=30, sticky=W)
    e_sch.grid(row=1, column=1, padx=(30, 0), ipady=5)
    l2.grid(row=4, column=0, padx=30, sticky=W)
    e_bok.grid(row=4, column=1, padx=(30, 0), ipady=5)
    b_giv.grid(row=8, columnspan=2, sticky=E+W,padx=(20,0), pady=10)
    b_ext.grid(row=9, columnspan=2, sticky=E+W,padx=(20,0), pady=10)
    l3.grid(row=5, column=0, padx=30, sticky=W)
    b_cal.grid(row=5, column=1, ipadx=16, pady=10)
    l4.grid(row=2, column=0, padx=30, pady=10, sticky=W)
    e_nme.grid(row=2, column=1, padx=(30, 0), ipady=5)
    e_sch.bind_all('<Key>',key_pressed)
    e_nme.bind_all('<Key>',key_pressed)
    e_bok.bind_all('<Key>',key_pressed)
    b_giv.bind('<Button-1>',clicker)

    # Creating ? icons
    q_mark = Image.open('images/question_mark.png')
    q_mark_re = q_mark.resize((15, 15), Image.ANTIALIAS)
    q_mark_new = ImageTk.PhotoImage(q_mark_re)

    q_mark_1 = Label(borrower, image=q_mark_new)
    q_mark_1.grid(row=1, column=2, padx=10)
    q_mark_2 = Label(borrower, image=q_mark_new)
    q_mark_2.grid(row=2, column=2, padx=10)
    q_mark_3 = Label(borrower, image=q_mark_new)
    q_mark_3.grid(row=3, column=1, padx=10)
    q_mark_4 = Label(borrower, image=q_mark_new)
    q_mark_4.grid(row=4, column=2, padx=10)
    q_mark_5 = Label(borrower, image=q_mark_new)
    q_mark_5.grid(row=5, column=2, padx=10)
    q_mark_6 = Label(borrower, image=q_mark_new)
    q_mark_6.grid(row=6, column=2, padx=10)
    q_mark_7 = Label(borrower, image=q_mark_new)
    q_mark_7.grid(row=8, column=2, padx=10)

    # Creating a tooltip for each ? icon
    nametooltip_1 = Pmw.Balloon(borrower)
    nametooltip_1.bind(q_mark_1, "Student ID:\nEnter your valid student ID")
    nametooltip_2 = Pmw.Balloon(borrower)
    nametooltip_2.bind(q_mark_2, "Student Name:\nEnter your full name")
    nametooltip_3 = Pmw.Balloon(borrower)
    nametooltip_3.bind(q_mark_3, 'Select by:\nChoose how you want to select your book')
    nametooltip_4 = Pmw.Balloon(borrower)
    nametooltip_4.bind(q_mark_4, 'Book:\nEnter the corresponding information of the book')
    nametooltip_5 = Pmw.Balloon(borrower)
    nametooltip_5.bind(q_mark_5, 'Date of borrowing:\nClick to choose the date of borrowing ( today\'s date )')
    nametooltip_6 = Pmw.Balloon(borrower)
    nametooltip_6.bind(q_mark_6, 'Due Date:\nClick to choose the date of returning')
    nametooltip_7 = Pmw.Balloon(borrower)
    nametooltip_7.bind(q_mark_7, 'Give Book:\nClick to lend the book')

# Function to search the book
def search():
    global q_mark_new
    log = Toplevel(root)
    log.title('Search Book')
    log.resizable(False,False)
    log.iconbitmap('images/search.ico')
    log.focus_force()
    log.geometry('+150+150')
    pygame.mixer.music.load('audio/pop_open.mp3')
    pygame.mixer.music.play()

    def dbase(event=None):
        a = drop.get()

        if a == 'Search by....':
            messagebox.showerror(
                'No choice given', 'Please choose a valid option to search by....',parent=log)
            e_sch.focus_force()

        elif a == 'Sl.no.' or a == 'Accession no.':
            if e_sch.get() == '':
                messagebox.showerror(
                'No data enter', 'Please enter a data in the box to search',parent=log)
                log.focus_force()
            
            else:
                con = mysql.connect(host='', user='',
                                    password='', database='')
                c = con.cursor()
                sql_command_23 = 'SELECT * from books where `{}`=%s;'
                sql_command_23 = sql_command_23.format(a)
                values_23 = (e_sch.get(),)
                c.execute(sql_command_23,values_23)
                result = c.fetchall()

                if result == []:
                    messagebox.showerror(
                        'Book does not exist', 'No such books found, please try a different book',parent=log)
                    log.focus_force()

                else:
                    result_win = Toplevel(log)
                    result_win.title('Search result')
                    result_win.focus_force()
                    result_win.iconbitmap('images/booksearch.ico')
                    result_win.geometry('+150+200')
                    result_win.resizable(False,False)
                    pygame.mixer.music.load('audio/pop_open.mp3')
                    pygame.mixer.music.play()

                    def out():
                        pygame.mixer.music.load('audio/main open.mp3')
                        pygame.mixer.music.play()
                        time.sleep(0.3)
                        result_win.destroy()

                    index = 0
                    for index, x in enumerate(result):
                        num = 0
                        for y in x:
                            lookup_label = Label(result_win, text=y)
                            lookup_label.grid(row=index+1, column=num)
                            num += 1
                    con.close()
                    l1 = Label(result_win, text='Sl.No', font=font_text)
                    l2 = Label(result_win, text='Title', font=font_text)
                    l3 = Label(result_win, text='Authors', font=font_text)
                    l6 = Label(result_win, text='Accession Number', font=font_text)
                    l4 = Label(result_win, text='Subject', font=font_text)
                    l5 = Label(result_win, text='Availability', font=font_text)
                    btn_ext = Button(result_win, text='Exit', font=font_text,
                                    command=out, borderwidth=2, fg='#eb4d4b')

                    l1.grid(row=0, column=0, padx=20)
                    l2.grid(row=0, column=1, padx=20)
                    l3.grid(row=0, column=2, padx=20)
                    l6.grid(row=0, column=3, padx=50)
                    l4.grid(row=0, column=4, padx=20)
                    l5.grid(row=0, column=5, padx=20)
                    btn_ext.grid(row=index+2, columnspan=7, sticky=E+W)
                    e_sch.delete(0,END)

        elif a == 'Approximate Accession no.':
            if e_sch.get() == '':
                messagebox.showerror(
                'No data enter', 'Please enter a data in the box to search',parent=log)
                log.focus_force()
            
            else:
                con = mysql.connect(host='', user='',
                                    password='', database='')
                c = con.cursor()
                sql_command_32 = "SELECT * from books where `Accession no.` REGEXP %s;"
                values_32 = (e_sch.get(),)
                c.execute(sql_command_32,values_32)
                result = c.fetchall()

                if result == []:
                    messagebox.showerror(
                        'No such book', 'No such books found, please try a different book',parent=log)
                    log.focus_force()

                if len(result) > 20:
                    result_win = Toplevel(root)
                    result_win.title('View all Visitors')
                    result_win.focus_force()
                    result_win.iconbitmap('images/booksearch.ico')
                    result_win.geometry('+150+200')
                    result_win.resizable(False,False)
                    pygame.mixer.music.load('audio/pop_open.mp3')
                    pygame.mixer.music.play()

                    def out():
                        pygame.mixer.music.load('audio/main open.mp3')
                        pygame.mixer.music.play()
                        time.sleep(0.3)
                        result_win.destroy()

                    # setup treeview
                    columns = (('Sl.no', 80), ('Title of the book', 500),('Author', 300), ('Accession no.', 80),
                            ('Subject', 150),('Availability', 80))
                    tree = ttk.Treeview(result_win, height=20, columns=[
                                        x[0] for x in columns], show='headings')
                    tree.grid(row=0, column=0, sticky='news')

                    # setup columns attributes
                    for col, width in columns:
                        tree.heading(col, text=col)
                        tree.column(col, width=width, anchor=tk.CENTER)

                    # fetch data
                    con = mysql.connect(host='', user='',
                                        password='', database='')
                    c = con.cursor()
                    sql_command_33 = 'SELECT * FROM books where `Accession no.` REGEXP %s;'
                    values_33 = (e_sch.get(),)
                    c.execute(sql_command_33,values_33)

                    # populate data to treeview
                    for rec in c:
                        tree.insert('', 'end', value=rec)

                    def pop_menu(event):
                        global column
                        tree.identify_row(event.y)
                        column = tree.identify_column(event.x)
                        popup1.post(event.x_root,event.y_root)

                    def copy():
                        row_id = tree.selection()
                        column_no = column
                        select = tree.set(row_id,column_no)
                        log.clipboard_append(select)
                        log.update()
                        
                    popup1 = Menu(log,tearoff=0)
                    popup1.add_command(label='Copy',command=copy)

                    tree.bind('<Button-3>',pop_menu)

                    # scrollbar
                    sb = tk.Scrollbar(result_win, orient=tk.VERTICAL, command=tree.yview)
                    sb.grid(row=0, column=1, sticky='ns')
                    tree.config(yscrollcommand=sb.set)
                    a = tree.item(tree.focus())['values']

                    status = Label(result_win,text=f'Total records fetched: {len(result)}',bd=1,relief=SUNKEN,anchor=W)
                    status.grid(row=1,columnspan=2,sticky=E+W)
                    btn = tk.Button(result_win, text='Close', command=out,
                                    width=20, bd=2, fg='red',font=font_text)
                    btn.grid(row=2, column=0, columnspan=2, sticky=E+W)
                    con.close()
                    e_sch.delete(0,END)

                else:
                    result_win = Toplevel(log)
                    result_win.title('Search result')
                    result_win.focus_force()
                    result_win.iconbitmap('images/booksearch.ico')
                    result_win.geometry('+150+200')
                    result_win.resizable(False,False)
                    pygame.mixer.music.load('audio/pop_open.mp3')
                    pygame.mixer.music.play()

                    def out():
                        pygame.mixer.music.load('audio/main open.mp3')
                        pygame.mixer.music.play()
                        time.sleep(0.3)
                        result_win.destroy()

                    index = 0
                    for index, x in enumerate(result):
                        num = 0
                        for y in x:
                            lookup_label = Label(result_win, text=y)
                            lookup_label.grid(row=index+1, column=num)
                            num += 1
                    con.close()
                    l1 = Label(result_win, text='Sl.No', font=font_text)
                    l2 = Label(result_win, text='Title', font=font_text)
                    l3 = Label(result_win, text='Authors', font=font_text)
                    l6 = Label(result_win, text='Accession Number', font=font_text)
                    l4 = Label(result_win, text='Subject', font=font_text)
                    l5 = Label(result_win, text='Availablity', font=font_text)
                    btn_ext = Button(result_win, text='Exit', font=font_text,
                                    command=out, borderwidth=2, fg='#eb4d4b')
                    status = Label(result_win,text=f'Total records fetched: {len(result)}',bd=1,relief=SUNKEN,anchor=W)
                    
                    status.grid(row=index+2,columnspan=7,sticky=E+W)
                    l1.grid(row=0, column=0, padx=20)
                    l2.grid(row=0, column=1, padx=20)
                    l3.grid(row=0, column=2, padx=20)
                    l4.grid(row=0, column=4, padx=20)
                    l5.grid(row=0, column=5, padx=20)
                    l6.grid(row=0, column=3, padx=50)
                    btn_ext.grid(row=index+3, columnspan=7, sticky=E+W)
                    e_sch.delete(0,END)

        elif a == 'Approximate Sl.no.':
            if e_sch.get() == '':
                messagebox.showerror(
                'No data enter', 'Please enter a data in the box to search',parent=log)
                log.focus_force()
            
            else:
                con = mysql.connect(host='', user='',
                                    password='', database='')
                c = con.cursor()
                sql_command_34 = "SELECT * from books where `sl.no.` REGEXP %s;"
                values_34 = (e_sch.get(),)
                c.execute(sql_command_34,values_34)
                result = c.fetchall()

                if result == []:
                    messagebox.showerror(
                        'No such book', 'No such books found, please try a different book',parent=log)
                    log.focus_force()

                if len(result) > 20:
                    result_win = Toplevel(root)
                    result_win.title('View all Visitors')
                    result_win.focus_force()
                    result_win.iconbitmap('images/booksearch.ico')
                    result_win.geometry('+150+200')
                    result_win.resizable(False,False)
                    pygame.mixer.music.load('audio/pop_open.mp3')
                    pygame.mixer.music.play()

                    def out():
                        pygame.mixer.music.load('audio/main open.mp3')
                        pygame.mixer.music.play()
                        time.sleep(0.3)
                        result_win.destroy()

                    # setup treeview
                    columns = (('Sl.no', 80), ('Title of the book', 500),('Author', 300), ('Accession no.', 80),
                            ('Subject', 150),('Availability', 80))
                    tree = ttk.Treeview(result_win, height=20, columns=[
                                        x[0] for x in columns], show='headings')
                    tree.grid(row=0, column=0, sticky='news')

                    # setup columns attributes
                    for col, width in columns:
                        tree.heading(col, text=col)
                        tree.column(col, width=width, anchor=tk.CENTER)

                    # fetch data
                    con = mysql.connect(host='', user='',
                                        password='', database='')
                    c = con.cursor()
                    sql_command_35 = 'SELECT * FROM books where `sl.no.` REGEXP %s;'
                    values_35 = (e_sch.get(),)
                    c.execute(sql_command_35,values_35)

                    # populate data to treeview
                    for rec in c:
                        tree.insert('', 'end', value=rec)

                    def pop_menu(event):
                        global column
                        tree.identify_row(event.y)
                        column = tree.identify_column(event.x)
                        popup1.post(event.x_root,event.y_root)

                    def copy():
                        row_id = tree.selection()
                        column_no = column
                        select = tree.set(row_id,column_no)
                        log.clipboard_append(select)
                        log.update()
                        
                    popup1 = Menu(log,tearoff=0)
                    popup1.add_command(label='Copy',command=copy)

                    tree.bind('<Button-3>',pop_menu)

                    # scrollbar
                    sb = tk.Scrollbar(result_win, orient=tk.VERTICAL, command=tree.yview)
                    sb.grid(row=0, column=1, sticky='ns')
                    tree.config(yscrollcommand=sb.set)
                    a = tree.item(tree.focus())['values']

                    status = Label(result_win,text=f'Total records fetched: {len(result)}',bd=1,relief=SUNKEN,anchor=W)
                    status.grid(row=1,columnspan=2,sticky=E+W)
                    btn = tk.Button(result_win, text='Close', command=out,
                                    width=20, bd=2, fg='red',font=font_text)
                    btn.grid(row=2, column=0, columnspan=2, sticky=E+W)
                    con.close()
                    e_sch.delete(0,END)

                else:
                    result_win = Toplevel(log)
                    result_win.title('Search result')
                    result_win.focus_force()
                    result_win.iconbitmap('images/booksearch.ico')
                    result_win.geometry('+150+200')
                    result_win.resizable(False,False)
                    pygame.mixer.music.load('audio/pop_open.mp3')
                    pygame.mixer.music.play()

                    def out():
                        pygame.mixer.music.load('audio/main open.mp3')
                        pygame.mixer.music.play()
                        time.sleep(0.3)
                        result_win.destroy()

                    index = 0
                    for index, x in enumerate(result):
                        num = 0
                        for y in x:
                            lookup_label = Label(result_win, text=y)
                            lookup_label.grid(row=index+1, column=num)
                            num += 1
                    con.close()
                    l1 = Label(result_win, text='Sl.No', font=font_text)
                    l2 = Label(result_win, text='Title', font=font_text)
                    l3 = Label(result_win, text='Authors', font=font_text)
                    l6 = Label(result_win, text='Accession Number', font=font_text)
                    l4 = Label(result_win, text='Subject', font=font_text)
                    l5 = Label(result_win, text='Availablity', font=font_text)
                    btn_ext = Button(result_win, text='Exit', font=font_text,
                                    command=out, borderwidth=2, fg='#eb4d4b')
                    status = Label(result_win,text=f'Total records fetched: {len(result)}',bd=1,relief=SUNKEN,anchor=W)
                    
                    status.grid(row=index+2,columnspan=7,sticky=E+W)
                    l1.grid(row=0, column=0, padx=20)
                    l2.grid(row=0, column=1, padx=20)
                    l3.grid(row=0, column=2, padx=20)
                    l4.grid(row=0, column=4, padx=20)
                    l5.grid(row=0, column=5, padx=20)
                    l6.grid(row=0, column=3, padx=50)
                    btn_ext.grid(row=index+3, columnspan=7, sticky=E+W)
                    e_sch.delete(0,END)

        else:
            if e_sch.get() == '':
                messagebox.showerror(
                'No data enter', 'Please enter a data in the box to search',parent=log)
                log.focus_force()
            
            else:
                con = mysql.connect(host='', user='',
                                    password='', database='')
                c = con.cursor()
                sql_command_24 = "SELECT * from books where `{}` REGEXP %s;"
                sql_command_24 = sql_command_24.format(a)
                values_24 = (e_sch.get(),)
                c.execute(sql_command_24,values_24)
                result = c.fetchall()

                if result == []:
                    messagebox.showerror(
                        'No such book', 'No such books found, please try a different book',parent=log)
                    log.focus_force()

                if len(result) > 20:
                    result_win = Toplevel(root)
                    result_win.title('View all Visitors')
                    result_win.focus_force()
                    result_win.iconbitmap('images/booksearch.ico')
                    result_win.geometry('+150+200')
                    result_win.resizable(False,False)
                    pygame.mixer.music.load('audio/pop_open.mp3')
                    pygame.mixer.music.play()

                    def out():
                        pygame.mixer.music.load('audio/main open.mp3')
                        pygame.mixer.music.play()
                        time.sleep(0.3)
                        result_win.destroy()

                    # setup treeview
                    columns = (('Sl.no', 80), ('Title of the book', 500),('Author', 300), ('Accession no.', 80),
                            ('Subject', 150),('Availability', 80))
                    tree = ttk.Treeview(result_win, height=20, columns=[
                                        x[0] for x in columns], show='headings')
                    tree.grid(row=0, column=0, sticky='news')

                    # setup columns attributes
                    for col, width in columns:
                        tree.heading(col, text=col)
                        tree.column(col, width=width, anchor=tk.CENTER)

                    # fetch data
                    con = mysql.connect(host='', user='',
                                        password='', database='')
                    c = con.cursor()
                    sql_command_25 = 'SELECT * FROM books where `{}` REGEXP %s;'
                    sql_command_25 = sql_command_25.format(a)
                    values_25 = (e_sch.get(),)
                    c.execute(sql_command_25,values_25)

                    # populate data to treeview
                    for rec in c:
                        tree.insert('', 'end', value=rec)

                    def pop_menu(event):
                        global column
                        tree.identify_row(event.y)
                        column = tree.identify_column(event.x)
                        popup1.post(event.x_root,event.y_root)

                    def copy():
                        row_id = tree.selection()
                        column_no = column
                        select = tree.set(row_id,column_no)
                        log.clipboard_append(select)
                        log.update()
                        
                    popup1 = Menu(log,tearoff=0)
                    popup1.add_command(label='Copy',command=copy)

                    tree.bind('<Button-3>',pop_menu)

                    # scrollbar
                    sb = tk.Scrollbar(result_win, orient=tk.VERTICAL, command=tree.yview)
                    sb.grid(row=0, column=1, sticky='ns')
                    tree.config(yscrollcommand=sb.set)
                    a = tree.item(tree.focus())['values']

                    status = Label(result_win,text=f'Total records fetched: {len(result)}',bd=1,relief=SUNKEN,anchor=W)
                    status.grid(row=1,columnspan=2,sticky=E+W)
                    btn = tk.Button(result_win, text='Close', command=out,
                                    width=20, bd=2, fg='red',font=font_text)
                    btn.grid(row=2, column=0, columnspan=2, sticky=E+W)
                    con.close()
                    e_sch.delete(0,END)

                else:
                    result_win = Toplevel(log)
                    result_win.title('Search result')
                    result_win.focus_force()
                    result_win.iconbitmap('images/booksearch.ico')
                    result_win.geometry('+150+200')
                    result_win.resizable(False,False)
                    pygame.mixer.music.load('audio/pop_open.mp3')
                    pygame.mixer.music.play()

                    def out():
                        pygame.mixer.music.load('audio/main open.mp3')
                        pygame.mixer.music.play()
                        time.sleep(0.3)
                        result_win.destroy()

                    index = 0
                    for index, x in enumerate(result):
                        num = 0
                        for y in x:
                            lookup_label = Label(result_win, text=y)
                            lookup_label.grid(row=index+1, column=num)
                            num += 1
                    con.close()
                    l1 = Label(result_win, text='Sl.No', font=font_text)
                    l2 = Label(result_win, text='Title', font=font_text)
                    l3 = Label(result_win, text='Authors', font=font_text)
                    l6 = Label(result_win, text='Accession Number', font=font_text)
                    l4 = Label(result_win, text='Subject', font=font_text)
                    l5 = Label(result_win, text='Availablity', font=font_text)
                    btn_ext = Button(result_win, text='Exit', font=font_text,
                                    command=out, borderwidth=2, fg='#eb4d4b')
                    status = Label(result_win,text=f'Total records fetched: {len(result)}',bd=1,relief=SUNKEN,anchor=W)
                    
                    status.grid(row=index+2,columnspan=7,sticky=E+W)
                    l1.grid(row=0, column=0, padx=20)
                    l2.grid(row=0, column=1, padx=20)
                    l3.grid(row=0, column=2, padx=20)
                    l4.grid(row=0, column=4, padx=20)
                    l5.grid(row=0, column=5, padx=20)
                    l6.grid(row=0, column=3, padx=50)
                    btn_ext.grid(row=index+3, columnspan=7, sticky=E+W)
                    e_sch.delete(0,END)

    def out():
        pygame.mixer.music.load('audio/main open.mp3')
        pygame.mixer.music.play()
        time.sleep(0.3)
        log.destroy()

    def key_pressed(event):
        pygame.mixer.music.load('audio/type.mp3')
        pygame.mixer.music.play()

    def clicker(event):
        pygame.mixer.music.load('audio/click.mp3')
        pygame.mixer.music.play()

    global a
    l = Label(log, text='Search Book', font=Font(
        family='helvetica', size='20'))
    drop = ttk.Combobox(log, value=['Search by....', 'Sl.no.', 'Title of the book', 'Accession no.',
                                    'Approximate Accession no.','Approximate Sl.no.','Authors', 'Subject'], state='readonly')
    drop.current(0)
    l2 = Label(log, text='Enter', font=font_text)
    e_sch = Entry(log)
    b_sch = Button(log, text='Search', command=dbase, font=font_text)
    b_ext = Button(log, text='Close', command=out, font=font_text)
    a = drop.get()
    l.grid(row=0, columnspan=3, pady=20)
    drop.grid(row=1, column=0, columnspan=3, ipady=5)
    l2.grid(row=2, column=0, padx=(20, 0))
    e_sch.grid(row=2, column=1, ipady=5, pady=20)
    b_sch.grid(row=3, column=0, columnspan=3, ipadx=200, sticky=E+W)
    b_ext.grid(row=4, column=0, columnspan=3, sticky=E+W)
    e_sch.bind_all('<Key>',key_pressed)
    b_sch.bind('<Button-1>',clicker)
    e_sch.bind('<Return>',dbase)
    e_sch.focus_force()

    # Creating ? icons
    q_mark = Image.open('images/question_mark.png')
    q_mark_re = q_mark.resize((15, 15), Image.ANTIALIAS)
    q_mark_new = ImageTk.PhotoImage(q_mark_re)

    q_mark_1 = Label(log, image=q_mark_new)
    q_mark_1.grid(row=1, column=2, padx=(0, 10),sticky=W)
    q_mark_2 = Label(log, image=q_mark_new)
    q_mark_2.grid(row=2, column=2, padx=(0, 10),sticky=W)

    nametooltip_1 = Pmw.Balloon(log)
    nametooltip_1.bind(q_mark_1, 'Select by:\nChoose how you want to search for the book')
    nametooltip_2 = Pmw.Balloon(log)
    nametooltip_2.bind(q_mark_2, 'Book:\nEnter the corresponding information of the book')

# Function to pop-open about
def about():
    # Defining Urls
    url = "https://nihaalnz.herokuapp.com"
    url_2 = "https://github.com/nihaalnz/Library-App-python-tkinter"

    def openweb():
        webbrowser.open(url, new=1)

    def openweb_2():
        webbrowser.open(url_2, new=1)

    def out():
        pygame.mixer.music.load('audio/main open.mp3')
        pygame.mixer.music.play()
        time.sleep(0.3)
        about.destroy()

    # Define about section
    about = Toplevel(root)
    about.title('About')
    about.iconbitmap('images/moderator.ico')
    about.geometry('300x300+300+300')
    about.resizable(False,False)
    about.focus_force()
    pygame.mixer.music.load('audio/pop_open.mp3')
    pygame.mixer.music.play()

    # Making frames
    frame = LabelFrame(about, text='About this program', padx=5, pady=5)
    # Making frame items
    l_name = Label(frame, text='Created by Nihaal Nz')
    l_ver = Label(frame, text='Ver : 3.00')
    l_lic = Label(frame, text='Licensed under MIT')
    btn_sup = Button(frame, text='Website', command=openweb)
    btn_cod = Button(frame, text='Source Code', command=openweb_2)
    btn_cls = Button(frame, text='Close', command=out)
    #Placing in screen
    frame.grid(row=0, column=0, padx=70, pady=40)
    l_name.grid(row=0, column=0)
    l_ver.grid(row=1, column=0)
    l_lic.grid(row=2, column=0)
    btn_sup.grid(row=3, columnspan=2, sticky=E+W, pady=(5, 0))
    btn_cod.grid(row=4, columnspan=2, sticky=E+W, pady=5)
    btn_cls.grid(row=5, columnspan=2, sticky=E+W)

# Function to exit the program
def exits():
    selection = messagebox.askyesno('Exit', 'Are you sure you want to exit?',parent=root)

    if selection == 1:
        pygame.mixer.music.load('audio/main open.mp3')
        pygame.mixer.music.play()
        time.sleep(0.5)
        root.destroy()

    else:
        root.focus_force()


# Define menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add menu items
file_menu = Menu(my_menu,tearoff=0)
my_menu.add_cascade(label='Menu', menu=file_menu)
file_menu.add_command(label='Search', command=search)
file_menu.add_command(label='Borrow', command=borrow)
file_menu.add_command(label='Return', command=return_b)
file_menu.add_separator()
file_menu.add_command(label='Show all logs', command=all_logs)
file_menu.add_command(label='Search visitors', command=sp_logs)
file_menu.add_separator()
file_menu.add_command(label='About', command=about)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=exits)

# Heading
l = Label(root, text='Main Menu', font=Font(family='helvetica', size='20'))

# Making buttons
btn_brw = Button(root, text='Borrow', command=borrow, font=font_text)
btn_ret = Button(root, text='Return', command=return_b, font=font_text)
btn_sch = Button(root, text='Search', command=search, font=font_text)
btn_log = Button(root, text='Search Visitors', command=sp_logs, font=font_text)
btn_logs = Button(root, text='Show All Visitors',command=all_logs, font=font_text)
btn_ext = Button(root, text='Exit', command=exits, font=font_text, fg='red')

# Placing in screen
btn_brw.grid(column=1, row=1, pady=65, padx=30, ipadx=30)
btn_ret.grid(column=2, row=1, ipadx=30, padx=(0, 10))
btn_sch.grid(column=0, row=1, padx=(8, 0), ipadx=30)
btn_log.grid(columnspan=3, row=3, sticky=E+W, padx=1, ipady=1, pady=(0, 20))
btn_logs.grid(columnspan=3, row=2, sticky=E+W, padx=1, ipady=1)
btn_ext.grid(columnspan=3, row=4, sticky=E+W, padx=1, ipady=1)
l.grid(row=0, columnspan=3, pady=(20, 0))


# Ending program
root.mainloop()

