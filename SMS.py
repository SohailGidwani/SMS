from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import matplotlib.pyplot as plt
import requests
import bs4
from PIL import ImageTk

n = 0
try:
    city_name = 'Mumbai'
    a1 = 'http://api.openweathermap.org/data/2.5/weather?units=metric'
    a2 = "&q=" + city_name
    a3 = "&appid=" + "c6e315d09197cec231495138183954bd"
    wa = a1 + a2 + a3
    res = requests.get(wa)
    data = res.json()
    main = data['main']
    temp = main['temp']
except Exception as e:
    print("issue ", e)

try:
    quote1 = None
    wa = "https://www.brainyquote.com/quote_of_the_day"
    res = requests.get(wa)
    data = bs4.BeautifulSoup(res.text, 'html.parser')
    info = data.find('img', {'class': 'p-qotd'})
    msg = info['alt']
    for i, c in enumerate(msg):
        if c == ',' or c == '-':
            quote = msg[:i]
            quote1 = msg[i:]
except Exception as e:
    print('issue', e)

# # Display Page (3 sec)
# splash = Tk()
# splash.after(3000, splash.destroy)
# splash.overrideredirect(True)
# splash.geometry("1100x600+200+100")
# msg = Label(splash, text="Welcome\nTo\nSTUDENT\nMANAGEMENT\nSYSTEM", font=('Calibri', 70, 'bold'), fg='blue')
# msg.pack(anchor='center')
# splash.mainloop()

# empty lists for graph

m = []
ss = []


# Update the list for graph
def up_l():
    m.clear()
    ss.clear()
    con = None
    try:
        con = connect("SMSdb.db")
        cursor = con.cursor()
        sql = "select * from student"
        cursor.execute(sql)
        data = cursor.fetchall()
        for d in data:
            m.append(d[2])
            ss.append(d[1])
    except Exception as e:
        showerror("Failure", e)
    finally:
        if con is not None:
            con.close()
    return m, ss


def f1():
    add_w.deiconify()
    main_w.withdraw()


def f2():
    main_w.deiconify()
    add_w.withdraw()


def f3():
    view_w.deiconify()
    main_w.withdraw()
    view_w_st_data.delete(1.0, END)
    info = ""
    con = None
    try:
        con = connect("SMSdb.db")
        cursor = con.cursor()
        sql = "select * from student"
        cursor.execute(sql)
        data = cursor.fetchall()
        view_w_st_data.insert(INSERT, 'RollNo.\t|Name\t\t|Marks\n')
        view_w_st_data.insert(INSERT, '-' * 40 + '\n')
        for d in data:
            info = info + str(d[0]) + "\t|" + str(d[1]) + "\t\t|  " + str(d[2]) + "\n"
        view_w_st_data.insert(INSERT, info)
    except Exception as e:
        showerror("Failure", e)
    finally:
        if con is not None:
            con.close()


def f4():
    main_w.deiconify()
    view_w.withdraw()


def f5():
    con = None
    try:
        con = connect("SMSdb.db")
        cursor = con.cursor()
        sql = "insert into student values('%d', '%s','%d')"
        rno = int(add_w_ent_rno.get())
        name = add_w_ent_name.get()
        marks = int(add_w_ent_marks.get())
        if rno is not None and rno > 0:
            if len(name) >= 2:
                if 0 <= marks <= 100:
                    cursor.execute(sql % (rno, name, marks))
                    con.commit()
                    showinfo('Success', 'Record has been added')
                else:
                    showerror('Failure', 'Entered marks are invalid!!')
            else:
                showerror('Failure', 'Entered name is invalid!!')
        else:
            showerror('Failure', 'Entered rollno. is invalid!!')
    except Exception as e:
        showerror('Failure', "Please enter correct data in every field.")
    finally:
        if con is not None:
            con.close()


def f6():
    del_w.deiconify()
    main_w.withdraw()


