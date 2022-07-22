from tkinter import *
from tkinter import messagebox
import hashlib
import os
import calendar
import tkcalendar
from tkcalendar import *
from tkcalendar import Calendar, DateEntry
import json
import datetime
from PIL import ImageTk, Image
#above is imports to allow the code to work

bg_colour = '#ede4d1'
colour_2 = '#ffe6b0'
user_temp = "temp"
pass_temp = "temp"
#global variables for colours used, and for temporary values used while program is running

class Start(Frame):
    #this class allows running of login and registration pages
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(bg = bg_colour)
        
        #this is the border around the login menu
        self.border = LabelFrame(self, bg = colour_2, bd = 10, font = ("Arial", 20))
        self.border.pack(fill = "both", expand = "yes", padx = 150, pady = 150)

        #this is the title
        self.main_label = Label(self.border, text = 'Login', font=("Arial Bold", 15), bg=colour_2)
        self.main_label.place(x = 50, y = 5)
        
        #this is the entry label and box for the username
        self.user_label = Label(self.border, text = "Username", font = ("Arial Bold", 15), bg = colour_2)
        self.user_label.place(x = 50, y = 35)
        self.user_entry = Entry(self.border, width = 30, bd = 5)
        self.user_entry.place(x = 180, y = 35)
        
        #this is the entry label and box for the password
        self.password_label = Label(self.border, text = "Password", font = ("Arial Bold", 15), bg = colour_2)
        self.password_label.place(x = 50, y = 95)
        self.password_entry = Entry(self.border, width = 30, show = '*', bd = 5)
        self.password_entry.place(x = 180, y = 95)
        
        #this function allows the inputted username to be compared to the saved one, and then the same for the password, to ensure successful logins only when both are correct
        def verify():
            try:
                with open("users.txt", "r") as file:
                    info = file.readlines()
                    i = 0
                    for e in info:
                        self.user_name, self.user_password, self.saltinput = e.split(" , ")
                        if self.user_name.strip() == self.user_entry.get():
                            salt = self.saltinput.strip()
                            password_input_2 = self.password_entry.get()
                            passwordhash = hashlib.pbkdf2_hmac('sha256', password_input_2.encode('utf-8'), salt.encode('utf-8'), 100000)
                            passwordstring = str(passwordhash)
                            if self.user_password.strip() == passwordstring:
                                global user_temp
                                global pass_temp
                                user_temp = self.user_entry.get()
                                pass_temp = passwordstring
                                controller.show_frame(Home)
                                i = 1
                                break
                    if i==0:
                        messagebox.showinfo("Error", "Please provide correct username and password!!")
            except:
                messagebox.showinfo("Error", "Couldnt open file")
     
        #this is the button that runs the verify function
        self.submitbutton = Button(self.border, text = "Submit", font = ("Arial", 15), command = verify)
        self.submitbutton.place(x = 320, y = 130)

        #this funtions opens the registration window 
        def register():
            #this is configuring the registration windows appearance
            register_window = Tk()
            register_window.resizable(0, 0)
            register_window.configure(bg = bg_colour)
            register_window.title("Register")
            #this is the registration windows username input
            reg_name_label = Label(register_window, text = "Username:", font = ("Arial",15), bg = "deep sky blue")
            reg_name_label.place(x = 10, y = 10)
            reg_name_entry = Entry(register_window, width = 30, bd = 5)
            reg_name_entry.place(x = 200, y = 10)
            
            #this creates the salt for the user registering, used later to make the password more secure
            salt_created = os.urandom(32)
            salt_used = str(salt_created)

            #this is the entry box for the password
            reg_password_label = Label(register_window, text = "Password:", font = ("Arial",15), bg = "deep sky blue")
            reg_password_label.place(x = 10, y = 60)
            reg_password_entry = Entry(register_window, width = 30, show = "*", bd = 5)
            reg_password_entry.place(x = 200, y = 60)
            
            #this is the entry box for the password confirmation, to ensure the correct password was entered originally
            confirm_password_label = Label(register_window, text = "Confirm Password:", font = ("Arial",15), bg = "deep sky blue")
            confirm_password_label.place(x = 10, y = 110)
            confirm_password_entry = Entry(register_window, width = 30, show = "*", bd = 5)
            confirm_password_entry.place(x = 200, y = 110)
            
            #this funtion runs the registration
            def check():
                #this loop checks to see if any of the entry boxes are empty
                if reg_name_entry.get() != "" or reg_password_entry.get() != "" or confirm_password_entry.get() != "":
                    f = open("users.txt", "r")
                    usernamecheck = reg_name_entry.get()
                    readfile = f.read()
                    #this loop checks if there is already a user with the same username
                    if usernamecheck in readfile:
                        messagebox.showinfo("Error", "User already exists")
                    else:
                        #this loop confirms the password was entered correctly both times
                        if reg_password_entry.get() == confirm_password_entry.get():
                            #this salts and then hashes the password for security
                            reg_password_salt = hashlib.pbkdf2_hmac('sha256', reg_password_entry.get().encode('utf-8'), salt_used.encode('utf-8'), 100000)
                            #this opens the user text file, and saves the inputted details to it after they have been secured
                            with open("users.txt", "a") as f:
                                f.write(reg_name_entry.get() + " , " + str(reg_password_salt) + " , "+str(salt_used)+"\n")
                                new_user = {"username": reg_name_entry.get(), "bookings":[]}
                                write_json(new_user)
                                messagebox.showinfo("Welcome", "You are registered successfully!!")
                                register_window.destroy()
                        else:
                            messagebox.showinfo("Error", "Your password didn't get match!!")
                else:
                    messagebox.showinfo("Error", "Please fill the complete field!!")

            #this button is to run the "check" function        
            self.register_button = Button(register_window, text = "Sign in", font = ("Arial", 15), bg = "#ffc22a", command = check)
            self.register_button.place(x = 170, y = 150)
            
            #this sets the size of the registration window popup
            register_window.geometry("470x220")
            register_window.mainloop()

        #this button opens the register window    
        self.register_button = Button(self, text = "Register", bg = "dark orange", font = ("Arial", 15), command = register)
        self.register_button.place(x = 650, y = 20)
        
