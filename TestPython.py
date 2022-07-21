from tkinter import *
from tkinter import messagebox
import hashlib
import os
import calendar
import tkcalendar
from tkcalendar import *

bg_colour = '#ede4d1'
colour_2 = '#ffe6b0'
user_temp = "temp"
pass_temp = "temp"
print(user_temp)
print(pass_temp)

class Start(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(bg=bg_colour)
        
        self.border = LabelFrame(self, bg=colour_2, bd = 10, font=("Arial", 20))
        self.border.pack(fill="both", expand="yes", padx = 150, pady = 150)

        self.main_label = Label(self.border, text = 'Login', font=("Arial Bold", 15), bg=colour_2)
        self.main_label.place(x=50, y=5)
        
        self.user_label = Label(self.border, text="Username", font=("Arial Bold", 15), bg=colour_2)
        self.user_label.place(x=50, y=35)
        self.user_entry = Entry(self.border, width = 30, bd = 5)
        self.user_entry.place(x=180, y=35)
        
        self.password_label = Label(self.border, text="Password", font=("Arial Bold", 15), bg=colour_2)
        self.password_label.place(x=50, y=95)
        self.password_entry = Entry(self.border, width = 30, show='*', bd = 5)
        self.password_entry.place(x=180, y=95)
        
        def verify():
            try:
                with open("users.txt", "r") as file:
                    info = file.readlines()
                    i = 0
                    for e in info:
                        self.user_name, self.user_password, self.saltinput =e.split(",")
                        if self.user_name.strip() == self.user_entry.get():
                            salt = self.saltinput.strip()
                            password_input_2 = self.password_entry.get()
                            passwordhash = hashlib.pbkdf2_hmac('sha256', password_input_2.encode('utf-8'), salt.encode('utf-8'), 100000)
                            passwordstring = str(passwordhash)
                            if self.user_password.strip() == passwordstring:
                                user_temp = self.user_entry.get()
                                pass_temp = passwordstring
                                print(user_temp)
                                print(pass_temp)
                                controller.show_frame(Home)
                                i = 1
                                break
                    if i==0:
                        messagebox.showinfo("Error", "Please provide correct username and password!!")
            except:
                messagebox.showinfo("Error", "Couldnt open file")
     
         
        self.submitbutton = Button(self.border, text="Submit", font=("Arial", 15), command=verify)
        self.submitbutton.place(x=320, y=130)
        
        def register():
            register_window = Tk()
            register_window.resizable(0,0)
            register_window.configure(bg=bg_colour)
            register_window.title("Register")
            reg_name_label = Label(register_window, text="Username:", font=("Arial",15), bg="deep sky blue")
            reg_name_label.place(x=10, y=10)
            reg_name_entry = Entry(register_window, width=30, bd=5)
            reg_name_entry.place(x = 200, y=10)
            salt_created = os.urandom(32)
            salt_used = str(salt_created)

            reg_password_label = Label(register_window, text="Password:", font=("Arial",15), bg="deep sky blue")
            reg_password_label.place(x=10, y=60)
            reg_password_entry = Entry(register_window, width=30, show="*", bd=5)
            reg_password_entry.place(x = 200, y=60)
            
            confirm_password_label = Label(register_window, text="Confirm Password:", font=("Arial",15), bg="deep sky blue")
            confirm_password_label.place(x=10, y=110)
            confirm_password_entry = Entry(register_window, width=30, show="*", bd=5)
            confirm_password_entry.place(x = 200, y=110)
            
            def check():
                if reg_name_entry.get()!="" or reg_password_entry.get()!="" or confirm_password_entry.get()!="":
                    if reg_password_entry.get()==confirm_password_entry.get():
                        reg_password_salt = hashlib.pbkdf2_hmac('sha256', reg_password_entry.get().encode('utf-8'), salt_used.encode('utf-8'), 100000)
                        with open("users.txt", "a") as f:
                            f.write(reg_name_entry.get()+","+str(reg_password_salt)+","+str(salt_used)+"\n")
                            messagebox.showinfo("Welcome","You are registered successfully!!")
                            register_window.destroy()
                    else:
                        messagebox.showinfo("Error","Your password didn't get match!!")
                else:
                    messagebox.showinfo("Error", "Please fill the complete field!!")
                    
            self.register_button = Button(register_window, text="Sign in", font=("Arial",15), bg="#ffc22a", command=check)
            self.register_button.place(x=170, y=150)
            
            register_window.geometry("470x220")
            register_window.mainloop()
            
        self.register_button = Button(self, text="Register", bg = "dark orange", font=("Arial",15), command=register)
        self.register_button.place(x=650, y=20)
        
class Home(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(bg=bg_colour)
    
        self.title_label = Label(self, text="Welcome to the MRGS Counselors Booking Webapp", bg = "ivory", font=("Arial Bold", 25))
        self.title_label.place(x=40, y=150)        
        self.next_button = Button(self, text="Next", font=("Arial", 15), command=lambda: controller.show_frame(Booking_Page))
        self.next_button.place(x=650, y=450)
        
        self.sign_out_button = Button(self, text="Sign Out", font=("Arial", 15), command=lambda: controller.show_frame(Start))
        self.sign_out_button.place(x=100, y=450)

class Booking_Page(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        
        self.configure(bg='ivory')
        
        def confirm_date():
            saved_date = cal.get_date()
            with open("users.txt", "a+") as f:
                flag = 0
                index = 0
                for line in f:
                    index += 1
                    if user_temp in line:
                        flag = 1
                        break
                if flag == 0:
                    messagebox.showinfo("Error","Your account couldn't be found")
                else:
                    f.write(", ")
                    f.write(saved_date)

        cal = Calendar(self, selectmode = 'day', year = 2022, month = 9, day = 22)
        cal.place(x=300, y=150)
        
        self.app_label = Label(self, text="Click on a date, then on confirm to make your booking", bg = "orange", font=("Arial Bold", 25))
        self.app_label.place(x=40, y=50)

        self.confirm_button = Button(self, text = "Confirm", font = ("Arial", 15), command = confirm_date)
        self.confirm_button.place(x=475, y=450)
        
        self.home_button = Button(self, text="Home", font=("Arial", 15), command=lambda: controller.show_frame(Start))
        self.home_button.place(x=650, y=450)
        
        self.back_button = Button(self, text="Back", font=("Arial", 15), command=lambda: controller.show_frame(Home))
        self.back_button.place(x=100, y=450)
        
'''
https://pythonprogramming.net/object-oriented-programming-crash-course-tkinter/
above link explains the new *args,**kwargs arguments used below
Like "self," actually typing out "args" and "kwargs" is not necessary, the asterisks to the trick. It is just common to add the "args" and "kwargs." 
So what are these? These are used to pass a variable, unknown, amount of arguments through the method. The difference between them is that args are used to pass non-keyworded arguments, 
where kwargs are keyword arguments (hence the meshing in the name to make it kwargs). Args are your typical parameters. Kwargs, will basically be dictionaries.
You can get by just thinking of kwargs as dictionaries that are being passed.
'''
        
class Application(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        
      
        self.window = Frame(self)
        self.window.pack()
        
        self.window.grid_rowconfigure(0, minsize = 500)
        self.window.grid_columnconfigure(0, minsize = 800)
        
        self.frames = {}
        for F in (Start, Home, Booking_Page):
            frame = F(self.window, self)
            self.frames[F] = frame
            frame.grid(row = 0, column=0, sticky="nsew")
            
        self.show_frame(Start)
        
    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        self.title("Application")


#start of program
if __name__ == '__main__':           
    app = Application()
    app.maxsize(800,500)
    app.mainloop()