def f7():
    con = None
    try:
        con = connect("SMSdb.db")
        cursor = con.cursor()
        sql = 'select rno from student order by rno'
        cursor.execute(sql)
        sql = "delete from student where rno='%d'"
        rno = int(del_w_ent_rno.get())
        cursor.execute(sql % rno)
        if cursor.rowcount > 0:
            showinfo('Success', 'Record has been deleted')
        else:
            showerror('Failure', "Record doesn't exist")
        con.commit()
        up_l()
    except Exception as e:
        showerror('Failure', e)
    finally:
        if con is not None:
            con.close()


def f8():
    main_w.deiconify()
    del_w.withdraw()


def f9():
    up_w.deiconify()
    main_w.withdraw()


def f10():
    con = None
    try:
        con = connect("SMSdb.db")
        cursor = con.cursor()
        sql = "update student set name='%s', marks='%d' where rno='%d'"
        rno = int(up_w_ent_rno.get())
        name = up_w_ent_name.get()
        marks = int(up_w_ent_marks.get())
        cursor.execute(sql % (name, marks, rno))
        if cursor.rowcount > 0:
            showinfo('Success', 'Record has been updated')
        else:
            showerror('Failure', "Record doesn't exist")
        con.commit()
        up_l()

    except Exception as e:
        showerror('Failure', "Please enter correct data in every field.")
    finally:
        if con is not None:
            con.close()


def f11():
    up_l()
    marks = []
    name = []
    marks, name = up_l()
    plt.bar(name, marks, width=0.3)
    plt.xlabel("NAME--->")
    plt.ylabel("MARKS--->")
    plt.title("ANALYSIS")
    plt.show()


def f12():
    main_w.deiconify()
    up_w.withdraw()


def login():
    main_w.withdraw()
    radio.deiconify()


def create_acc():
    global radio
    radio = Tk()
    radio.title(' ')
    radio.geometry('300x300')
    radio.config(bg='sienna1')
    global var
    var = StringVar()
    quest = Label(radio, text='Who wants to register ?', font=("constantia", 18, 'bold'), bg='sienna1').place(x=10,
                                                                                                              y=10)
    # radio1 = Radiobutton(radio, text='Staff Member', variable=var, value='1', font=("constantia", 16, 'bold')).place(x=10,
    #                                                                                                                y=60)
    # radio2 = Radiobutton(radio, text='Student', variable=var, value='2', font=("constantia", 16, 'bold')).place(x=10,
    #                                                                                                           y=100)
    # next_b = Button(radio, text='Next', font=("constantia", 14, "bold"), width=10, height=1, bd=1,
    #                 command=next_button).place(x=50, y=160)
    next_b1 = Button(radio, text='Staff Member', font=("constantia", 14, "bold"), width=10, height=1, bd=1,
                     command=next_button).place(x=80, y=60)
    next_b2 = Button(radio, text='Student', font=("constantia", 14, "bold"), width=10, height=1, bd=1,
                     command=next_button2).place(x=80, y=120)
    print(n)
    radio.mainloop()


def next_button():
    login_w.withdraw()
    radio.withdraw()
    register_w_t.deiconify()


def next_button2():
    login_w.withdraw()
    radio.withdraw()
    register_w_s.deiconify()


def one():
    global n
    n = 1
    radio.withdraw()
    login_w.deiconify()


def two():
    global n
    n = 2
    radio.withdraw()
    login_w.deiconify()


