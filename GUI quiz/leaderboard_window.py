import tkinter as tk
import pandas as pd
from score_board import get_file_path
import ttkbootstrap as ttk
import csv

class leaderboard:
    def __init__(self, master):
        self.master = master
        self.master.title("leaderboard")

        self.leaderboard_label = tk.Label(self.master,text="leaderboard",font=('consolas',12,'bold'), justify="center").pack()

        file_path = get_file_path('scoreBoard.csv')
        file = open(file_path)
        csvreader = csv.reader(file)
        l1 = []
        l1 = next(csvreader)
        r_set = [row for row in csvreader]

        trv = ttk.Treeview(self.master,selectmode='browse')
        trv.pack()
        
        trv['height'] = 5
        trv['show'] = 'headings'
        trv['column'] = l1

        for i in l1:
            trv.column(i, width=100,anchor='c')
            trv.heading(i, text=i)

        for dt in r_set:
            v=[r for r in dt]
            trv.insert('','end',iid=v[0],values=v)
