from tkinter import *
from tkinter import messagebox
from tkinter import ttk


def Quit():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # ngat kết nối client
            #client.close()
            messagebox.showinfo('Announce', 'Disconnected from ALL Clients.')
            window.destroy()

def Refresh():
    #update size và arr
    for i in arr:
        list.insert(END, i)

def Active():

    Active_frame.destroy()


window = Tk()
window.title('Server - GOLD EXCHANGE RATE LOOOKUP')
window.geometry('330x450')
window.resizable(0, 0)

size = 0
arr=('1', '2', '2')

Label(window, text = 'Number of connected Clients:', font =('arial', 12, 'italic')).place(x = 0, y = 1)
number = Label(window, text = size, font =('arial', 13), fg = 'tomato').place(x = 219, y = 1)

list = Listbox(window, width = 330, height = 21, font =('arial', 10))
list.place(x = 0, y = 25)

Button(window, width = 8, height = 2, bd = 0, fg = 'white', bg = 'coral', text = 'Refresh', command =  Refresh).place(x = 50, y = 400)
Button(window, width = 8, height = 2, bd = 0, fg = 'white', bg = 'coral', text = 'Quit', command =  Quit).place(x = 200, y = 400)

# Khoi dong
Active_frame = Frame(window)
Active_frame.pack(fill='both', expand=True)

Button(Active_frame, width = 8, height = 2, bd = 0, fg = 'white', bg = 'coral', text = 'A C T I V E', command = Active).place(relx=0.5, rely=0.5, anchor=CENTER)

window.protocol("WM_DELETE_WINDOW", Quit)

window.mainloop()