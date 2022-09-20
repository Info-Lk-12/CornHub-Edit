from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog

from menu import AppMenu, ContextMenu


class CornHubEdit(Tk):
    def __init__(self):
        super().__init__("CornHub")
        self.title("Cornhub Edit")
        self.geometry("960x540")

        self.text_area = ScrolledText(self, height=35, undo=True)
        self.text_area.pack(fill=BOTH, expand=True)

        self.config(menu=AppMenu(self))
        self.bind('<Control-s>', lambda e: self.saveFile())
        self.text_area.bind('<Button-3>', ContextMenu(self.text_area))

        self.__file = None

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
        if file != '':
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

    def clickMenu(event):
        clickmenu.tk_popup(event.x_root, event.y_root)


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