import tkinter as tk
from tkinter import colorchooser, filedialog
from tkfontchooser import askfont
from tkinter import ttk
from PIL import ImageGrab, ImageTk

class CodePreview:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Preview")

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill='both', expand=True)

        self.text_frame = tk.Frame(self.main_frame)
        self.text_frame.pack(side='left', fill='both', expand=True)

        self.text = tk.Text(self.text_frame, wrap='word', font=("JetBrains Mono", 12))
        self.text.pack(fill='both', expand=True)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(fill='both', padx=10, pady=10)

        self.font_button = tk.Button(self.button_frame, text="Choose Font", command=self.choose_font, width=15, height=1)
        self.font_button.grid(row=0, column=0, pady=2, sticky='w')

        self.font_info = tk.StringVar()
        self.font_info_label = tk.Label(self.button_frame, textvariable=self.font_info)
        self.font_info_label.grid(row=0, column=1, padx=2, pady=2, sticky='w')

        self.color_button = tk.Button(self.button_frame, text="Choose Color", command=self.choose_color, width=15, height=1)
        self.color_button.grid(row=1, column=0, pady=2, sticky='w')

        self.color_info = tk.StringVar()
        self.color_info_label = tk.Label(self.button_frame, textvariable=self.color_info)
        self.color_info_label.grid(row=1, column=1, padx=2, pady=2, sticky='w')

        self.create_menu()

        self.dark_theme = False
        self.change_theme(theme='light')

        self.text.bind("<<Selection>>", self.update_info_from_selection)

    def create_menu(self):
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Take Screenshot", command=self.take_screenshot)

        self.theme_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Theme", menu=self.theme_menu)
        self.theme_menu.add_command(label="Dark Theme", command=lambda: self.change_theme('dark'))
        self.theme_menu.add_command(label="Light Theme", command=lambda: self.change_theme('light'))

    def get_current_tags(self):
        try:
            selected_text = self.text.tag_ranges(tk.SEL)
            if selected_text:
                tags = self.text.tag_names(selected_text[0])
                return tags
            return []
        except tk.TclError:
            return []

    def choose_color(self):
        current_tags = self.get_current_tags()
        initial_color = '#000000'
        for tag in current_tags:
            if tag.startswith('colored_'):
                initial_color = tag.split('_')[1]
                break

        color = colorchooser.askcolor(initialcolor=initial_color)[1]
        if color:
            self.change_text_color(color)
            self.update_color_info(color)

    def choose_font(self):
        current_tags = self.get_current_tags()
        initial_font = {'family': 'JetBrains Mono', 'size': 12, 'weight': 'normal', 'slant': 'roman'}
        for tag in current_tags:
            if tag.startswith('font_'):
                font_info = tag.split('_')[1:-1]
                if len(font_info) == 4:
                    initial_font = {'family': font_info[0], 'size': int(font_info[1]), 'weight': font_info[2], 'slant': font_info[3]}
                break

        font = askfont(self.root, **initial_font)
        if font:
            font_tuple = (font['family'], font['size'], font['weight'], font['slant'])
            self.change_text_font(font_tuple)
            self.update_font_info(font)

    def change_text_color(self, color):
        try:
            selected_text = self.text.tag_ranges(tk.SEL)
            if selected_text:
                tag_name = f"colored_{color}_{self.text.index(tk.INSERT)}"
                self.text.tag_add(tag_name, *selected_text)
                self.text.tag_configure(tag_name, foreground=color)
        except tk.TclError:
            pass

    def change_text_font(self, font_tuple):
        try:
            selected_text = self.text.tag_ranges(tk.SEL)
            if selected_text:
                tag_name = f"font_{font_tuple[0]}_{font_tuple[1]}_{font_tuple[2]}_{font_tuple[3]}_{self.text.index(tk.INSERT)}"
                self.text.tag_add(tag_name, *selected_text)
                self.text.tag_configure(tag_name, font=font_tuple)
        except tk.TclError:
            pass

    def update_font_info(self, font):
        font_info = f"Font: {font['family']}, Size: {font['size']}, Weight: {font['weight']}, Slant: {font['slant']}"
        self.font_info.set(font_info)

    def update_color_info(self, color):
        color_info = f"Color: {color}"
        self.color_info.set(color_info)
        self.color_info_label.config(foreground=color)

    def update_info_from_selection(self, event=None):
        current_tags = self.get_current_tags()
        initial_font = {'family': 'JetBrains Mono', 'size': 12, 'weight': 'normal', 'slant': 'roman'}
        initial_color = '#000000'

        for tag in current_tags:
            if tag.startswith('font_'):
                font_info = tag.split('_')[1:-1]
                if len(font_info) == 4:
                    initial_font = {'family': font_info[0], 'size': int(font_info[1]), 'weight': font_info[2], 'slant': font_info[3]}
            elif tag.startswith('colored_'):
                initial_color = tag.split('_')[1]

        self.update_font_info(initial_font)
        self.update_color_info(initial_color)

    def take_screenshot(self):
        x = self.root.winfo_rootx() + self.text.winfo_x()
        y = self.root.winfo_rooty() + self.text.winfo_y()
        x1 = x + self.text.winfo_width()
        y1 = y + self.text.winfo_height()

        image = ImageGrab.grab().crop((x, y, x1, y1))
        
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            image.save(file_path)

    def change_theme(self, theme):
        if theme == 'dark':
            bg_color = '#1e1e1e'
            fg_color = '#dcdcdc'
            button_frame_bg_color = '#3e3e3e'
            buttons_bg_color = '#262626'
            buttons_fg_color = 'white'
        elif theme == 'light':
            bg_color = '#ffffff'
            fg_color = '#000000'
            button_frame_bg_color = '#dcdcdc'
            buttons_bg_color = '#cfcfcf'
            buttons_fg_color = 'black'

        self.text.config(bg=bg_color, fg=fg_color, insertbackground=fg_color)
        self.font_info_label.config(bg=button_frame_bg_color, fg=fg_color)
        self.color_info_label.config(bg=button_frame_bg_color, fg=fg_color)
        self.button_frame.config(bg=button_frame_bg_color)
        self.font_button.config(bg=buttons_bg_color, fg=buttons_fg_color)
        self.color_button.config(bg=buttons_bg_color, fg=buttons_fg_color)
        self.main_frame.config(bg=bg_color)
        self.text_frame.config(bg=bg_color)
        self.root.config(bg=bg_color)

if __name__ == "__main__":
    root = tk.Tk()
    app = CodePreview(root)
    root.mainloop()
