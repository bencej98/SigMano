import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
from tkinter import ttk

class MainApp(tk.Tk):

    def __init__(self, add_user_name_password: callable  ,*args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.frame_width = 400
        self.frame_height = 400
        self.resizable(False, False)
        self.background_color = "#535356"
        self.title_line_color = "#6b0404"
        self.login_background_color = "#2b2b2c"
        self.register_button_background = "#a40c13"
        self.font_color = "white"
        self.wm_iconbitmap('logo/sigma_logo.ico')
        # fonts
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.label_font = tkfont.Font(family='Arial', size=12, weight="bold")
        self.login_label_font = tkfont.Font(family='Arial', size=10)
        self.button_font = tkfont.Font(family='Helvetica', size=12, weight="bold")
        self.geometry("400x400")
        self.title("Sigmano War")
        # screen opens in the middle
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width/2) - (self.frame_width/2)
        y = (screen_height/2) - (self.frame_height/1)
        self.geometry('%dx%d+%d+%d' % (self.frame_width, self.frame_height, x, y))

        # stack frames onto each other in container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # create a frame dict. and put each page into it
        self.frames = {}
        for curr_page in (LoginPage, RegisterPage):
            page_name = curr_page.__name__
            frame = curr_page(parent=container, controller=self, add_user_to_login=add_user_name_password)
            self.frames[page_name] = frame

            # set all frame to the same grid location
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class LoginPage(tk.Frame):

    def __init__(self, parent, controller, add_user_to_login):
        self.add_user_to_login = add_user_to_login
        self.frame_parent = controller
        self.direct_frame_parent = parent

        tk.Frame.__init__(self, parent, bg=controller.background_color)
        self.controller = controller
        title_label = tk.Label(self, text="Login Page", font=self.controller.title_font, background=self.controller.title_line_color, fg="white")
        title_label.pack(side="top", fill="x", pady=10)

        # username
        label_1 = tk.Label(self, text="User name", font=self.controller.label_font, background=controller.background_color, fg=self.controller.font_color)
        username = tk.StringVar()
        username_input_field = tk.Entry(self, textvariable=username, font=controller.label_font)
        # password
        label_2 = tk.Label(self, text="Password", font=self.controller.label_font, background=controller.background_color, fg=self.controller.font_color)
        password = tk.StringVar()
        password_input_field = tk.Entry(self, textvariable=password, show="*", font=controller.label_font)
        # buttons
        login_button = tk.Button(self, text="Login",
                            command=lambda: self._logging_in(username, password), font=self.controller.button_font, width=10, background=self.controller.login_background_color, fg="white")
        register_button = tk.Button(self, text="Register",
                            command=lambda: controller.show_frame("RegisterPage"), font=self.controller.button_font, width=10, background=self.controller.register_button_background, fg="white")
        
        label_1.pack()
        username_input_field.pack()
        label_2.pack()
        password_input_field.pack()
        login_button.pack(ipady=10, ipadx=10, pady=10)
        register_button.pack(ipady=10, ipadx=10)

    def _logging_in(self, username: tk.StringVar, password: tk.StringVar)-> dict | None:
        """Controls user input and passes user datas and _destroy fucntion to client_socket.py"""
        if self._control_input(username, password):
            self.add_user_to_login("Auth", username.get(), password.get(), self._destroy)

    def _destroy(self):
        """Withdraws the login screen once the login is successful"""
        self.frame_parent.withdraw()

    def _control_input(self, username: tk.StringVar, password: tk.StringVar):
        """ Controls the input from the user """
        if str(username.get()).strip() == "":
            messagebox.showinfo("Empty input", "User name field can't be empty!")
            return False

        elif str(password.get()).strip() == "":
            messagebox.showinfo("Empty input", "Password field can't be empty!")
            return False
        return True