def Log_in():
    global em_en, n
    con = None
    try:
        con = connect("SMSdb.db")
        cursor = con.cursor()

        if n == 1:
            em = em_en.get()
            sql = "select password,name from regteach where email='%s'"
            cursor.execute(sql % (em))
            data = cursor.fetchone()
            print(data)
            pwd = pass_en.get()
            if pwd == str(data[0]):
                showinfo('SUCCESS!', 'Logged in successfully')
                login_w.withdraw()
                main_w.deiconify()
                main_w_b_add['state'] = 'normal'
                main_w_b_view['state'] = 'normal'
                main_w_b_delete['state'] = 'normal'
                main_w_b_update['state'] = 'normal'
                main_w_chart['state'] = 'normal'
                log_in_b.destroy()
                login_name = Label(main_w, text=f'Staff - {data[1]}', font=("constantia", 20, 'bold'), bg="snow",
                                   fg="sienna3")
                login_name.place(x=1000, y=5)

        if n == 2:
            em = em_en.get()
            print(em)
            sql = "select password,name from regstud where email='%s'"
            cursor.execute(sql % (em))
            data = cursor.fetchone()
            print(data, '1')
            pwd = pass_en.get()
            if pwd == str(data[0]):
                showinfo('SUCCESS!', 'Logged in successfully')
                main_w.deiconify()
                main_w_b_add['state'] = 'disabled'
                main_w_b_view['state'] = 'normal'
                main_w_b_delete['state'] = 'disabled'
                main_w_b_update['state'] = 'disabled'
                main_w_chart['state'] = 'normal'
                log_in_b.destroy()
                login_name = Label(main_w, text=f'Student - {data[1]}', font=("constantia", 20, 'bold'), bg="snow",
                                   fg="sienna3")
                login_name.place(x=1000, y=5)

    except Exception as e:
        showerror('Failure', e)
    finally:
        if con is not None:
            con.close()


def reg_teach():
    con = None
    try:
        con = connect("SMSdb.db")
        cursor = con.cursor()
        sql = "insert into regteach values('%s', '%s','%s', '%s', '%s')"
        pwd = pass_en_t.get()
        name = name_en_t.get()
        email = EM_en_t.get()
        phno = ph_no_en_t.get()
        sub = sub_en_t.get()
        cursor.execute(sql % (email, name, phno, sub, pwd))
        con.commit()
        showinfo('Success', 'Record has been added')
        register_w_t.withdraw()
        login_w.deiconify()

        # if rno is not None and rno > 0:
        #     if len(name) >= 2:
        #         if 0 <= marks <= 100:
        #             cursor.execute(sql % (rno, name, marks))
        #             con.commit()
        #             showinfo('Success', 'Record has been added')
        #         else:
        #             showerror('Failure', 'Entered marks are invalid!!')
        #     else:
        #         showerror('Failure', 'Entered name is invalid!!')
        # else:
        #     showerror('Failure', 'Entered rollno. is invalid!!')

    except Exception as e:
        showerror('Failure', "Please enter correct data in every field.")
    finally:
        if con is not None:
            con.close()


def regstud():
    con = None
    try:
        con = connect("SMSdb.db")
        cursor = con.cursor()
        sql = "insert into regstud values('%s', '%d', '%s','%s', '%s')"
        rno = int(r_no_en_s.get())
        name = name_en_s.get()
        email = em_en_s.get()
        bd = bd_en_s.get()
        pwd = pass_en_s.get()
        cursor.execute(sql % (email, rno, name, bd, pwd))
        con.commit()
        showinfo('Success', 'Record has been added')
        register_w_s.withdraw()
        login_w.deiconify()
        # if rno is not None and rno > 0:
        #     if len(name) >= 2:
        #         if 0 <= marks <= 100:
        #             cursor.execute(sql % (rno, name, marks))
        #             con.commit()
        #             showinfo('Success', 'Record has been added')
        #         else:
        #             showerror('Failure', 'Entered marks are invalid!!')
        #     else:
        #         showerror('Failure', 'Entered name is invalid!!')
        # else:
        #     showerror('Failure', 'Entered rollno. is invalid!!')
    except Exception as e:
        showerror('Failure', "Please enter correct data in every field.")
    finally:
        if con is not None:
            con.close()


def login_back():
    main_w.deiconify()
    login_w.withdraw()


def reg_t_back():
    login_w.deiconify()
    register_w_t.withdraw()


def reg_s_back():
    login_w.deiconify()
    register_w_s.withdraw()


