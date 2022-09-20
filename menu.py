from tkinter import *


class _ListenerMenu(Menu):
    def __init__(self, master):
        super().__init__(master, tearoff=False)

        self.__listeners = dict()

    def _call_listeners(self, event):
        if event in self.__listeners:
            for listener in self.__listeners[event]:
                listener()

    def add_listener(self, event, callback):
        if event not in self.__listeners:
            self.__listeners[event] = list()
        self.__listeners[event].append(callback)


class BasicMenu(Menu):
    def __init__(self, master):
        super().__init__(master, tearoff=False)
        self.listener = None

    def add(self, name, label, *args, **kwargs):
        self.add_command(label=label, command=lambda: self.__call_listener(name), *args, **kwargs)

    def attatch_listener(self, listener):
        self.listener = listener

    def __call_listener(self, event):
        if self.listener is not None:
            self.listener(event)


class AppMenu(_ListenerMenu):
    def __init__(self, master):
        super().__init__(master)

        filemenu = BasicMenu(self)
        filemenu.attatch_listener(self._call_listeners)

        filemenu.add('open', 'Open')
        filemenu.add('save', 'Save')
        filemenu.add('save_as', 'Save As')
        filemenu.add('exit', 'Exit')

        self.add_cascade(label="File", menu=filemenu)


class ContextMenu(_ListenerMenu):
    def __init__(self, master):
        super().__init__(master)

        clickmenu = BasicMenu(master)
        clickmenu.attatch_listener(self._call_listeners)

        clickmenu.add('cut', 'Cut')
        clickmenu.add('copy', 'Copy')
        clickmenu.add('paste', 'Paste')