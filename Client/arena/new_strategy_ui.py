import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from tkinter import messagebox
from tkinter.colorchooser import askcolor

class ActionApp(tk.Tk):

    def __init__(self, get_action_payload, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.frame_width = 400
        self.frame_height = 580
        self.resizable(False, False)
        self.action_payload = get_action_payload
        self.background_color = "#535356"
        self.points_frame_background = "#3c3c3c"
        self.remove_button_background = "#a40c13"
        self.font_color = "white"
        self.wm_iconbitmap('logo/sigma_logo.ico')

        # fonts
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.label_font = tkfont.Font(family='Arial', size=11, weight="bold")
        self.button_font = tkfont.Font(family='Helvetica', size=12, weight="bold")

        self.geometry("400x400")
        self.title("Sigmano War")
        # screen opens in the middle
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width/2) - (self.frame_width/2)
        y = (screen_height/2) - (self.frame_height/1)
        self.geometry('%dx%d+%d+%d' % (self.frame_width, self.frame_height, x, (y + 200)))

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

    def _get_frame_width(self):
        return self.frame_width


class ChooseAction(tk.Frame):

    def __init__(self, action_payload, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(background=controller.background_color)
        self.controller = controller
        self.current_action = None
        self.action_payload = action_payload
        self.total_points = 0
        self.action_point_frame_background = "#3c3c3c"
        self.chosen_color = None
        # self.ALLOWED_COLORS = ['#8000000', '#FF0000', '#FF4500', '#FFD700', '#008000', '#008080', '#000080']
        self.ALLOWED_COLORS = ['Maroon', 'Red', 'Orange', 'Gold', 'Green', 'Teal', 'Navy']
        # self.ALLOWED_COLORS = ['red']
        self.action_points = {
            "Runaway": 2,
            "Approach": 1,
            "Defend": 1
        }
        self.event_points = {
            "Fight nearby": 2,
            "Gnomes in vicinity": 1,
        }

        # style
        self.someStyle=ttk.Style()
        self.someStyle.configure('my.TMenubutton',font=('Futura',20))

        # title label
        title_label = tk.Label(self, text="Strategy", font=self.controller.title_font, background="#6b0404", fg=self.controller.font_color)
        title_label.pack(side="top", fill="x", pady=10)
        # tree frame
        tree_frame = tk.Frame(self, height=5, width=1, padx=3)
        tree_frame.pack(side=tk.BOTTOM, padx=10, pady=10)
        # button frame
        button_frame = tk.Frame(self, height=5, width=10, background=self.controller.background_color)
        button_frame.pack(padx=10, pady=10)
        # action point frame
        action_point_frame = tk.Frame(self, height=5, width=10, background=self.action_point_frame_background)
        action_point_frame.pack(padx=10, pady=10)
        # color frame
        color_frame = tk.Frame(self, height=5, width=10, background=self.controller.background_color)
        color_frame.pack(padx=10, pady=10)
        # label frame
        label_frame = tk.Frame(self, height=5, width=10, background=self.controller.background_color)
        label_frame.pack(padx=10, pady=10)

        # option menu frame
        option_meun_frame = tk.Frame(self, height=5, width=10, background=self.controller.background_color)
        option_meun_frame.pack(padx=10, pady=10)
        # labels
        event_label = tk.Label(label_frame, text="Choose event", fg=self.controller.font_color, background=self.controller.background_color, font=self.controller.label_font)
        action_label = tk.Label(label_frame, text="Choose action", fg=self.controller.font_color, background=self.controller.background_color, font=self.controller.label_font)
        self.action_points_label = tk.Label(action_point_frame, text="0", fg=self.controller.font_color, background=self.controller.points_frame_background, font=self.controller.label_font)
        self.points_label = tk.Label(action_point_frame, text="points", fg=self.controller.font_color, background=self.controller.points_frame_background, font=self.controller.label_font)
        # buttons
        add_action = tk.Button(button_frame, text="Add", background="#1c1c24", fg=self.controller.font_color,
                    command=self.add_action, font=self.controller.button_font, width=5)
        remove_action = tk.Button(button_frame, text="Remove", background=self.controller.remove_button_background, fg=self.controller.font_color,
                    command=self.remove_action, font=self.controller.button_font, width=5)
        fight_button = tk.Button(button_frame, text="Fight", background="#040404", fg=self.controller.font_color,
            command=lambda: self.fight(), font=self.controller.button_font, width=5)
        calculate_points_button = tk.Button(action_point_frame, text="Calculate", fg=self.controller.font_color, background=self.controller.background_color, font=self.controller.label_font, command=self.calculate_action_points)
        # color picker
        choose_color_label = tk.Button(color_frame, text="Choose color", fg=self.controller.font_color, background=self.controller.background_color, font=self.controller.label_font, command=self._open_colorchooser)
        
        # event option menu
        default_value_event = tk.StringVar()
        default_value_event.set("Please Choose")
        self.option_menu_event = tk.OptionMenu(option_meun_frame, default_value_event, "Fight nearby",
                                                                                        "Gnomes in vicinity",
                                                                                        command=self.save_chosen_event)
        # action option menu
        default_value_action = tk.StringVar()
        default_value_action.set("Please Choose")
        self.option_menu_action = tk.OptionMenu(option_meun_frame, default_value_action,"Approach",
                                                                                        "Runaway",
                                                                                        "Defend",
                                                                                        command=self.save_chosen_action)

        # treeview
        columns = ('events', 'actions')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=5)
        self.tree.column('events', width=100)
        self.tree.column('actions', width=140)
        # headings
        self.tree.heading('events', text='Events')
        self.tree.heading('actions', text='Actions')

        # scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # choose color section
        choose_color_label.pack(side="left", fill="x", pady=10, padx=35)
        # labels
        action_label.pack(side="left", fill="x", pady=10, padx=35)
        event_label.pack(side="right", fill="x", pady=10, padx=35)
        self.points_label.pack(side="right", fill="x", pady=10, padx=35)
        self.action_points_label.pack(side="right", fill="x", pady=10, padx=35)
        # buttons
        fight_button.pack(side=tk.LEFT, ipady=10, ipadx=10, pady=10)
        remove_action.pack(side=tk.LEFT, ipady=10, ipadx=10, pady=10)
        add_action.pack(side=tk.LEFT, ipady=10, ipadx=10, pady=10)
        calculate_points_button.pack(side="right", fill="x", pady=10, padx=35)
        # option menus
        self.option_menu_action.pack(side=tk.LEFT, padx=10, pady=10)
        self.option_menu_event.pack(side=tk.LEFT, padx=10, pady=10)
        self.tree.pack(side=tk.TOP)
        scrollbar.place(x=380, y=260, height=140)

    # def _get_selected_color(self):
    #     """ Gets & saves the pciked color """
    #     ALLOWED_COLORS = ['#FF0000', '#00FF00', '#0000FF']
    #     self.grab_set()
    #     self.chosen_color = askcolor(parent=self, color=ALLOWED_COLORS)[1]
    #     self.grab_release()

    def _set_selected_color(self, color, top_level: tk.Toplevel):
        """ Saves the selected color """
        self.chosen_color = color
        top_level.withdraw()

    def _open_colorchooser(self):
        """ Displays available colors """
        top_level = tk.Toplevel(self)
        # screen opens in the middle
        self.top_lvl_frame_width = 400
        self.top_lvl_frame_height = 580
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width/2) - (self.top_lvl_frame_width/2)
        y = (screen_height/2) - (self.top_lvl_frame_height/1)
        top_level.geometry('%dx%d+%d+%d' % (350, 200, x, (y + 50)))

        top_level.attributes('-topmost', True)
        for color in self.ALLOWED_COLORS:
            button = tk.Button(top_level, bg=color, width=4,
                               command=lambda c=color: self._set_selected_color(c, top_level))
            button.pack(side=tk.LEFT, padx=5, pady=5)

    def _color_choosed(self) -> bool:
        """ Checks if user has choosen color """
        if self.chosen_color is None:
            return False
        return True

    def fight(self) -> dict:
        """ Starts fight - returns a dictionary containing fight actions """
        fight_data = {"Type": "Behavior", "Payload": []} # e.g.: "Payload": [{"Attack": "If weaker opponent"}, {"Defend": "If fight nearby"}]
        current_action_pair = {} # e.g.: {"Event": "...","Action": "..."},{"Event": "...","Action": "..."}
        current_action = None
        current_event = None

        if self.calculate_action_points(): # calculate points before fight
            if self.total_points >= 2:
                    for line in self.tree.get_children():
                        counter = 0
                        for value in self.tree.item(line)['values']:
                            if counter % 2 == 0:
                                current_action = value
                            else:
                                current_event = value
                                current_action_pair["Action"] = current_action
                                current_action_pair["Event"] = current_event
                                # current_action_pair[current_action] = current_event
                                fight_data["Payload"].append(current_action_pair)
                            counter += 1

                    if not self._color_choosed():
                        messagebox.showinfo("Color", "Choose a color!")
                        return

                    messagebox.showinfo("FIGHT", "You are going to fight!")
                    print("Returns choosed actions...")
                    print("Choosed actions:", fight_data)
                    self.action_payload(fight_data, self.chosen_color)
                    self.controller.destroy()

            else:
                messagebox.showinfo("Choose action", "You don't have anough action points to fight" \
                                    "\nChoose one action pair at least.")

    def save_chosen_action(self, action):
        """ Saves the chosen action to a variable """
        self.current_action = action
    def save_chosen_event(self, event):
        """ Saves the chosen action to a variable """
        self.current_event = event

    def add_action(self):
        """ Adds saved action to tree """
        number_of_added_items = len(self.tree.get_children())
        if self.current_action == None or self.current_action == "Please Choose":
            messagebox.showinfo("Choose", "Choose an action event pair!")
            return
        else:
            if number_of_added_items >= 20:
                messagebox.showinfo("Full", "Can't add any more action." \
                                    "\nMaximum number of actions: 20")
            else:
                if self.action_pair_exists():
                    messagebox.showinfo("Already exists", "The action event pair already added...")
                else:
                    self.tree.insert('', tk.END, values=(self.current_action, self.current_event, ))

    def action_pair_exists(self) -> bool:
        """ Checks if current action event pair already added """
        current_action = None
        current_event = None
        for line in self.tree.get_children():
            counter = 0
            for value in self.tree.item(line)['values']:
                if counter % 2 == 0:
                    current_action = value
                else:
                    current_event = value
                    if self.current_event == current_event and self.current_action == current_action:
                        return True
                counter += 1
        return False

    def remove_action(self):
        """ Removes action that has been seleced """
        if self.tree.selection() != (): # eg.: () or ('I003',)
            selected_item = self.tree.selection()[0]
            self.tree.delete(selected_item)
        else:
            messagebox.showinfo("No item selected", "Select an action event pair to remove.")

    def calculate_action_points(self) -> bool:
        """Calculates the action an even points, returns false if points are too much."""
        current_event_points = 0
        current_action_points = 0
        for line in self.tree.get_children():
            counter = 0
            for value in self.tree.item(line)["values"]:
                if counter % 2 == 0:
                    current_action_points += self.action_points[value]
                else:
                    current_event_points += self.event_points[value]
                counter += 1

        self.total_points = current_action_points + current_event_points
        self.action_points_label.config(text=self.total_points, fg=self.controller.font_color)
        if self.total_points > 10:
            self.action_points_label.config(fg="red")
            messagebox.showinfo("Too much point!", "You can have a maximum of 10 points!")
            return False
        return True

def mock_func(action_payload):
    print("MOCK'S action payload: ", end='')
    print(action_payload)

if __name__ == '__main__':
    a = ActionApp(mock_func)
    a.mainloop()