class RegisterPage(tk.Frame):

    def __init__(self, parent, controller, add_user_to_login):
        self.add_user_to_login = add_user_to_login 
        self.frame_parent = controller

        tk.Frame.__init__(self, parent, background=controller.background_color)
        self.controller = controller
        title_label = tk.Label(self, text="Register Page", font=controller.title_font, background=self.controller.title_line_color, fg=self.controller.font_color)
        title_label.pack(side="top", fill="x", pady=10)

        # # username
        username_label = tk.Label(self, text="User name: ", font=controller.label_font, background=controller.background_color, fg=self.controller.font_color)
        username = tk.StringVar()
        self.username_entry = tk.Entry(self, textvariable=username, font=controller.label_font)
        # password 1
        password_label_1 = tk.Label(self, text="Password: ", font=controller.label_font, background=controller.background_color, fg=self.controller.font_color)
        password_1 = tk.StringVar()
        self.password_entry_1 = tk.Entry(self, textvariable=password_1, font=controller.label_font, show="*")
        # password 2
        password_label_2 = tk.Label(self, text="Password again: ", font=controller.label_font, background=controller.background_color, fg=self.controller.font_color)
        password_2 = tk.StringVar()
        self.password_entry_2 = tk.Entry(self, textvariable=password_2,font=controller.label_font, show="*")

        register_button = tk.Button(self, text="Register",
                           command=lambda: self._register_user(username, password_1, password_2), font=self.controller.button_font, width=10, background=self.controller.register_button_background, fg="white")
        go_to_login_button = tk.Button(self, text="Back to Login",
                           command=lambda: controller.show_frame("LoginPage"), font=self.controller.button_font, width=10, background=self.controller.login_background_color, fg="white")
        # pack all
        username_label.pack()
        self.username_entry.pack()
        password_label_1.pack()
        self.password_entry_1.pack()
        password_label_2.pack()
        self.password_entry_2.pack()
        register_button.pack(ipady=10, ipadx=10, pady=10)
        go_to_login_button.pack(ipady=10, ipadx=10)

    def _register_user(self, username: tk.StringVar, password_1: tk.StringVar, password_2: tk.StringVar):
        """Controls user credentials and passes user data, _destroy() to client_socket.py"""
        if self._control_user_credentials(username, password_1, password_2):
            self.add_user_to_login("Registration", username.get(), password_1.get(), self._destroy)

            self._empty_entry_fields()
            messagebox.showinfo("Success", "Successfuly registered!")
            self.controller.show_frame("LoginPage")

    def _destroy(self):
        """Destroys register frame"""
        self.frame_parent.destroy()

    def _control_user_credentials(self, username: tk.StringVar, password_1: tk.StringVar, password_2: tk.StringVar):
        """Controls if user gave correct credentials
        Checks if passwords match"""
        if username.get().strip() == "":
            messagebox.showinfo("Empty field", "User name field can't be empty!")
        elif password_1.get().strip() == "" or password_2.get().strip() == "":
            messagebox.showinfo("Empty field", "Password field can't be empty!")
        elif len(username.get()) > 10:
            messagebox.showinfo("Username too long", "Username shall contain a maximum of 10 characters!")
        elif self._check_special_characters(username.get()):
            # check password match
            if password_1.get() != password_2.get():
                messagebox.showinfo("Passwords do not match", "Passwords must match!")
            else:
                return True
            
    def _check_special_characters(self, username: str):
        """Controls username based on the current rule"""
        allowed_chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        special_characters = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*',
                              '+', ',', '-', '.', '/', ':', ';', '<', '=', '>',
                              '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|',
                              '}', '~', 'ö', 'ä', 'ü', 'ß']
        for letter in username:
            if letter.upper() not in allowed_chars:
                messagebox.showinfo("Forbidden", "Only englsih alphabet characters are allowed!")
                return False
        return True

    def _hash_user_password(self, password: tk.StringVar) -> str:
        """Hashes the passwrod of the user"""
        hashed_pw = password.get()
        return hashed_pw
    
    def _empty_entry_fields(self):
        """Empties all entry fields"""
        self.username_entry.delete(0,tk.END)
        self.password_entry_1.delete(0,tk.END)
        self.password_entry_2.delete(0,tk.END)

def mock_functon():
    print("MOCK")

if __name__ == '__main__':
    a = MainApp(mock_functon)
    a.mainloop()