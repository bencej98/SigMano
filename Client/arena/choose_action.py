import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from tkinter import messagebox

class ActionApp(tk.Tk):

    def __init__(self, get_action_payload, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.frame_width = 400
        self.frame_height = 400
        self.resizable(False, False)
        self.action_payload = get_action_payload
        # fonts
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.label_font = tkfont.Font(family='Arial', size=14)
        self.button_font = tkfont.Font(family='Helvetica', size=12, weight="bold")

        self.geometry("400x400")
        self.title("Sigmano War")
        # screen opens in the middle
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width/2) - (self.frame_width/2)
        y = (screen_height/2) - (self.frame_height/1)
        # self.geometry('%dx%d+%d+%d' % (self.frame_width, self.frame_height, x, y))
        self.geometry('%dx%d+%d+%d' % (self.frame_width, self.frame_height, 0, 300))

        # stack frames onto each other in container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # create a frame dict. and put each page into it
        self.frames = {}
        # create sub-frame and place it into self.frames
        frame = ChooseAction(action_payload=self.action_payload, parent=container, controller=self)
        self.frames[ChooseAction.__name__] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("ChooseAction")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class ChooseAction(tk.Frame):

    def __init__(self, action_payload, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(background="skyblue")
        self.controller = controller
        title_label = tk.Label(self, text="Choose action", font=self.controller.title_font)
        title_label.pack(side="top", fill="x", pady=10)
        self.current_action = None
        self.action_payload = action_payload

        # buttons
        add_action = tk.Button(self, text="Add", background="green", fg="white",
                    command=self.add_action, font=self.controller.button_font, width=5)
        remove_action = tk.Button(self, text="Remove", background="red", fg="white",
                    command=self.remove_action, font=self.controller.button_font, width=5)
        fight_button = tk.Button(self, text="Fight", background="orange", fg="white",
            command=lambda: self.fight(), font=self.controller.button_font, width=5)
        
        # option menu
        default_value = tk.StringVar()
        default_value.set("Please Choose")
        self.option_menu = tk.OptionMenu(self, default_value, "rock", "paper", "scissor", command=self.save_chosen_action)

        # treeview
        columns = ('actions')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        # headings
        self.tree.heading('actions', text='Actions')

        # scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        fight_button.pack()
        remove_action.pack(ipady=10, ipadx=10, pady=10)
        add_action.pack(ipady=10, ipadx=10, pady=10)
        self.option_menu.pack()
        self.tree.pack()
        scrollbar.place(x=285, y=260, height=140)

    def fight(self) -> dict:
        """ Starts fight - returns a dictionary containing fight actions """
        fight_data = {"type": "Action", "payload": []}
        if len(self.tree.get_children()) == 10:
            for line in self.tree.get_children():
                for value in self.tree.item(line)['values']:
                    fight_data["payload"].append(value)

            messagebox.showinfo("FIGHT", "You are going to fight!")
            print("Returns choosed actions...")
            print("Choose actions:", fight_data)
            # self.destroy_frame(self._destroy_action_frame)
            # self._get_action_payload()
            self.action_payload(fight_data)
            self.controller.destroy()

        else:
            messagebox.showinfo("Choose action", "You don't have anough action to fight.\n Choose 10 action.")

    # def _get_action_payload(self, payload):
    #     return payload

    def save_chosen_action(self, action):
        """ Saves the chosen action to a variable """
        self.current_action = action

    def add_action(self):
        """ Adds saved action to tree """
        number_of_added_items = len(self.tree.get_children())
        if self.current_action == None or self.current_action == "Please Choose":
            messagebox.showinfo("Choose", "Choose an action!")
            return
        else:
            item_count = number_of_added_items
            if item_count >= 10:
                messagebox.showinfo("Full", "Can't add any more action.")
            else:
                self.tree.insert('', tk.END, values=self.current_action)

    def remove_action(self):
        """ Removes action that has been seleced """
        if self.tree.selection() != (): # eg.: () or ('I003',)
            selected_item = self.tree.selection()[0]
            self.tree.delete(selected_item)
        else:
            messagebox.showinfo("No item selected", "Select an item to remove.")

if __name__ == '__main__':
    app = ActionApp()
    app.mainloop()