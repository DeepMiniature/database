from tkinter import *
import mysql.connector
import math
from tkinter import dialog
from PIL import ImageTk, Image
import random

# main window or first window
main_screen = Tk()
main_screen.title('Hello World')

# background image
bkrd_img = ImageTk.PhotoImage(Image.open(('background_soft.png'))) # rgb = 255,202,228
label_bkrd = Label(main_screen, image = bkrd_img).grid(row = 0, column = 0, rowspan = 700, columnspan = 1400)

# main heading
label_heading = Label(main_screen, text = 'WELCOME TO THE SUPER MARKET', font = ('revive ov',16)).grid(row = 50, column = 0, columnspan = 1400)

# creating link to the 'super_market' database with the program
db = mysql.connector.connect(host = 'localhost', username = 'root', password = 'deep', database = 'cic')

# stting up a cursor to perform task in database
db_cur = db.cursor()

# showing tables of "super_market" database
db_cur.execute('show tables')
tables = db_cur.fetchall()
l_name = Label(main_screen, text = 'Tables in the Database are :',justify = LEFT, font = ('revive ov', 15)).grid(row = 120, column = 35)
v_row = 100
run = False

for i in tables:
    if v_row % 2 == 0:
        l_tab = Label(main_screen, text = i, font = ('revive ov', 14)).grid(row = 150, column = v_row)
    else:
        l_tab = Label(main_screen, text=i, font=('revive ov', 14)).grid(row = 180, column= v_row-25)
    v_row += 25

# asking for table name to open
l_ask = Label(main_screen, text = 'Which table do you want to use :',justify = LEFT, font = ('revive ov', 14)).grid(row = 230, column = 35, padx = 10)
e_ask = Entry(main_screen, font = ('revive ov', 14))
e_ask.grid(row = 230, column = 150, padx = 10)

