import tkinter as tk
from tkinter import ttk

class ToolTip():
    '''
    Custom Tooltips, easy to use, specify widget and text as positional arguments\n
    Additional Arguments:\n
    triggerkey - Which key triggers the placeholder\n
    releasekey - Which key hides the placeholder\n
    bg - Background color of tooltip window(default-yellow-ish), accepts hex and standard colors\n
    fg - Foreground color/Font color of the text, accepts hex and standard colors\n
    fadeout - Default set to 'enabled', set to 'disabled' to disable fadeout or tooltip\n
    ISSUE: What if user want it on left side?
    '''

    def __init__(self, widget, text, triggerkey='<Enter>', releasekey='<Leave>', bg='#ffffe0', fg='black', fadeout='enabled'):
        # basic widget attributes
        self.widget = widget
        self.text = text
        self.bg = bg
        self.fg = fg
        self.fadeout = fadeout

        # making the tooltip
        self.master = tk.Toplevel(bg=self.bg)
        self.master.attributes('-alpha', 0)  # hide the window
        self.master.overrideredirect(1)
        self.master.attributes('-topmost', True)
        self.frame = tk.Frame(self.master, bg=self.bg, highlightbackground="black",
                              highlightcolor="black", highlightthickness=1)
        self.frame.pack(expand=1, fill='x')
        self.label = tk.Label(self.frame, text=self.text,
                              bg=self.bg, justify=tk.LEFT, fg=self.fg)
        self.label.grid(row=0, column=0)

        # widget binding
        self.widget.bind(triggerkey, self.add)
        self.widget.bind(releasekey, self.remove)
        self.widget.bind('<ButtonPress>', self.remove)

        # reference to window status
        self.hidden = True

    def add(self, event):
    
        # calculating offset
        offset_x = event.widget.winfo_width() + 2
        offset_y = int((event.widget.winfo_height() -
                        self.widget.winfo_height())/2)
        # get geometry
        w = self.label.winfo_width() + 10
        h = self.label.winfo_height() + 2
        self.x = event.widget.winfo_rootx() + offset_x
        self.y = event.widget.winfo_rooty() + offset_y
        # apply geometry
        self.master.geometry(f'{w}x{h}+{self.x}+{self.y}')
        # bringing the visibility of the window back
        self.master.attributes('-alpha', 1)
        self.hidden = False  # setting status to false

    def remove(self, *args):
        if self.fadeout == 'enabled':  # if fadeout enabled

            if not self.hidden:  # if window is not hidden
                alpha = self.master.attributes('-alpha')
                if alpha > 0:
                    alpha -= 0.10
                    self.master.attributes('-alpha', alpha)
                    self.master.after(25, self.remove)

            else:
                self.master.attributes('-alpha', 0)  # hide the window

        elif self.fadeout == 'disabled':  # if fadeout disabled
            if not self.hidden:
                self.master.attributes('-alpha', 0)
                self.hidden = True

        else:
            raise tk.TclError('Unknown value for option -fadeout')