class Home(Frame):
    #this class creates the home page
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(bg=bg_colour)

        #this creates the image used as the background for this page
        logo = Image.open("mental_health.png")
        logo_test = ImageTk.PhotoImage(logo)
        logo_label = Label(self, image = logo_test)
        logo_label.image = logo_test
        logo_label.place(x = 140, y = 0)
    
        #this is the title
        self.title_label = Label(self, text = "Welcome to the MRGS Counsellors Booking Webapp", bg = colour_2, font = ("Arial Bold", 24))
        self.title_label.place(x = 0, y = 40)  

        #this is the calendar page button
        self.calendar_page_button = Button(self, text = "Calendar", font = ("Arial", 15), command = lambda: controller.show_frame(Booking_Page))
        self.calendar_page_button.place(x = 600, y = 450)
        
        #this is the info page button
        self.info_page_button = Button(self, text = "Info", font = ("Arial", 15), command = lambda: controller.show_frame(Info))
        self.info_page_button.place(x = 100, y = 450)

        #this is the sing out button
        self.sign_out_button = Button(self, text = "Sign Out", font = ("Arial", 15), command = lambda: controller.show_frame(Start))
        self.sign_out_button.place(x = 10, y = 0)

class Info(Frame):
    #this creates the information page
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(bg=bg_colour)

        #title
        self.title_label = Label(self, text = "About Us", bg = colour_2, font = ("Arial Bold", 25))
        self.title_label.place(x = 80, y = 80)

        #text displayed on the page
        self.content_label = Label(self, text = """
This booking application was made by:
Joshua Bagnall, 18350@students.mrgs.school.nz

This app was made to assist students in keeping track
of which days they had booked appointments with the
MRGS counsellors""", bg = colour_2, font = ("Arial Bold", 16), justify = LEFT)
        self.content_label.place(x = 80, y = 120)

        #sign out button
        self.sign_out_button = Button(self, text = "Sign Out", font = ("Arial", 15), command = lambda: controller.show_frame(Start))
        self.sign_out_button.place(x = 600, y = 450)
        
        #back button
        self.Back_button = Button(self, text = "Back", font = ("Arial", 15), command = lambda: controller.show_frame(Home))
        self.Back_button.place(x = 100, y = 450)