# Main Page
w_login = 0
main_w = Tk()
p = PhotoImage(file='icons8-pass-fail-64.png')
main_w.iconphoto(False, p)
main_w.title('Menu')
main_w.geometry("1280x853+200+100")
main_w.configure(bg='snow')
main_w.resizable(False, False)
bg = ImageTk.PhotoImage(file='Appbg.jpg')
bf_image = Label(main_w, image=bg).place(x=0, y=60, relwidth=1, relheight=1)
Menu_Frame = Frame(main_w, bg='snow')
Menu_Frame.place(x=220, y=110, height="725", width="850")
sms = Label(main_w, text="S.M.S", font=("constantia", 32, 'bold'), bg="snow", fg="sienna3").place(x=590, y=0)
title = Label(Menu_Frame, text="Menu", font=("constantia", 30, 'bold'), bg="snow", fg="salmon3").place(x=370, y=8)
main_w_b_add = Button(Menu_Frame, text="Add", font=("constantia", 16, "bold"), bg="salmon3", fg="white", width=15,
                      height=2, bd=0, command=f1, state=DISABLED)
main_w_b_add.place(x=140, y=120)
main_w_b_view = Button(Menu_Frame, text="View", font=("constantia", 16, "bold"), bg="salmon3", fg="white", width=15,
                       height=2, bd=0, command=f3, state=DISABLED)
main_w_b_view.place(x=510, y=120)
main_w_b_update = Button(Menu_Frame, text="Update", font=("constantia", 16, "bold"), bg="salmon3", fg="white", width=15,
                         height=2, bd=0, command=f9, state=DISABLED)
main_w_b_update.place(x=140, y=210)
main_w_b_delete = Button(Menu_Frame, text="Delete", font=("constantia", 16, "bold"), bg="salmon3", fg="white", width=15,
                         height=2, bd=0, command=f6, state=DISABLED)
main_w_b_delete.place(x=510, y=210)
main_w_chart = Button(Menu_Frame, text="Graphical View", font=("constantia", 16, "bold"), bg="salmon3", fg="white",
                      width=15,
                      height=2, bd=0, command=f11, state=DISABLED)
main_w_chart.place(x=325, y=300)
exit_button = Button(Menu_Frame, text="Exit", font=("constantia", 16, "bold"), bg="salmon3", fg="white", width=15,
                     height=2, bd=0, command=main_w.destroy).place(x=325, y=390)

lbl_temp = Label(Menu_Frame, text=f'\u03B8 Temp : {temp}\u2103', font=("constantia", 16, "bold"), bg='snow',
                 fg="salmon3")
lbl_temp.place(relx=0.0, rely=1.0, anchor='sw')

log_in_b = Button(main_w, text='Log In', font=("constantia", 20, "bold"), bg="snow", fg="sienna3",
                  width=20,
                  height=1, bd=0, command=login)
log_in_b.place(x=1000, y=3)

# Add new student
add_w = Toplevel(main_w)
add_w.title("Add Student Info")
add_w.geometry("1280x853+200+100")
add_w.resizable(False, False)
bg1 = ImageTk.PhotoImage(file='register_bg.webp')
bf_image1 = Label(add_w, image=bg1).place(x=0, y=0, relwidth=1, relheight=1)
add_frame = Frame(add_w, bg='white')
add_frame.place(x=220, y=60, height="725", width="850")
title1 = Label(add_frame, text="Add Student Info", font=("constantia", 32, 'bold'), bg="white", fg="salmon3").pack(
    pady=10)
add_w_lbl_rno = Label(add_frame, text="Enter Roll No.", font=("constantia", 20, 'bold'), bg="white", fg="salmon3")
add_w_ent_rno = Entry(add_frame, bd=5)
add_w_lbl_name = Label(add_frame, text="Enter Name", font=("constantia", 20, 'bold'), bg="white", fg="salmon3")
add_w_ent_name = Entry(add_frame, bd=5)
add_w_lbl_marks = Label(add_frame, text="Enter Marks", font=("constantia", 20, 'bold'), bg="white", fg="salmon3")
add_w_ent_marks = Entry(add_frame, bd=5)
add_w_b_save = Button(add_frame, text="Save", font=("constantia", 16, "bold"), bg="salmon3", fg="white", width=14, bd=0,
                      command=f5)
