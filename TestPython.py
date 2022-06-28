from tkinter import *
from tkinter import messagebox
import hashlib
import os

'''
understanding the parameters in the init function (constructor):
    self represents the current object. This is a common first parameter for any method of a class. As you suggested, it's similar to Java's this.
    
    parent represents a widget to act as the parent of the current object. All widgets in tkinter except the root window require a parent (sometimes also called a master)
    
    controller represents some other object that is designed to act as a common point of interaction for several pages of widgets. It is an attempt to decouple the pages. 
    That is to say, each page doesn't need to know about the other pages. If it wants to interact with another page, such as causing it to be visible, it can ask the controller to make it visible.    
    '''
class Start(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        
        self.border = LabelFrame(self, text='Login', bg='ivory', bd = 10, font=("Arial", 20))
        self.border.pack(fill="both", expand="yes", padx = 150, pady=150)
        
        self.user_label = Label(self.border, text="Username", font=("Arial Bold", 15), bg='ivory')
        self.user_label.place(x=50, y=20)
        self.user_entry = Entry(self.border, width = 30, bd = 5)
        self.user_entry.place(x=180, y=20)
        
        self.password_label = Label(self.border, text="Password", font=("Arial Bold", 15), bg='ivory')
        self.password_label.place(x=50, y=80)
        self.password_entry = Entry(self.border, width = 30, show='*', bd = 5)
        self.password_entry.place(x=180, y=80)
        
        def verify():
            try:
                with open("users.txt", "r") as f:
                    info = f.readlines()
                    i  = 0
                    for e in info:
                        self.user_name, self.user_password =e.split(",")
                        if self.user_name.strip() == self.user_entry.get() and self.user_password.strip() == self.password_entry.get():
                            controller.show_frame(Second)
                            i = 1
                            break
                    if i==0:
                        messagebox.showinfo("Error", "Please provide correct username and password!!")
            except:
                messagebox.showinfo("Error", "Couldnt open file")
     
         
        self.submitbutton = Button(self.border, text="Submit", font=("Arial", 15), command=verify)
        self.submitbutton.place(x=320, y=115)
        
        def register():
            register_window = Tk()
            register_window.resizable(0,0)
            register_window.configure(bg="ivory")
            register_window.title("Register")
            reg_name_label = Label(register_window, text="Username:", font=("Arial",15), bg="deep sky blue")
            reg_name_label.place(x=10, y=10)
            reg_name_entry = Entry(register_window, width=30, bd=5)
            reg_name_entry.place(x = 200, y=10)
            salt = os.urandom(32)

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
                        reg_password_salt = hashlib.pbkdf2_hmac('sha256', reg_password_entry.get().encode('utf-8'), salt, 100000)
                        with open("users.txt", "a") as f:
                            f.write(reg_name_entry.get() + "," + str(reg_password_salt)+"\n")
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
        
class Second(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
    
        self.title_label = Label(self, text="Start of Appliction, Welocme to my program....", bg = "ivory", font=("Arial Bold", 25))
        self.title_label.place(x=40, y=150)        
        self.next_button = Button(self, text="Next", font=("Arial", 15), command=lambda: controller.show_frame(Third))
        self.next_button.place(x=650, y=450)
        
        self.back_button = Button(self, text="Back", font=("Arial", 15), command=lambda: controller.show_frame(Start))
        self.back_button.place(x=100, y=450)
        
#A lambda function is a small anonymous function(usually we dont need to reuse it)
#A lambda function can take any number of arguments, but can only have one expression 

class Third(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        
        self.configure(bg='ivory')
        
        self.app_label = Label(self, text="Store some content related to your \n project or what your application made for. \n All the best!!", bg = "orange", font=("Arial Bold", 25))
        self.app_label.place(x=40, y=150)
        
        self.home_button = Button(self, text="Home", font=("Arial", 15), command=lambda: controller.show_frame(Start))
        self.home_button.place(x=650, y=450)
        
        self.back_button = Button(self, text="Back", font=("Arial", 15), command=lambda: controller.show_frame(Second))
        self.back_button.place(x=100, y=450)
        
'''https://pythonprogramming.net/object-oriented-programming-crash-course-tkinter/
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
        for F in (Start, Second, Third):
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

