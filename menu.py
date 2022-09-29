from tkinter import *


class _ListenerMenu(Menu):
    def __init__(self, master):
        super().__init__(master, tearoff=False)

        self.__listeners = dict()

    def _call_listeners(self, event):
        if event in self.__listeners:
            for listener in self.__listeners[event]:
                listener()

    def add_btn(self, name, label, *args, **kwargs):
        self.add_command(label=label, command=lambda: self._call_listeners(name), *args, **kwargs)

    def add_listener(self, event, callback):
        if event not in self.__listeners:
            self.__listeners[event] = list()
        self.__listeners[event].append(callback)


class BasicMenu(Menu):
    def __init__(self, master):
        super().__init__(master, tearoff=False)
        self.listener = None

    def add_btn(self, name, label, *args, **kwargs):
        self.add_command(label=label, command=lambda: self.__call_listener(name), *args, **kwargs)

    def attach_listener(self, listener):
        self.listener = listener

    def __call_listener(self, event):
        if self.listener is not None:
            self.listener(event)


class AppMenu(_ListenerMenu):
    def __init__(self, master):
        super().__init__(master)

        filemenu = BasicMenu(self)
        filemenu.attach_listener(self._call_listeners)
        
        filemenu.add_btn('new', 'New File')
        filemenu.add_btn('open', 'Open')
        filemenu.add_btn('save', 'Save')
        filemenu.add_btn('save_as', 'Save As')
        filemenu.add_btn('exit', 'Exit')
        
        snippets_menu = BasicMenu(self)
        snippets_menu.add_btn('email','E-Mail')
        snippets_menu.attach_listener(self._call_listeners)

        self.add_cascade(label="File", menu=filemenu)
        self.add_cascade(label="Snippets", menu=snippets_menu)


class ContextMenu(_ListenerMenu):
    def __init__(self, master):
        super().__init__(master)

        self.add_btn('cut', 'Cut')
        self.add_btn('copy', 'Copy')
        self.add_btn('paste', 'Paste')
