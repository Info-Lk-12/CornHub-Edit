from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog

from menu import AppMenu, ContextMenu


class CornHubEdit(Tk):
    def __init__(self):
        super().__init__()
        self.title("Cornhub Edit")
        self.geometry("960x540")

        self.text_area = ScrolledText(self, height=35, undo=True)
        self.text_area.pack(fill=BOTH, expand=True)

        self.menu = AppMenu(self)
        self.click_menu = ContextMenu(self.text_area)

        self.config(menu=self.menu)
        self.bind('<Control-s>', lambda e: self.saveFile())
        self.text_area.bind('<Button-3>', self.context_menu)

        self.__init_listeners()

        self.__file = None

    def __init_listeners(self):
        self.menu.add_listener('open', self.openFile)
        self.menu.add_listener('save', self.saveFile)
        self.menu.add_listener('save_as', self.saveAsFile)
        self.menu.add_listener('exit', self.destroy)

        self.click_menu.add_listener('cut', self.cut)
        self.click_menu.add_listener('copy', self.copy)
        self.click_menu.add_listener('paste', self.paste)

    def openFile(self):
        file = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')], defaultextension="*.txt")
        if file != '':
            self.__file = file
            with open(file, 'r') as f:
                data = f.read()
            self.text_area.delete('1.0', END)
            self.text_area.insert(END, data)

    def saveAsFile(self):
        file = filedialog.asksaveasfilename(filetypes=[('Text Files', '*.txt')], defaultextension="*.txt")
        if type(file) is str and file != '':
            self.__file = file
            with open(file, 'w') as f:
                data = self.text_area.get('1.0', END)
                f.write(data)

    def saveFile(self):
        if self.__file is None:
            self.saveAsFile()
        else:
            with open(self.__file, 'w') as f:
                data = self.text_area.get('1.0', END)
                f.write(data)

    def context_menu(self, event):
        self.click_menu.tk_popup(event.x_root, event.y_root)

    def cut(self):
        text = self.text_area.selection_get()

        start = self.text_area.index('sel.first')
        end = self.text_area.index('sel.last')

        self.text_area.delete(start, end)
        
        self.clipboard_clear()
        self.clipboard_append(text)


    def copy(self):
        text = self.text_area.selection_get()
        self.clipboard_clear()
        self.clipboard_append(text)

    def paste(self):
        text = self.clipboard_get()
        if self.text_area.tag_ranges("sel"):
            start = self.text_area.index('sel.first')
            end = self.text_area.index('sel.last')
            self.text_area.delete(start, end)
        self.text_area.insert(END, text)


if __name__ == '__main__':
    app = CornHubEdit()
    app.mainloop()