add_w_b_back = Button(add_frame, text="Back", font=("constantia", 16, "bold"), bg="salmon3", fg="white", width=14, bd=0,
                      command=f2)
add_w_lbl_rno.pack(pady=10)
add_w_ent_rno.pack(pady=10)
add_w_lbl_name.pack(pady=10)
add_w_ent_name.pack(pady=10)
add_w_lbl_marks.pack(pady=10)
add_w_ent_marks.pack(pady=10)
add_w_b_save.pack(pady=10)
add_w_b_back.pack(pady=10)
add_w.withdraw()

# View Student Info
view_w = Toplevel(main_w)
view_w.title("View Students Info")
view_w.geometry("1280x853+200+100")
view_w.resizable(False, False)
bg2 = ImageTk.PhotoImage(file='Viewpg.jpg')
bf_image2 = Label(view_w, image=bg2).place(x=0, y=0, relwidth=1, relheight=1)
view_w_st_data = ScrolledText(view_w, width=65, height=15, font=('Courier', 20, 'bold'))
view_w_b_back = Button(view_w, text="Back", font=('Courier', 20, 'bold'), bg='snow', command=f4)
view_w_st_data.pack(pady=10)
view_w_b_back.pack(pady=10)
view_w.withdraw()

# Delete Specific Student
del_w = Toplevel(main_w)
del_w.title("Delete Student Info")
del_w.geometry("1280x853+200+100")
del_w.resizable(False, False)
bg3 = ImageTk.PhotoImage(file='Deletepg.jpg')
bf_image3 = Label(del_w, image=bg3).place(x=0, y=0, relwidth=1, relheight=1)
del_frame = Frame(del_w, bg='white')
del_frame.place(x=220, y=60, height="725", width="850")
title2 = Label(del_frame, text="Delete Student Info", font=("constantia", 32, 'bold'), bg="white", fg="salmon3").place(
    x=240, y=8)
del_w_lbl_rno = Label(del_frame, text="Enter Roll No.", font=("constantia", 20, 'bold'), bg="white",
                      fg="salmon3").place(x=350, y=120)
del_w_ent_rno = Entry(del_frame, bg="light gray", bd=5)
del_w_ent_rno.place(x=375, y=180)
del_w_b_delete = Button(del_frame, text="Delete", font=("constantia", 16, "bold"), bg="salmon3", fg="white", width=14,
                        bd=0, command=f7).place(x=350, y=300)
del_w_b_back = Button(del_frame, text="Back", font=("constantia", 16, "bold"), bg="salmon3", fg="white", width=14, bd=0,
                      command=f8).place(x=350, y=390)
del_w.withdraw()

# Update Specific Student's Info
up_w = Toplevel(main_w)
up_w.title("Update Student Info")
up_w.geometry("1280x853+200+100")
up_w.resizable(False, False)
bg4 = ImageTk.PhotoImage(file='Deletepg.jpg')
bf_image4 = Label(up_w, image=bg4).place(x=0, y=0, relwidth=1, relheight=1)
up_frame = Frame(up_w, bg='white')
up_frame.place(x=220, y=60, height="725", width="850")
title3 = Label(up_frame, text="Update Student Info", font=("constantia", 32, 'bold'), bg="white", fg="salmon3").pack(
    pady=10)
