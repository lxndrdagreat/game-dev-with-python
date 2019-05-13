import tkinter as tk

class just_kidding(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master        
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.message = tk.Label(self, text='just kidding', font=('Helvetica Neue', 32))
        self.message.pack(side='top')

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('500x200')
    root.title('tkinter...')
    root.resizable(0, 0)
    app = just_kidding(master=root)
    app.mainloop()
