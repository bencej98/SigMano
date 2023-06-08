import tkinter as tk

class MainScreen:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Sigmano War")
        self.root.geometry("400x400")
        self.root.config(bg="skyblue")  
        self.root.resizable(0,0)

    def init_screen(self):
        pass

class LoginScreen(MainScreen):
    def __init__(self,):
        super().__init__()
        self.font_type = "Arial"
        self.font_size = 13

    def setup_layout(self):
        self.root.title("Login Screen")

        # main frame
        frame = tk.Frame(self.root, width=200, height=400, background="skyblue")
        frame.pack(pady=90, ipady=40)

        # username fields
        self.username_label = tk.Label(frame, text="User Name", font=(self.font_type, self.font_size), background="skyblue")
        self.username_label.grid(row=0, column=0, sticky="e")

        username = tk.StringVar()
        self.username_inputfield = tk.Entry(frame, textvariable=username, font=(self.font_type, self.font_size))
        self.username_inputfield.grid(row=0, column=1, padx=10, pady=10)

        # password fields
        self.password_label = tk.Label(frame, text="Password", font=(self.font_type, self.font_size), background="skyblue")
        self.password_label.grid(row=1, column=0, sticky="e")

        password = tk.StringVar()
        self.password_inputfield = tk.Entry(frame, textvariable=password, show='*', font=(self.font_type, self.font_size))
        self.password_inputfield.grid(row=1, column=1, padx=15)

        # login button
        self.login_button = tk.Button(frame, text="Login", command=lambda: self.login(username, password), width=25, height=2, background="MediumTurquoise", fg="white", font=(self.font_type, self.font_size, "bold"))
        self.login_button.grid(row=2, column=0, columnspan=2, pady=15)

        # register button
        self.register_button = tk.Button(frame, text="Register", command=self.open_register_window, width=25, height=2, background="Teal", fg="white", font=(self.font_type, self.font_size, "bold"))
        self.register_button.grid(row=3, column=0, columnspan=2)

        self.root.mainloop()

    def login(self, username, password):
        print("Logging in...")
        print(username.get(), password.get())

    def open_register_window(self):
        print("Opening register window...")


main_screen = LoginScreen()
main_screen.setup_layout()