def next_page():
    global db, db_cur, rt, go,row1, count,tuple_no ,data , table_data_type, primary, run, deep_ent, table_column, row_tab, ask_entry, table_col, data_type, ent_crit, ent_col, ent_tname, names_column, types_column, col_nent, col_tent, statement
    deep = Toplevel()
    deep.title('Auro in '+e_ask.get())
    l_deep_bkrd = Label(deep, image = bkrd_img).grid(row = 0, column = 0, rowspan = 700, columnspan = 1400)
    select = rt.get()

    if select == 1:
        deep_heading = Label(deep, text = "Here You Can Add A Data In '"+e_ask.get()+"' Table", font = ('revive ov', 16))
        deep_heading.grid(row = 30, column = 0, columnspan = 1400, pady = 10)
        db_cur.execute('desc '+e_ask.get())
        table_type = db_cur.fetchall()

        def add_record():
            global db, db_cur, table_column, deep_ent, count, table_data_type, row_tab
            add = ''

            for j in range(count-1):

                if table_data_type[j][0:3] == 'int' or table_data_type[j][0:3] == 'big':
                    add += str(deep_ent[j].get())+','

                elif table_data_type[j][0:3] == 'var' or table_data_type[j][0:3] == 'dat':
                    add += "'"+str(deep_ent[j].get())+"',"

            if table_data_type[-1][0:3] == 'int' or table_data_type[-1][0:3] == 'big':
                add += str(deep_ent[-1].get())

            elif table_data_type[-1][0:3] == 'var' or table_data_type[-1][0:3] == 'dat':
                add += "'"+str(deep_ent[-1].get())+"'"

            db_cur.execute("insert into "+e_ask.get()+" values("+add+")")
            db.commit()
            add_record_lab = Label(deep, text = 'Record Added', font = ('revive ov', 14)).grid(row =row_tab, column = 200)

        table_column = []
        table_data_type = []
        deep_ent = []
        row_tab = 100

        for i in table_type:

            table_column.append(i[0])
            table_data_type.append(i[1])

        count = len(table_column)

        for j in range(count):

            deep_ent.append('deep_ent'+str(j))
            deep_lab = Label(deep, text = 'Give the value to store in column '+table_column[j]+' ('+table_data_type[j]+') :', font = ('revive ov',15))
            deep_lab.grid(row = row_tab, column = 30, padx = 15)
            deep_ent[j] = Entry(deep, font = ('revive ov', 15))
            deep_ent[j].grid(row = row_tab, column = 200, padx = 5)
            row_tab += 50

        deep_submit_button = Button(deep, text = 'Add Given Record', font = ('cooper black', 12), command = add_record)
        deep_submit_button.grid(row = row_tab-50, column = 300, padx = 15)

    elif select == 2:

        deep_heading = Label(deep, text='Here You Can Check A Data In ' + e_ask.get() + ' Table', font=('revive ov', 16))
        deep_heading.grid(row = 30, column = 0, columnspan = 1400)
        db_cur.execute('desc ' + e_ask.get())
        table_type = db_cur.fetchall()
        table_col = []
        data_type = []
        deep_column = Label(deep, text='Columns in the table  are as follows :', font=('revive ov', 15)).grid(row=100, column=30, padx=10)
        k = (100, 130)
        j = 150

        for i in table_type:
            table_col.append(i[0])
            data_type.append(i[1])

            if j % 2 == 0:
                deep_fields = Label(deep, text=i[0], font=('revive ov', 15)).grid(row=k[0], column=j)

            else:
                deep_fields = Label(deep, text=i[0], font=('revive ov', 15)).grid(row=k[1], column=j - 35)

            j += 35

        def check_table():
            global db, db_cur, ask_entry, table_col, data_type, ent_crit, ent_col, e_ask
            deep1 = Toplevel()
            deep1.title('Required Data')
            deep1_bkrd = Label(deep1, image = bkrd_img).grid(row = 0, column = 0, rowspan = 700, columnspan = 1400)
            deep1_main = Label(deep1, text = 'Data You Want To See Is Here', font = ('revive ov',16)).grid(row = 50 , column = 0, columnspan = 1400)
            k_col = 0

            for i in table_col:

                if i == str(ask_entry.get()):

                    if data_type[k_col][0:3] == 'var' :
                        db_cur.execute("select "+str(ent_col.get())+" from "+str(e_ask.get())+" where "+str(ask_entry.get())+" like '%"+str(ent_crit.get())+"%'")

                    elif data_type[k_col][0:3] == 'int':
                        db_cur.execute('select ' + str(ent_col.get()) + ' from ' + str(e_ask.get()) + ' where ' + str(ask_entry.get()) + str(ent_crit.get()))

                k_col += 1

            result = db_cur.fetchall()
            num_result = len(result[0])
            row_val = 50

            for i in result:
                row_val += 50
                col_val = 70

                for j in range(num_result):
                    lab_show = Label(deep1, text = i[j], font = ('revive ov', 15)).grid(row = row_val, column = col_val*(j+1))

        ask_lab = Label(deep, text = 'On basis of which column do you want to check :', font = ('revive ov',15)).grid(row = 170, column = 30, padx = 20)
        ask_entry = Entry(deep, font = ('revive ov', 15))
        ask_entry.grid(row = 170, column = 220)
        lab_crit = Label(deep, text='Write the condition to check(eg.deep,<10,=100..) :', font=('revive ov', 15)).grid(row=220, column=30, padx=20)
        ent_crit = Entry(deep, font=('revive ov', 15))
        ent_crit.grid(row=220, column=220)
        lab_col = Label(deep, text = 'Write the columns you want to check(eg.<Column1>,<Column2>,..:', font = ('revive ov',15)).grid(row = 270, column = 30, padx = 20)
        ent_col = Entry(deep, font = ('revive ov', 15))
        ent_col.grid(row = 270, column = 220)
        note_lab = Label(deep, text = 'Note: for seeing all columns type " * " in the space given', font = ('arial', 14)).grid(row = 300, column = 30, padx = 20)
        ask_button = Button(deep, text = 'NEXT', font = ('cooper black', 12), command = check_table)
        ask_button.grid(row = 270, column = 390)

    elif select == 3:
        deep_heading = Label(deep, text='Here You Can See All Data In ' + e_ask.get() + ' Table', font=('revive ov', 16))
        deep_heading.grid(row = 30, column = 0, columnspan = 1400, pady = 10)
        db_cur.execute('desc '+str(e_ask.get()))
        result = db_cur.fetchall()
        tab_col = []

        for i in result:
            tab_col.append(i[0])

        for j in range(len(tab_col)):
            name_col = Label(deep, text = tab_col[j], font = ('revive ov', 15), width = 20, padx = 5).grid(row = 100, column = (j+1)*100)

        db_cur.execute('select * from '+str(e_ask.get()))
        data = db_cur.fetchall()
        row1 = 150
        tuple_no = 1

        def show_data():
            global db, db_cur, data, tuple_no, row1

            def next():
                global db, db_cur, data, tuple_no, row1
                print(tuple_no)
                total_data = len(data)
                page = (total_data//10) + 1
                last = total_data%10
                if ((tuple_no+10-last) // 10) < page:

                    row1 = 150
                    if (tuple_no//10) == page-1:
                        for j in range(last):
                            for i in range(len(data[0])):
                                label = Label(deep, text = data[tuple_no-1][i], font = ('revive ov', 14),width =20, padx = 5).grid(row = row1, column = (i+1)*100)
                            tuple_no += 1
                            row1 += 30
                        for j in range(10-last):
                            for i in range(len(data[0])):
                                label = Label(deep, text = '', font = ('revive ov', 14),width =20, padx = 5).grid(row = row1, column = (i+1)*100)
                            row1 += 30
                    else:
                        for j in range(10):
                            for i in range(len(data[0])):
                                label = Label(deep, text = data[tuple_no-1][i], font = ('revive ov', 14), width =20, padx = 5).grid(row = row1, column = (i+1)*100)
                            tuple_no += 1
                            row1 += 30


            def previous():
                global db, db_cur, data, tuple_no, row1
                print(tuple_no)
                total_data = len(data)
                page = (total_data // 10) + 1
                last = total_data % 10
                if (tuple_no // 10) >= 1 and (tuple_no % 10) != 0:
                    row1 = 150
                    if tuple_no//10==(page-1) and (tuple_no % 10) != 1:
                        tuple_no -= (10+last)
                    else:
                        tuple_no -= 20
                    for j in range(10):
                        for i in range(len(data[0])):
                            label = Label(deep, text = data[tuple_no-1][i], font = ('revive ov',14), width = 20, padx = 5).grid(row = row1, column = (i+1)*100)
                        tuple_no += 1
                        row1 +=30

            previous_button = Button(deep, text = '<--Previous', font = ('cooper black', 12), command = previous)
            previous_button.grid(row = 50, column = 100)
            next_button = Button(deep, text = 'Next-->', font = ('cooper black', 12), command = next)
            next_button.grid(row = 50, column = 300)

            for j in data:
                if tuple_no<11:
                    for i in range(len(tab_col)):
                        lab_data = Label(deep, text=j[i], font=('revive ov', 14), width = 20, padx = 5).grid(row=row1, column=(i + 1) * 100)
                    tuple_no += 1
                    row1 += 30

        show_button = Button(deep, text = 'Show', font = ('cooper black', 12), command = show_data)
        show_button.grid(row = 50, column = 900)

    elif select == 4:

        deep.geometry('1400x700')
        deep_bkrd = Label(deep, image = bkrd_img).grid(row = 701, column = 0, rowspan = 700, columnspan =1400)
        deep_heading = Label(deep, text = 'Here You Can Create A New Table', font = ('revive ov', 16)).grid(row = 50, column = 0, columnspan = 1400, pady =10)
        Lab_tab_name = Label(deep, text = 'Give name of the new TABLE :', font = ('revive ov', 15)).grid(row = 120, column = 30, padx = 10)
        ent_tname = Entry(deep, font = ('revive ov', 15))
        ent_tname.grid(row = 120, column = 200)

        def show_column():
            global db, db_cur, ent_tname, names_column, types_column, col_nent, col_tent, primary, run, go
            add_column()
            col_name = Label(deep, text='Give name of Column(use only letters and "_") :', font=('revive ov', 15)).grid(row=170, column=30,padx=10)
            col_nent = Entry(deep, font=('revive ov', 15))
            col_nent.grid(row=170, column=200)
            col_type = Label(deep, text='Give type of Column(eg.int, varchar, date..) :', font=('revive ov', 15)).grid(row=220, column=30,padx=10)
            col_tent = Entry(deep, font=('revive ov', 15))
            col_tent.grid(row=220, column=200)
            primary = IntVar()
            primary.set(0)
            primary_check = Radiobutton(deep, text = 'PRIMARY KEY', font = ('revive ov', 14), variable = primary, value = 1)
            primary_check.grid(row = 170, column = 300)
            go = primary
            run = True


        def create():
            global db, db_cur, ent_tname, names_column, types_column, col_nent, col_tent, statement
            final1 = ''
            print(names_column)
            print(types_column)
            for i in range(len(names_column)-1):
                final1 = final1 + names_column[i] + ' ' + types_column[i] + ','
            final1 = final1 + names_column[-1] + ' ' + types_column[-1]
            final = statement + ent_tname.get() + '(' + final1 + ')'
            print(final)
            db_cur.execute(final)
            db.commit()
            lab_tab_created = Label(deep, text = 'Table Created', font = ('revive ov', 15)).grid(row = 270, column = 200)

        def add_column():
            global db, db_cur, ent_tname, names_column, types_column, col_nent, col_tent, primary, run, go
            print('haap')
            if run == True:
                go = primary.get()
                print(go)
                if go == 1:
                    types_column.append(col_tent.get()+' primary key')
                else:
                    types_column.append(col_tent.get())
                names_column.append(col_nent.get())

        names_column = []
        types_column = []
        add_button = Button(deep, text = 'Add Column', font = ('cooper black', 12), command = show_column)
        add_button.grid(row = 120, column = 300)
        create_button = Button(deep, text = 'Create Table', font = ('cooper black', 12), command = create)
        create_button.grid(row = 220, column = 300)
        statement = 'create table '



# activity to perform in database
l_activity = Label(main_screen, text = 'What do you want to do with table:',justify = LEFT, font = ('revive ov', 14)).grid(row = 280, column = 35, padx = 20)
rt = IntVar()
rt.set(0)
r1 = Radiobutton(main_screen, text = 'Add a data', font = ('revive ov', 14), variable = rt, value = 1)
r2 = Radiobutton(main_screen, text = 'Check a data', font = ('revive ov', 14), variable = rt, value = 2)
r3 = Radiobutton(main_screen, text = 'See all data', font = ('revive ov', 14), variable = rt, value = 3)
r4 = Radiobutton(main_screen, text = 'Create a New Table', variable = rt, value = 4, font = ('revive ov', 14))
r1.grid(row = 280, column = 150)
r2.grid(row = 300, column = 150)
r3.grid(row = 320, column = 150)
r4.grid(row = 340, column = 150)
b1 = Button(main_screen, text = 'NEXT', font = ('cooper black', 12), command = next_page)
b1.grid(row = 340, column = 200)


main_screen.mainloop()