class Booking_Page(Frame):
    #this page creates the calendar, and allows for the making and displaying of bookings
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        
        self.configure(bg = bg_colour)
        
        #this function adds the selected date to the JSON file containing dates and users
        def confirm_date():
            saved_date = cal.get_date()
            #this opens and reads the JSON file
            f = open("bookings.json", "r")
            data = json.load(f)
            f.close()
            #this loop checks for the correct user before editing the data
            for user in data["booking_details"]:
                if user["username"] == user_temp:
                    #this resets the file, and writes the selected date in alongside all the old data, effectively appending it
                    f = open("bookings.json" , "w")
                    user["bookings"].append(saved_date)
                    json.dump(data, f, indent = 4)

        #this creates the calendar, and sets the colour for the displayed bookings
        cal = Calendar(self, selectmode = 'day', locale = "en_NZ")
        cal.tag_config('meeting', background = 'navy', foreground = 'yellow')
        cal.pack(padx=100, pady=100, fill = "both", expand = True)

        #semi-global variable to allow the making of events on the calendar
        current_bookings = []
        def make_events():
            #opening and reading the JSON file
            f = open("bookings.json", "r")
            data = json.load(f)
            f.close()
            #checking to make sure the correct user is being displayed
            for user in data["booking_details"]:
                if user["username"] == user_temp:
                    current_bookings = user["bookings"]
                    #going through each date for the user and making an event for them to display on the calendar
                    for date in current_bookings:
                        formatted_date = datetime.datetime.strptime(date, "%d/%m/%y").date()
                        cal.calevent_create(formatted_date, "Reminder", "meeting")  

        #sign out function, used to change page and clear the displayed bookings
        def sign_out():
            cal.calevent_remove("all")
            controller.show_frame(Start)

        #back function, used to change page and clear the displayed bookings
        def back():
            cal.calevent_remove("all")
            controller.show_frame(Home)

        #label to display how to use buttons
        self.app_label = Label(self, text = "Click on a date, then on confirm to make your booking", bg = colour_2, font = ("Arial Bold", 18))
        self.app_label.place(x = 85, y = 50)

        #button to add selected date to file
        self.confirm_button = Button(self, text = "Confirm", font = ("Arial", 15), command = confirm_date)
        self.confirm_button.place(x = 475, y = 450)

        #button to display saved dates
        self.events_button = Button(self, text = "Show Bookings", font = ("Arial", 15), command = make_events)
        self.events_button.place(x = 250, y = 450)
        
        #button to sign out
        self.home_button = Button(self, text = "Sign Out", font = ("Arial", 15), command = sign_out)
        self.home_button.place(x = 650, y = 450)
        
        #button to go back to home page
        self.back_button = Button(self, text = "Back", font = ("Arial", 15), command = back)
        self.back_button.place(x = 100, y = 450)
 
class Application(Tk):
    #class to create overall application
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        
        #create the frame
        self.window = Frame(self)
        self.window.pack()
        
        #set minimum size for window
        self.window.grid_rowconfigure(0, minsize = 500)
        self.window.grid_columnconfigure(0, minsize = 800)
        
        #create frames for each windw
        self.frames = {}
        for F in (Start, Home, Booking_Page, Info):
            frame = F(self.window, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")

        #display sign in page    
        self.show_frame(Start)

    #function to change pages    
    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        self.title("MRGS Counsellor Booking App")

#function to allow writing to the JSON file
def write_json(new_data, filename = 'bookings.json'):
    with open(filename,'r+') as file:
        file_data = json.load(file)
        file_data["booking_details"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent = 4)

#start of program
if __name__ == '__main__':           
    app = Application()
    app.maxsize(800, 500)
    app.mainloop()