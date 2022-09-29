import platform
import threading

from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog

if platform.system() == "Windows":
    from winsound import PlaySound, SND_FILENAME

from menu import AppMenu, ContextMenu


def play_a_sound(*sound):
    def play_win():
        for s in sound:
            PlaySound(s, SND_FILENAME)

    if platform.system() == "Windows":
        threading.Thread(target=play_win, daemon=False).start()


class CornHubEdit(Tk):
    def __init__(self):
        super().__init__()
        self.title("untitled - Cornhub Edit")
        self.geometry("960x540")

        self.text_area = ScrolledText(self, height=35, undo=True)
        self.text_area.pack(fill=BOTH, expand=True)

        self.menu = AppMenu(self)
        self.click_menu = ContextMenu(self.text_area)

        self.config(menu=self.menu)
        self.bind('<Control-s>', lambda e: self.saveFile())

        if platform.system() == "Windows":
            self.iconbitmap('cornhubeditlogofinal.ico')

        self.text_area.bind('<Button-3>', self.context_menu)
        self.__init_listeners()

        self.__file = None
        
        self.check_file = self.text_area.get('1.0', END)

    def __init_listeners(self):
        self.menu.add_listener('new', self.newFile)
        self.menu.add_listener('open', self.openFile)
        self.menu.add_listener('save', self.saveFile)
        self.menu.add_listener('save_as', self.saveAsFile)
        self.menu.add_listener('exit', self.destroy)
        
        self.menu.add_listener('email', lambda: self.text_area.insert(END,'email'))

        self.click_menu.add_listener('cut', self.cut)
        self.click_menu.add_listener('copy', self.copy)
        self.click_menu.add_listener('paste', self.paste)

        self.bind("<Control-n>", self.newFile)
        self.bind("<Control-o>", self.openFile)
        self.bind("<Control-s>", self.saveFile)
        self.bind("<Control-Shift-s>", self.saveAsFile)
        self.bind("<Alt-F4>", self.quit)

        self.bind("<Control-x>", self.cut)
        self.bind("<Control-c>", self.copy)
        self.bind("<Control-v>", self.paste)
    
    def newFile(self, *e):
        if self.check_file != self.text_area.get('1.0', END):
            if askyesno('Close without Save', 'Do you want to close the current file without saving?') == False:
                return
        self.text_area.delete('1.0', END)
        self.check_file = self.text_area.get('1.0', END)
        self.__file = None
        self.title('untitled - Cornhub Edit')
    
    def openFile(self, *e):
        if self.check_file != self.text_area.get('1.0', END):
            if askyesno('Close without Save', 'Do you want to close the current file without saving?') == False:
                return
        file = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')], defaultextension="*.txt")
        if type(file) is str and file != '':
            self.__file = file
            with open(file, 'r') as f:
                data = f.read()
                self.title(f.name + ' - Cornhub Edit')
            self.text_area.delete('1.0', END)
            self.text_area.insert(END, data)
            self.check_file = self.text_area.get('1.0', END)

    def saveAsFile(self, *e):
        file = filedialog.asksaveasfilename(filetypes=[('Text Files', '*.txt')], defaultextension="*.txt")
        if type(file) is str and file != '':
            self.__file = file
            self.title(file + ' - Cornhub Edit')
            with open(file, 'w') as f:
                data = self.text_area.get('1.0', END)
                f.write(data)
                self.check_file = self.text_area.get('1.0', END)

    def saveFile(self, *e):
        if self.__file is None:
            self.saveAsFile()
        else:
            with open(self.__file, 'w') as f:
                data = self.text_area.get('1.0', END)
                f.write(data)
                self.check_file = self.text_area.get('1.0', END)

    def context_menu(self, event):
        self.click_menu.tk_popup(event.x_root, event.y_root)

    def cut(self, *e):
        text = self.text_area.selection_get()

        start = self.text_area.index('sel.first')
        end = self.text_area.index('sel.last')

        self.text_area.delete(start, end)
        
        self.clipboard_clear()
        self.clipboard_append(text)


    def copy(self, *e):
        text = self.text_area.selection_get()
        self.clipboard_clear()
        self.clipboard_append(text)

    def paste(self, *e):
        text = self.clipboard_get()
        if self.text_area.tag_ranges("sel"):
            start = self.text_area.index('sel.first')
            end = self.text_area.index('sel.last')
            self.text_area.delete(start, end)
        self.text_area.insert(END, text)


if __name__ == '__main__':
    play_a_sound('phintro.wav')
    app = CornHubEdit()
    app.mainloop()
    play_a_sound('phoutro.wav')
