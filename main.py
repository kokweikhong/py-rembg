import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, Scrollbar, Menu, PhotoImage


class SaveLocationFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill="x", expand=True)
        self.save_location = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):

        ttk.Label(self, text="Output Directory:", style="Normal.TLabel").pack(
            side="top", anchor=tk.NW)

        self.save_location_entry = ttk.Entry(
            self, textvariable=self.save_location).pack(side=tk.LEFT, anchor=tk.NW, fill="x", expand=True)

        ttk.Separator(self, orient="vertical").pack(side=tk.LEFT, anchor=tk.NW,
                                                    padx=10, fill="y")

        ttk.Button(self, text="browse",
                   command=self.select_save_location_dir).pack(side=tk.LEFT, anchor=tk.NW)

    def select_save_location_dir(self):
        save_location = filedialog.askdirectory(
            title="Select Save Location")
        self.save_location.set(save_location)


class ImagesFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Selected Images:", style="Normal.TLabel").pack(
            side="top", anchor=tk.NW)

        self.frame1 = ttk.Frame(self)
        self.frame1.pack(fill="both", expand=True)

        self.frame_listbox = ttk.Frame(self.frame1)
        self.frame_listbox.pack(fill="both", expand=True,
                                side="left", anchor=tk.NW)

        self.listbox = tk.Listbox(self.frame_listbox, selectmode=tk.SINGLE)
        self.listbox.bind('<<ListboxSelect>>', self.image_selected)

        scrollbar_x = Scrollbar(self.frame_listbox)

        scrollbar_x.config(command=self.listbox.xview, orient="horizontal")

        scrollbar_y = Scrollbar(self.frame_listbox)

        scrollbar_y.config(command=self.listbox.yview)

        self.listbox.config(yscrollcommand=scrollbar_y.set)
        self.listbox.config(xscrollcommand=scrollbar_x.set)

        # pack sequence
        scrollbar_x.pack(side="bottom", fill="x")
        self.listbox.pack(fill="both", expand=True, side="left", anchor=tk.NW)
        scrollbar_y.pack(side="right", fill="y")

        ttk.Separator(self.frame1, orient="vertical").pack(
            side="left", fill="y", padx=10, pady=10)

        # self.canvas = tk.Listbox(self.frame1)
        # self.canvas.pack(fill="both", expand=True, side="left")

        self.frame_image = ttk.Frame(self, borderwidth=2, relief=tk.SUNKEN)
        self.frame_image.pack(side=tk.LEFT, fill="x")

        ttk.Button(self, text="Browse Images", command=self.select_images).pack(
            side="left", pady=10)

        ttk.Separator(self, orient="vertical").pack(
            side="left", fill="y", padx=10, pady=10)

        self.button_convert = ttk.Button(self, text="Convert")
        self.button_convert.pack(side="left", pady=10)

    def image_selected(self, event):
        w = event.widget
        idx = w.curselection()[0]
        value = w.get(idx)

        self.frame_image.picture = PhotoImage(file=value)
        self.frame_image.label = ttk.Label(
            self.frame_image, image=self.frame_image.picture)
        self.frame_image.label.pack()

    def select_images(self):
        filenames = filedialog.askopenfilenames(title="Select Image Files")
        self.listbox.delete(0, tk.END)
        for file in filenames:

            self.listbox.insert(tk.END, file)
        print(filenames)


class LogsFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)
        # self.logs = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        # self.logs = tk.Text(self)
        self.logs = scrolledtext.ScrolledText(self, height=8)

        self.logs.pack(fill="both", expand=True)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True, padx=20, pady=20)

        self.create_widgets()
        self.images_frame.button_convert["command"] = self.convert_images

    def create_widgets(self):
        self.save_location_frame = SaveLocationFrame(master=self)
        self.images_frame = ImagesFrame(master=self)
        self.logs_frame = LogsFrame(master=self)

    def convert_images(self):
        # self.logs_frame.logs.delete(0, tk.END)
        try:
            self.logs_frame.logs.delete(0)
        except:
            pass
        files = self.images_frame.listbox.get(0, tk.END)
        for file in files:
            self.logs_frame.logs.insert(tk.END, f"{file}\n")
        # self.logs_frame.logs.insert(tk.END, "bbbb")


class Root(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.default_configuration()
        self.init_menu()
        self.wm_title("Background Remover")
        # self.app = Application(self)
        self.labelStyle = ttk.Style(self).configure(
            "Normal.TLabel", font=('Arial', 11))
        self.config(menu=self.menu)

    def init_menu(self):
        self.menu = Menu(self, tearoff=0)
        filemenu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Exit", command=self.quit)

    def default_configuration(self):
        self.geometry("800x600")
        self.title = "Background Remover"
        self.resizable(False, False)


if __name__ == "__main__":

    root = Root()
    root.title = "aaaa"
    app = Application(root)
    app.mainloop()