up_w_lbl_rno = Label(up_frame, text="Enter Roll No.", font=("constantia", 20, 'bold'), bg="white", fg="salmon3")
up_w_ent_rno = Entry(up_frame, bd=5)
up_w_lbl_name = Label(up_frame, text="Enter Name", font=("constantia", 20, 'bold'), bg="white", fg="salmon3")
up_w_ent_name = Entry(up_frame, bd=5)
up_w_lbl_marks = Label(up_frame, text="Enter Marks", font=("constantia", 20, 'bold'), bg="white", fg="salmon3")
up_w_ent_marks = Entry(up_frame, bd=5)
up_w_b_save = Button(up_frame, text="Save", font=("constantia", 16, "bold"), bg="salmon3", fg="white", width=14, bd=0,
                     command=f10)
up_w_b_back = Button(up_frame, text="Back", font=("constantia", 16, "bold"), bg="salmon3", fg="white", width=14, bd=0,
                     command=f12)
up_w_lbl_rno.pack(pady=10)
up_w_ent_rno.pack(pady=10)
up_w_lbl_name.pack(pady=10)
up_w_ent_name.pack(pady=10)
up_w_lbl_marks.pack(pady=10)
up_w_ent_marks.pack(pady=10)
up_w_b_save.pack(pady=10)
up_w_b_back.pack(pady=10)
up_w.withdraw()

radio = Toplevel(main_w)
radio.title(' ')
radio.geometry('300x300+300+200')
radio.config(bg='sienna1')
quest = Label(radio, text='Who wants to log in ?', font=("constantia", 18, 'bold'), bg='sienna1').place(x=10,
                                                                                                        y=10)
# radio1 = Radiobutton(radio, text='Staff Member', variable=var, value='1', font=("constantia", 16, 'bold')).place(x=10,
#                                                                                                                y=60)
# radio2 = Radiobutton(radio, text='Student', variable=var, value='2', font=("constantia", 16, 'bold')).place(x=10,
#                                                                                                           y=100)
# next_b = Button(radio, text='Next', font=("constantia", 14, "bold"), width=10, height=1, bd=1,
#                 command=next_button).place(x=50, y=160)
next_bn1 = Button(radio, text='Staff Member', font=("constantia", 14, "bold"), width=10, height=1, bd=1,
                  command=one).place(x=80, y=60)
next_bn2 = Button(radio, text='Student', font=("constantia", 14, "bold"), width=10, height=1, bd=1,
                  command=two).place(x=80, y=120)
radio.withdraw()

login_w = Toplevel(main_w)
login_w.title("Log In")
login_w.geometry("670x720+300+200")
login_w.resizable(False, False)
login_w.config(bg='sienna1')
login_frame = Frame(login_w, bg='white')
login_frame.place(x=35, y=20, height="650", width="600")
bg10 = ImageTk.PhotoImage(file='user.png')
bf_image10 = Label(login_frame, image=bg10, bg='white')
# .place(x=315, y=100)

login_lbl = Label(login_frame, text='S.M.S', font=("constantia", 32, 'bold'), bg='white', fg="sienna2")
# .place(x=270, y=10)
login_lbl.pack(pady=10)
bf_image10.pack(pady=30)
em_lbl = Label(login_frame, text='E-mail', font=("constantia", 16, 'bold'), bg='white', fg="sienna2").place(x=110,
                                                                                                            y=220)

em_en = Entry(login_frame, bd=0, width=35, font=("constantia", 16, 'bold'), bg='gray95')
em_en.place(x=110, y=250)
w = Canvas(login_frame, width=420, height=2, bg='sienna2')
w.place(x=109, y=275)
pass_lbl = Label(login_frame, text='Password', font=("constantia", 16, 'bold'), bg='white', fg="sienna2").place(
    x=110,
    y=320)
pass_en = Entry(login_frame, bd=0, width=35, font=("constantia", 16, 'bold'), bg='gray95', show='*')
pass_en.place(x=110, y=350)
w1 = Canvas(login_frame, width=420, height=2, bg='sienna2')
w1.place(x=109, y=375)

login_b = Button(login_frame, text="Log In", font=("constantia", 16, "bold"), bg="sienna2", fg="white",
                 width=10,
                 height=1, bd=0, command=Log_in).place(x=240, y=430)
