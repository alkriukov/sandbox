import os
import tkinter as Tk


def form_menu(menu_frame):
    file_btn = Tk.Button(text='New', master = menu_frame)
    file_btn.pack(side=Tk.LEFT)
    file_btn = Tk.Button(text='Open', master = menu_frame)
    file_btn.pack(side=Tk.LEFT)
    file_btn = Tk.Button(text='Save', master = menu_frame)
    file_btn.pack(side=Tk.LEFT)
    file_btn = Tk.Button(text='Save As', master = menu_frame)
    file_btn.pack(side=Tk.LEFT)
    file_btn = Tk.Button(text='Copy Graph', master = menu_frame)
    file_btn.pack(side=Tk.LEFT)
    sets_btn = Tk.Button(text='Settings', master = menu_frame)
    sets_btn.pack(side=Tk.LEFT)
    sets_btn = Tk.Button(text='Help', master = menu_frame)
    sets_btn.pack(side=Tk.LEFT)
    sets_btn = Tk.Button(text='About', master = menu_frame)
    sets_btn.pack(side=Tk.LEFT)


def form_quick_acc(quick_acc_frame):
    file_btn = Tk.Button(text='+', master = quick_acc_frame)
    file_btn.pack(side=Tk.LEFT)


def form_graph(graph_frame):
    quick_acc_lbl = Tk.Label(master=graph_frame, text='Graph Area')
    quick_acc_lbl.pack()


def form_calc(calc_frame):
    quick_acc_lbl = Tk.Text(master=calc_frame)
    quick_acc_lbl.pack()


home_window = Tk.Tk()
home_window.geometry('500x700')

calc_frames = {
    'menu': Tk.Frame(width=80),
    'quick': Tk.Frame(width=80),
    'graph': Tk.Frame(width=80),
    'calc': Tk.Frame(width=80),
}

form_menu(calc_frames['menu'])
calc_frames['menu'].place(x=0, y=0, width=500, height=25)
form_quick_acc(calc_frames['quick'])
calc_frames['quick'].place(x=0, y=25, width=500, height=25)
form_graph(calc_frames['graph'])
calc_frames['graph'].place(x=0, y=50, width=500, height=300)
form_calc(calc_frames['calc'])
calc_frames['calc'].place(x=0, y=350, width=500, height=350)

home_window.mainloop()
