import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
from tkinter import ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.attributes('-type', 'splash')
        self.title('Editor')
        self.geometry("800x600")
        self.folder_path = tk.StringVar()
        self.__build()

    def __build(self):
        # Button to quit the app.
        options_frame = tk.Frame(self)
        options_frame.pack()
        quit_button = tk.Button(options_frame, text="Quit", command=self.destroy)
        quit_button.pack(side=tk.RIGHT)

        help_button = tk.Button(options_frame, text="Help", command=self.open_help)
        help_button.pack(side=tk.LEFT)

        update_button = tk.Button(options_frame, text="Update", command=self.update_docs)
        update_button.pack(side=tk.LEFT)

        # Entry to type search string.
        search_frame = tk.Frame(self)
        search_frame.pack()

        # Button to run main script.
        self.method_box = ttk.Combobox(
            master = search_frame,
            state="readonly",
            values=["Alphabet", "Word frequency", "Neural network"]
        )
        self.method_box.pack(side=tk.LEFT)
        self.method_box.set("Alphabet")
        
        go_button = tk.Button(search_frame, text="Load", command=self.recognize_lang)
        go_button.pack()

        # Text box to display output of main text.
        self.text_box = ScrolledText(
            width=110, borderwidth=2, relief="sunken", padx=20, font=("Helvetica", 15))
        self.text_box.pack()

        # Button to clear the text box display.
        clear_button = tk.Button(
            self, text="Clear", command=lambda: self.text_box.delete("1.0", tk.END))
        clear_button.pack()

    def update_docs(self):
        pass

    def recognize_lang(self):
        file = filedialog.askopenfilename()
        text = open(file).read()
        
        self.print_to_textbox(text)



    def print_to_textbox(self, text):
        self.text_box.delete("1.0", tk.END)
        self.text_box.insert("end", text)

    def open_help(self):
        top = tk.Toplevel()
        #top.geometry("180x100")
        top.attributes('-type', 'splash')
        top.title('Editor')
        l2 = tk.Label(top, text = """

                                """)
        l2.pack()
        quit_button = tk.Button(top, text="Quit", command=top.destroy)
        quit_button.pack(side=tk.BOTTOM)

        top.mainloop()

    def run(self):
        self.mainloop()