want_to_reg_b = Button(login_frame, text="Don't have an account ?", font=("constantia", 16, "bold", 'underline'),
                       bg="white", fg="sienna2", width=20,
                       height=1, bd=0, command=create_acc).place(x=180, y=515)
login_w_b_back = Button(login_frame, text="Back", font=("constantia", 16, "bold"), bg="sienna2", fg="white", width=10,
                        bd=0, height=1, command=login_back).place(x=240, y=575)
login_w.withdraw()

register_w_t = Toplevel(main_w)
register_w_t.title('Register')
register_w_t.geometry("1280x853+200+100")
register_w_t.resizable(False, False)
register_w_t.configure(bg='sienna1')
register_frame_t = Frame(register_w_t, bg='white')
register_frame_t.place(x=65, y=50, height="750", width="1150")
bg11 = ImageTk.PhotoImage(file='icons8-checkmark-1080.png')
bf_image11 = Label(register_frame_t, image=bg11, bg='white')
bf_image11.place(x=0, y=80)

CM = Label(register_frame_t, text="CHECKMARK", font=("constantia", 32, 'bold'), bg='white', fg="sienna2").place(
    x=145,
    y=600)
register = Label(register_frame_t, text="Register", font=("constantia", 32, 'bold'), bg='white',
                 fg="sienna2").place(
    x=775, y=10)
w = Canvas(register_frame_t, width=2, height=630, bg='sienna1')
w.place(x=540, y=60)
name_lbl_t = Label(register_frame_t, text="Name", font=("constantia", 20, 'bold'), bg='white', fg="sienna2").place(
    x=600,
    y=70)
name_en_t = Entry(register_frame_t, bd=1, width=40, font=("constantia", 16, 'bold'), bg='azure2')
name_en_t.place(x=600, y=110, height=30)

'''roll_lbl = Label(register_frame_t, text="RollNo.", font=("constantia", 18, 'bold'), bg='white', fg="salmon3").place(x=950,
                                                                                                                  y=70)
roll_en = Entry(register_frame_t, bd=5, width=25)
roll_en.place(x=950, y=110)
star_lbl = Label(register_frame_t, text='*', font=("constantia", 18, 'bold'), bg='white', fg='red')
star_lbl.place(x=1040, y=70)'''

ph_no_lbl_t = Label(register_frame_t, text="Phone No.", font=("constantia", 20, 'bold'), bg='white',
                    fg="sienna2").place(
    x=600,
    y=160)
ph_no_en_t = Entry(register_frame_t, bd=1, font=("constantia", 16, 'bold'), width=40, bg='azure2')
ph_no_en_t.place(x=600, y=200)

EM_lbl_t = Label(register_frame_t, text="E-mail", font=("constantia", 20, 'bold'), bg='white', fg="sienna2").place(
    x=600, y=250)
EM_en_t = Entry(register_frame_t, bd=1, font=("constantia", 16, 'bold'), width=40, bg='azure2')
EM_en_t.place(x=600, y=290)

sub_lbl_t = Label(register_frame_t, text="Subject", font=("constantia", 20, 'bold'), bg='white',
                  fg="sienna2").place(
    x=600, y=340)
sub_en_t = Entry(register_frame_t, bd=1, font=("constantia", 16, 'bold'), width=40, bg='azure2')
sub_en_t.place(x=600, y=380)

pass_lbl_t = Label(register_frame_t, text="Password", font=("constantia", 20, 'bold'), bg='white',
                   fg="sienna2").place(
    x=600, y=430)
pass_en_t = Entry(register_frame_t, bd=1, font=("constantia", 16, 'bold'), show='*', width=40, bg='azure2')
pass_en_t.place(x=600, y=470)

register_b_t = Button(register_frame_t, text="Register", font=("constantia", 18, "bold"), bg="sienna2", fg="white",
                      width=20,
                      height=2, bd=0, command=reg_teach).place(x=700, y=550)
