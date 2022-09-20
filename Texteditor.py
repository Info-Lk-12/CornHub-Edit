from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog


file = None

def openFile():
    global file
    file = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')], defaultextension="*.txt")
    if file != '':
        with open(file, 'r') as f:
            data = f.read()
        text_area.delete('1.0', END)
        text_area.insert(END, data)

def saveAsFile():
    global file
    file = filedialog.asksaveasfilename(filetypes=[('Text Files', '*.txt')], defaultextension="*.txt")
    if file != '':
        with open(file, 'w') as f:
            data = text_area.get('1.0', END)
            f.write(data)

def saveFile():
    global file
    if file is None:
        saveAsFile()
    else:
        with open(file, 'w') as f:
            data = text_area.get('1.0', END)
            f.write(data)

def clickMenu(event):
    clickmenu.tk_popup(event.x_root, event.y_root)

def cut():
    text = text_area.selection_get()

    start = text_area.index('sel.first')
    end = text_area.index('sel.last')

    text_area.delete(start, end)
    
    root.clipboard_clear()
    root.clipboard_append(text)

def copy():
    text = text_area.selection_get()
    root.clipboard_clear()
    root.clipboard_append(text)

def paste():
    text = root.clipboard_get()
    if text_area.tag_ranges("sel"):
        start = text_area.index('sel.first')
        end = text_area.index('sel.last')
        text_area.delete(start, end)
    text_area.insert(END, text)

    
root = Tk()
root.title('Wort')
root.geometry('960x540')

text_area = ScrolledText(root, height=35, undo=True)
text_area.pack(fill=BOTH, expand=True)

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=False)
filemenu.add_command(label="Open", command=openFile)
filemenu.add_command(label="Save", command=saveFile)
filemenu.add_command(label="Save as", command=saveAsFile)
filemenu.add_command(label="Exit", command=root.destroy)
menubar.add_cascade(label="File", menu=filemenu)

clickmenu = Menu(root, tearoff=False)
clickmenu.add_command(label="Cut", command=cut)
clickmenu.add_command(label="Copy", command=copy)
clickmenu.add_command(label="Paste", command=paste)

root.bind('<Control-s>', lambda e:saveFile())
text_area.bind('<Button-3>', clickMenu)

root.config(menu=menubar)
root.mainloop()

#penis
#lol