register_w_t_b_back = Button(register_frame_t, text="Back", font=("constantia", 16, "bold"), bg="sienna2", fg="white",
                             width=10,
                             bd=0, height=1, command=reg_t_back).place(x=790, y=650)

register_w_t.withdraw()

register_w_s = Toplevel(main_w)
register_w_s.title('Register')
register_w_s.geometry("1280x853+200+100")
register_w_s.resizable(False, False)
register_w_s.configure(bg='sienna1')
register_frame_s = Frame(register_w_s, bg='white')
register_frame_s.place(x=65, y=50, height="750", width="1150")
# bg12 = ImageTk.PhotoImage(file='icons8-checkmark-1080.png')
bf_image12 = Label(register_frame_s, image=bg11, bg='white')
bf_image12.place(x=0, y=80)
CM_s = Label(register_frame_s, text="CHECKMARK", font=("constantia", 32, 'bold'), bg='white', fg="sienna2").place(x=145,
                                                                                                                  y=600)
register_s = Label(register_frame_s, text="Register", font=("constantia", 32, 'bold'), bg='white', fg="sienna2").place(
    x=775, y=10)
w_s = Canvas(register_frame_s, width=2, height=630, bg='sienna2')
w_s.place(x=540, y=60)
name_lbl_s = Label(register_frame_s, text="Name", font=("constantia", 20, 'bold'), bg='white', fg="sienna2").place(
    x=600,
    y=70)
name_en_s = Entry(register_frame_s, bd=1, width=40, font=("constantia", 16, 'bold'), bg='azure2')
name_en_s.place(x=600, y=110, height=30)

'''roll_lbl = Label(register_frame_s, text="RollNo.", font=("constantia", 18, 'bold'), bg='white', fg="salmon3").place(x=950,
                                                                                                                  y=70)
roll_en = Entry(register_frame_s, bd=5, width=25)
roll_en.place(x=950, y=110)
star_lbl = Label(register_frame_s, text='*', font=("constantia", 18, 'bold'), bg='white', fg='red')
star_lbl.place(x=1040, y=70)'''

r_no_lbl_s = Label(register_frame_s, text="Roll No.", font=("constantia", 20, 'bold'), bg='white', fg="sienna2").place(
    x=600,
    y=160)
r_no_en_s = Entry(register_frame_s, bd=1, font=("constantia", 16, 'bold'), width=40, bg='azure2')
r_no_en_s.place(x=600, y=200)

bd_lbl_s = Label(register_frame_s, text="Birthdate (DD/MM/YY)", font=("constantia", 20, 'bold'), bg='white',
                 fg="sienna2").place(x=600, y=250)
bd_en_s = Entry(register_frame_s, bd=1, font=("constantia", 16, 'bold'), width=40, bg='azure2')
bd_en_s.place(x=600, y=290)

em_lbl_s = Label(register_frame_s, text="Email", font=("constantia", 20, 'bold'), bg='white', fg="sienna2").place(x=600,
                                                                                                                  y=340)
em_en_s = Entry(register_frame_s, bd=1, font=("constantia", 16, 'bold'), width=40, bg='azure2')
em_en_s.place(x=600, y=380)

pass_lbl_s = Label(register_frame_s, text="Password", font=("constantia", 20, 'bold'), bg='white', fg="sienna2").place(
    x=600, y=430)
pass_en_s = Entry(register_frame_s, bd=1, font=("constantia", 16, 'bold'), show='*', width=40, bg='azure2')
pass_en_s.place(x=600, y=470)

register_b_s = Button(register_frame_s, text="Register", font=("constantia", 18, "bold"), bg="sienna2", fg="white",
                      width=20,
                      height=2, bd=0, command=regstud).place(x=700, y=550)
register_w_s_b_back = Button(register_frame_s, text="Back", font=("constantia", 16, "bold"), bg="sienna2", fg="white",
                             width=10,
                             bd=0, height=1, command=reg_s_back).place(x=790, y=650)
register_w_s.withdraw()

main_w.mainloop()
