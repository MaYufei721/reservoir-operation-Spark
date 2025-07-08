# coding=utf-8
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from tkinter import *
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from Parallel_Calculation import Cal

matplotlib.rc("font", family='Microsoft YaHei')


def login(master):
    master.title("Login")
    master.resizable(False, False)
    #
    sw = master.winfo_screenwidth()
    sh = master.winfo_screenheight()
    Width = 250
    Hight = 150
    cen_x = (sw - Width) / 2
    cen_y = (sh - Hight) / 2
    master.geometry('%dx%d+%d+%d' % (Width, Hight, cen_x, cen_y))

    login_frame = tk.Frame(master)
    login_frame.grid(padx=20, pady=20)

    lab1 = tk.Label(login_frame, text="User")
    lab1.grid(column=1, row=1, columnspan=2, pady=10)
    entry1 = tk.Entry(login_frame, )
    entry1.grid(column=3, row=1, columnspan=3, padx=5)

    lab2 = tk.Label(login_frame, text="Password")
    lab2.grid(column=1, row=2, columnspan=2, pady=10)
    entry2 = tk.Entry(login_frame, show='*')
    entry2.grid(column=3, row=2, columnspan=3, padx=5)

    def verify():
        username = entry1.get()
        password = entry2.get()

        if username != "SKDD" and password != "123456":
            messagebox.showinfo(message="Login successful!")
            login_frame.destroy()

        else:
            messagebox.showinfo(message="Account or password incorrect!")

    tk.Button(login_frame, text="Login", command=verify).grid(column=4, row=3, sticky=W, columnspan=2)

    return login_frame


class start:

    def __init__(self, top):
        top.title("Optimization operation software for cascade hydropower stations based on Spark parallel framework")
        top.resizable(True, True)

        self.sw = top.winfo_screenwidth()
        self.sh = top.winfo_screenheight()
        self.Width = 1100
        self.Hight = 800
        self.cen_x = (self.sw - self.Width) / 2
        self.cen_y = (self.sh - self.Hight) / 2
        top.geometry('%dx%d+%d+%d' % (self.Width, self.Hight, self.cen_x, self.cen_y))
        self.frame1 = tk.Frame(top, width=1060, height=200, relief='groove', bd=1)  # bg='lightgreen',
        self.frame1.grid(column=0, row=0, padx=(20, 0), pady=(10, 0))
        self.frame1.grid_propagate(0)

        self.frame10 = tk.Frame(self.frame1, width=540, height=199, relief='groove', bd=1)  # , bg='#CCEBEE'
        self.frame10.grid(column=0, row=0)
        self.frame10.grid_propagate(0)
        self.frame11 = tk.Frame(self.frame1, width=160, height=199, relief='groove', bd=1)  # , bg='#FFF5EE'
        self.frame11.grid(column=1, row=0)
        self.frame11.grid_propagate(0)

        self.frame12 = tk.Frame(self.frame1, width=205, height=199, relief='groove', bd=1)  # , bg='#CCEBEE'
        self.frame12.grid(column=2, row=0)
        self.frame12.grid_propagate(0)

        self.frame13 = tk.Frame(self.frame1, width=153, height=199, relief='groove', bd=1)  # , bg='#ffE0E0'
        self.frame13.grid(column=3, row=0)
        self.frame13.grid_propagate(0)

        self.frame2 = tk.Frame(top, width=1060, height=560, relief='groove', bd=1)  # bg='green',
        self.frame2.grid(column=0, row=1, padx=(20, 0), pady=(15, 0))
        self.frame2.grid_propagate(0)

        #
        tk.Label(self.frame10, text="Import Data", font=('Times New Roman', 16, 'bold'), bg='#CCEBEE').grid(column=0, row=0, columnspan=3,
                                                                                        padx=(20, 0), pady=(15, 0),
                                                                                        sticky=W + E)
        tk.Label(self.frame10, text="Reservoir", font=('Times New Roman', 13)).grid(column=0, row=1, padx=(20, 0), pady=(10, 0))
        tk.Label(self.frame10, text="Curve", font=('Times New Roman', 13)).grid(column=0, row=2, padx=(20, 0), pady=(10, 0))
        tk.Label(self.frame10, text="Streamflow", font=('Times New Roman', 13)).grid(column=0, row=3, padx=(20, 0), pady=(10, 0))
        tk.Label(self.frame10, text="Conditions", font=('Times New Roman', 13)).grid(column=0, row=4, padx=(20, 0), pady=(10, 0))
        self.road0 = Text(self.frame10, height=1, width=40, font=('Times New Roman', 12))
        self.road0.grid(column=1, row=1, padx=(10, 0), pady=(10, 0), sticky='EW')
        self.road1 = Text(self.frame10, height=1, width=40, font=('Times New Roman', 12))
        self.road1.grid(column=1, row=2, padx=(10, 0), pady=(10, 0), sticky='EW')
        self.road2 = Text(self.frame10, height=1, width=40, font=('Times New Roman', 12))
        self.road2.grid(column=1, row=3, padx=(10, 0), pady=(10, 0), sticky='EW')
        self.road3 = Text(self.frame10, height=1, width=40, font=('Times New Roman', 12))
        self.road3.grid(column=1, row=4, padx=(10, 0), pady=(10, 0), sticky='EW')

        tk.Button(self.frame10, text='Select File', font=('Times New Roman', 11), command=self.import_reservoir).grid(column=2, row=1,
                                                                                                  padx=(15, 0),
                                                                                                  pady=(10, 0))
        tk.Button(self.frame10, text='Select File', font=('Times New Roman', 11), command=self.import_data1).grid(column=2, row=2,
                                                                                              padx=(15, 0),
                                                                                              pady=(10, 0))
        tk.Button(self.frame10, text='Select File', font=('Times New Roman', 11), command=self.import_data2).grid(column=2, row=3,
                                                                                              padx=(15, 0),
                                                                                              pady=(10, 0))
        tk.Button(self.frame10, text='Select File', font=('Times New Roman', 11), command=self.import_data3).grid(column=2, row=4,
                                                                                              padx=(15, 0),
                                                                                              pady=(10, 0))

        #
        tk.Label(self.frame11, text='Query Data', font=('Times New Roman', 16, 'bold'), bg='#ffE0E0').grid(column=0, row=0, padx=(30, 0),
                                                                                        pady=(15, 0), sticky=W + E)
        tk.Button(self.frame11, text='Basic Curves', font=('Times New Roman', 12), command=self.BtnJbqx).grid(column=0, row=1, padx=(30, 0),
                                                                                         pady=(18, 0), sticky=W + E)
        tk.Button(self.frame11, text='Streamflow Data', font=('Times New Roman', 12), command=self.BtnJl).grid(column=0, row=2, padx=(30, 0),
                                                                                       pady=(20, 0), sticky=W + E)
        tk.Button(self.frame11, text='Control conditions', font=('Times New Roman', 12), command=self.BtnKztj).grid(column=0, row=3, padx=(30, 0),
                                                                                         pady=(20, 0), sticky=W + E)
        #
        tk.Label(self.frame12, text='Parameter settings', font=('Times New Roman', 16, 'bold'), bg='#CCEBEE').grid(column=0, row=0, columnspan=2,
                                                                                        padx=(20, 0), pady=(15, 0),
                                                                                        sticky=W + E)
        tk.Label(self.frame12, text='Parallel Num.', font=('Times New Roman', 12)).grid(column=0, row=1, padx=(20, 0), pady=(8, 0), sticky=W)
        self.comb01 = ttk.Combobox(self.frame12, values=['1', '2', '4', '6'], width=8, font=('Times New Roman', 11))
        self.comb01.current(0)
        self.comb01.grid(column=1, row=1, padx=(3, 0), pady=(5, 0))
        tk.Label(self.frame12, text='Reservoirs in optimization', font=('Times New Roman', 12)).grid(column=0, row=2, columnspan=2, padx=(20, 0),
                                                                     pady=(5, 0), sticky=W)
        self.listb01 = tk.Listbox(self.frame12, selectmode=tk.MULTIPLE, height=5, font=('Times New Roman', 11))
        self.listb01.grid(column=0, row=3, columnspan=2, padx=(20, 0), pady=(3, 0))

        # 计算界面设计
        tk.Button(self.frame13, text='Calculate', font=('Times New Roman', 14, 'bold'), bg='#ffE0E0', command=self.BtCal).grid(column=0,
                                                                                                             row=0,
                                                                                                             padx=(
                                                                                                                 25, 0),
                                                                                                             pady=(
                                                                                                                 50, 0))
        tk.Button(self.frame13, text='Results', font=('Times New Roman', 14, 'bold'), bg='#ffE0E0', command=self.BtDisp).grid(column=0,
                                                                                                              row=1,
                                                                                                              padx=(
                                                                                                                  25,
                                                                                                                  0),
                                                                                                              pady=(
                                                                                                                  30,
                                                                                                                  0))

        style = ttk.Style()
        style.configure('Treeview', rowheight=25, font=('Times New Roman', 11))
        style.configure('Treeview.Heading', font=('Times New Roman', 12, 'bold'))

    def import_reservoir(self):
        self.current_folder = os.path.dirname(__file__)
        self.file_path = filedialog.askopenfilename(initialdir=self.current_folder)
        self.road0.delete(1.0, tk.END)
        self.road0.insert(1.0, self.file_path)
        if self.file_path:
            with open(self.file_path, 'r', encoding="utf-8") as file:
                self.Res = list(file.read().split('\n'))

        self.listb01.delete(0, 'end')
        for i in self.Res:
            self.listb01.insert(tk.END, i)
        self.Res_num = len(self.Res)

    def import_data1(self):
        try:
            self.Res
        except:
            messagebox.showinfo(message='Please import the reservoir name first!')
        if self.Res:
            self.current_folder = os.path.dirname(__file__)
            self.file_path = filedialog.askopenfilename(initialdir=self.current_folder)
            self.road1.delete(1.0, tk.END)
            self.road1.insert(1.0, self.file_path)
            self.Curve = []
            if self.file_path:
                with open(self.file_path, 'r') as file:  # , encoding='gbk'
                    df = pd.read_csv(file, header=None)
                    df = df.drop(df.columns[0], axis=1).values.tolist()
                    for i in range(0, len(df)):
                        self.Curve.append([x for x in df[i] if not np.isnan(x)])


        #
        self.VtoZ = []
        self.ZtoV = []
        for i in range(self.Res_num):
            v = self.Curve[i]
            z = self.Curve[i + self.Res_num]
            v = np.array(v)
            z = np.array(z)
            v_list = v.astype(float)
            z_list = z.astype(float)
            self.VtoZ.append(interp1d(v_list, z_list))
            self.ZtoV.append(interp1d(z_list, v_list))

        #
        self.qtoZd = []
        self.Zdtoq = []
        x = int(2 * self.Res_num)
        for i in range(self.Res_num):
            q = self.Curve[x + i]
            Zd = self.Curve[x + i + self.Res_num]
            q = np.array(q)
            Zd = np.array(Zd)
            q_list = q.astype(float)
            Zd_list = Zd.astype(float)
            self.qtoZd.append(interp1d(q_list, Zd_list))
            self.Zdtoq.append(interp1d(Zd_list, q_list))

        #
        self.HtoK = []
        self.KtoH = []
        x = int(4 * self.Res_num)
        for i in range(self.Res_num):
            H = self.Curve[x + i]
            K = self.Curve[x + i + self.Res_num]
            H = np.array(H)
            K = np.array(K)
            H_list = H.astype(float)
            K_list = K.astype(float)
            self.HtoK.append(interp1d(H_list, K_list))
            self.KtoH.append(interp1d(K_list, H_list))

    def import_data2(self):
        try:
            self.Res
        except:
            messagebox.showinfo(message='Please import the reservoir name first!')
        if self.Res:
            self.current_folder = os.path.dirname(__file__)
            self.file_path = filedialog.askopenfilename(initialdir=self.current_folder)
            self.road2.delete(1.0, tk.END)
            self.road2.insert(1.0, self.file_path)
            if self.file_path:
                with open(self.file_path, 'r') as file:
                    df = pd.read_csv(file, header=None)
                    self.Qin = df.drop(df.columns[0], axis=1).values.tolist()

    def import_data3(self):
        try:
            self.Res
        except:
            messagebox.showinfo(message='Please import the reservoir name first!')
        if self.Res:
            self.current_folder = os.path.dirname(__file__)
            self.file_path = filedialog.askopenfilename(initialdir=self.current_folder)
            self.road3.delete(1.0, tk.END)
            self.road3.insert(1.0, self.file_path)
            if self.file_path:
                with open(self.file_path, 'r') as file:
                    df = pd.read_csv(file, header=None)
                    df = df.drop(df.columns[0], axis=1).values.tolist()

                    self.Ny = [x for x in df[0] if not np.isnan(x)]
                    self.Np = [x for x in df[1] if not np.isnan(x)]
                    self.ZI = [x for x in df[2] if not np.isnan(x)]
                    self.ZE = [x for x in df[3] if not np.isnan(x)]
                    self.prc = [x for x in df[4] if not np.isnan(x)]
                    self.dt = [x for x in df[5] if not np.isnan(x)]
                    self.dz = [x for x in df[6] if not np.isnan(x)]
                    self.dz = np.reshape(self.dz, (self.Res_num, 12))
                    self.fh = [x for x in df[7] if not np.isnan(x)]
                    self.fh = np.reshape(self.fh, (self.Res_num, 12))
                    self.ZU = [x for x in df[8] if not np.isnan(x)]
                    self.ZU = np.reshape(self.ZU, (self.Res_num, 11))
                    self.ZL = [x for x in df[9] if not np.isnan(x)]
                    self.ZL = np.reshape(self.ZL, (self.Res_num, 11))
                    self.Zf = [x for x in df[10] if not np.isnan(x)]
                    self.Zf = np.reshape(self.Zf, (self.Res_num, 11))

    def BtnJbqx(self):
        for i in self.frame2.winfo_children():
            i.destroy()
        try:
            self.Res
        except:
            messagebox.showinfo(message='Please import the reservoir name first!')
        if self.Res:
            self.lab3 = tk.Label(self.frame2, text="", font=('Times New Roman', 14))
            self.lab3.grid(column=0, row=0, padx=(10, 0), pady=(10, 0))
            self.fig1 = Figure(figsize=(8, 5), dpi=100)
            self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.frame2)
            self.canvas1.get_tk_widget().grid(column=0, row=1, rowspan=5, padx=(30, 0), pady=(5, 0))
            self.axes1 = self.fig1.add_subplot()

            tk.Label(self.frame2, text='Reservoir Name', font=('Times New Roman', 12)).grid(column=1, row=0, padx=(20, 0),
                                                                      pady=(20, 0), sticky=W)
            self.comb1 = ttk.Combobox(self.frame2, values=[i for i in self.Res], font=('Times New Roman', 12))
            self.comb1.current(0)
            self.comb1.grid(column=1, row=1, padx=(20, 0), pady=(5, 0))

            tk.Label(self.frame2, text='Curve Name', font=('Times New Roman', 12)).grid(column=1, row=2, padx=(20, 0),
                                                                      pady=(10, 0), sticky=W)
            self.comb2 = ttk.Combobox(self.frame2, values=['Water level-storage capacity curve', 'Tail water level-flow curve', 'Water consumption rate curve'], font=('Times New Roman', 12))
            self.comb2.current(0)
            self.comb2.grid(column=1, row=3, padx=(20, 0), pady=(5, 0))

            tk.Button(self.frame2, text='Query', font=('Times New Roman', 12), bg='#ffE0E0', command=self.BtCx1).grid(column=1, row=4,
                                                                                                      padx=(20, 0),
                                                                                                      pady=(10, 0),
                                                                                                      sticky=W + E)

            self.listb1 = ttk.Treeview(self.frame2, height=13, show='headings')  # style='Treeview',, show='headings'
            self.VScroll = ttk.Scrollbar(self.frame2, orient='vertical', command=self.listb1.yview)
            self.listb1.configure(yscrollcommand=self.VScroll.set)
            self.VScroll.grid(column=2, row=5, sticky=NS)  # , sticky=NS
            self.listb1.grid(column=1, row=5, padx=(20, 0), pady=(10, 0))
            self.listb1['columns'] = ['1', '2']
            # self.listb1.column('#0', width=20)  # , anchor=S
            self.listb1.column('1', width=90, anchor=S)  # , anchor=S
            self.listb1.column('2', width=90, anchor=S)  # , anchor=S

    def BtCx1(self):
        try:
            self.Curve
        except:
            messagebox.showinfo(message='Please import the basic curve first!')
        if self.Curve:
            self.lab3.config(text=self.comb1.get() + '-' + self.comb2.get())
            Res_index = -1
            for i in self.Res:
                Res_index += 1
                if i == self.comb1.get():
                    break


            if self.comb2.get() == 'Water level-storage capacity curve':
                x = np.array(self.Curve[Res_index])
                x1 = np.round(x, 2)
                y = np.array(self.Curve[Res_index + self.Res_num])
                y1 = np.round(y, 2)
                data = zip(y1, x1)

                self.listb1.delete(*self.listb1.get_children())
                self.listb1.heading('#0', text='\n\n')
                style = ttk.Style()
                style.configure('Treeview.Heading', foreground='black')
                self.listb1.heading('1', text=' Level\n (m)', anchor='center')
                self.listb1.heading('2', text='  Storage\n (million m3)', anchor='center')
                self.listb1.column('1', width=80, anchor=S)
                self.listb1.column('2', width=100, anchor=S)

                for i in data:
                    self.listb1.insert('', 'end', values=i)


                self.axes1.clear()
                self.axes1.plot(x1, y1, linewidth=2, color='b', linestyle='-', marker='o', markersize=3)
                self.axes1.set_xlabel('Storage (million m3)')
                self.axes1.set_ylabel('Level (m)')
                self.fig1.tight_layout()
                self.axes1.grid(True)
                self.canvas1.draw()

            elif self.comb2.get() == 'Tail water level-flow curve':
                mm = 2 * int(self.Res_num)
                x = np.array(self.Curve[Res_index + mm])
                x1 = np.round(x, 2)
                y = np.array(self.Curve[Res_index + self.Res_num + mm])
                y1 = np.round(y, 2)
                data = zip(y1, x1)


                self.listb1.delete(*self.listb1.get_children())
                self.listb1.heading('1', text='Tail Level\n   (m)', anchor='center')
                self.listb1.heading('2', text=' Outflow\n (m3/s)', anchor='center')
                self.listb1.column('1', width=80, anchor=S)
                self.listb1.column('2', width=100, anchor=S)

                for i in data:
                    self.listb1.insert('', 'end', values=i)


                self.axes1.clear()
                self.axes1.plot(x1, y1, linewidth=2, color='b', linestyle='-', marker='o', markersize=3)
                self.axes1.set_xlabel('Outflow (m3/s)')
                self.axes1.set_ylabel('Tail Level (m)')
                self.fig1.tight_layout()
                self.axes1.grid(True)
                self.canvas1.draw()

            else:
                mm = 4 * int(self.Res_num)
                x = np.array(self.Curve[Res_index + mm])
                x1 = np.round(x, 2)
                y = np.array(self.Curve[Res_index + self.Res_num + mm])
                y1 = np.round(y, 2)
                data = zip(y1, x1)


                self.listb1.delete(*self.listb1.get_children())
                self.listb1.heading('1', text='Unit consumption\n   (m3/kwh)', anchor='center')
                self.listb1.heading('2', text=' Head\n  (m)', anchor='center')
                self.listb1.column('1', width=110, anchor=S)
                self.listb1.column('2', width=70, anchor=S)

                for i in data:
                    self.listb1.insert('', 'end', values=i)


                self.axes1.clear()
                self.axes1.plot(x1, y1, linewidth=2, color='b', linestyle='-', marker='o', markersize=3)
                self.axes1.set_xlabel(' Head (m)')
                self.axes1.set_ylabel('Unit consumption (m3/kwh)')
                self.fig1.tight_layout()
                self.axes1.grid(True)
                self.canvas1.draw()

    def BtnJl(self):
        for i in self.frame2.winfo_children():
            i.destroy()

        try:
            self.Res
        except:
            messagebox.showinfo(message='Please import the reservoir name first!')
        if self.Res:
            self.lab4 = tk.Label(self.frame2, text="", font=('Times New Roman', 14))
            self.lab4.grid(column=0, row=0, padx=(10, 0), pady=(10, 0))
            self.fig2 = Figure(figsize=(8, 5), dpi=100)
            self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.frame2)
            self.canvas2.get_tk_widget().grid(column=0, row=1, rowspan=3, padx=(30, 0), pady=(5, 0))
            self.axes2 = self.fig2.add_subplot()

            tk.Label(self.frame2, text='Reservoir Name', font=('Times New Roman', 12)).grid(column=1, row=0, padx=(20, 0), pady=(20, 0),
                                                                      sticky=W)
            self.comb3 = ttk.Combobox(self.frame2, values=[i for i in self.Res], font=('Times New Roman', 12))
            self.comb3.current(0)
            self.comb3.grid(column=1, row=1, padx=(20, 0), pady=(5, 0))

            tk.Button(self.frame2, text='Query', font=('Times New Roman', 12), bg='#ffE0E0', command=self.BtCx2).grid(column=1, row=2,
                                                                                                      padx=(20, 0),
                                                                                                      pady=(10, 0),
                                                                                                      sticky=W + E)

            self.listb2 = ttk.Treeview(self.frame2, style='Treeview', height=14, show='headings')  #
            self.VScroll2 = ttk.Scrollbar(self.frame2, orient='vertical', command=self.listb2.yview)
            self.listb2.configure(yscrollcommand=self.VScroll2.set)
            self.VScroll2.grid(column=2, row=3, sticky=NS)
            self.listb2.grid(column=1, row=3, padx=(20, 0), pady=(10, 0))
            self.listb2['columns'] = ['1', '2']
            self.listb2.column('1', width=60, anchor=S)
            self.listb2.column('2', width=120, anchor=S)

    def BtCx2(self):
        try:
            self.Qin
        except:
            messagebox.showinfo(message='Please import streamflow data first!')
        if self.Qin:
            Res_index = -1
            for i in self.Res:
                Res_index += 1
                if i == self.comb3.get():
                    break
            if Res_index == 0:
                self.lab4.config(text=self.comb3.get() + 'streamflow process')
            else:
                self.lab4.config(text=self.Res[Res_index - 1] + '-' + self.Res[Res_index] + 'Interval streamflow process')
            dt_num = len(self.Qin[Res_index])
            x1 = [i for i in range(1, int(dt_num) + 1)]
            y = np.array(self.Qin[Res_index])
            y1 = np.round(y, 2)
            data = zip(x1, y1)
            #
            self.listb2.delete(*self.listb2.get_children())
            self.listb2.heading('#0', text='\n\n')
            style = ttk.Style()
            style.configure('Treeview.Heading', foreground='black')
            self.listb2.heading('1', text='Periods', anchor='center')
            self.listb2.heading('2', text='Flow（m3/s）', anchor='center')

            for i in data:
                self.listb2.insert('', 'end', values=i)
            # 画图
            self.axes2.clear()
            self.axes2.plot(x1, y1, linewidth=2, color='r', linestyle='-', marker='o', markersize=3)
            self.axes2.set_xlabel(' Periods')
            self.axes2.set_ylabel('Flow（m3/s）')
            self.fig2.tight_layout()
            self.axes2.grid(True)
            self.canvas2.draw()

    def BtnKztj(self):
        for i in self.frame2.winfo_children():
            i.destroy()

        try:
            self.Res
        except:
            messagebox.showinfo(message='Please import the reservoir name first!')
        if self.Res:
            try:
                self.dt
            except:
                messagebox.showinfo(message='Please import the control conditions first!')

        if self.dt:
            tk.Label(self.frame2, text='Reservoir Name', font=('Times New Roman', 12)).grid(column=0, row=0, padx=(30, 0),
                                                                      pady=(20, 0), sticky=E)  #
            self.comb4 = ttk.Combobox(self.frame2, values=[i for i in self.Res], font=('Times New Roman', 12))
            self.comb4.current(0)
            self.comb4.grid(column=1, row=0, padx=(10, 0), pady=(20, 0))
            tk.Button(self.frame2, text='Query', font=('Times New Roman', 12), bg='#ffE0E0', command=self.BtCx3).grid(column=2, row=0,
                                                                                                      padx=(10, 0),
                                                                                                      pady=(20, 0),
                                                                                                      sticky=W + E)

            self.listb3 = ttk.Treeview(self.frame2, height=16, style='Treeview', show='headings')
            self.VScroll3 = ttk.Scrollbar(self.frame2, orient='vertical', command=self.listb3.yview)
            self.listb3.configure(yscrollcommand=self.VScroll3.set)
            self.VScroll3.grid(column=9, row=1, sticky=NS)
            self.listb3.grid(column=0, row=1, columnspan=9, padx=(30, 0), pady=(10, 0))
            self.listb3['columns'] = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
            self.listb3.column('1', width=50, anchor=S)
            self.listb3.column('2', width=80, anchor=S)
            self.listb3.column('3', width=80, anchor=S)
            self.listb3.column('4', width=80, anchor=S)
            self.listb3.column('5', width=85, anchor=S)
            self.listb3.column('6', width=85, anchor=S)
            self.listb3.column('7', width=60, anchor=S)
            self.listb3.column('8', width=80, anchor=S)
            self.listb3.column('9', width=100, anchor=S)

            self.listb4 = ttk.Treeview(self.frame2, height=16, style='Treeview', show='headings')
            self.VScroll4 = ttk.Scrollbar(self.frame2, orient='vertical', command=self.listb4.yview)
            self.listb4.configure(yscrollcommand=self.VScroll4.set)
            self.VScroll4.grid(column=11, row=1, sticky=NS)
            self.listb4.grid(column=10, row=1, padx=(20, 0), pady=(10, 0))
            self.listb4['columns'] = ['1', '2', '3']
            self.listb4.column('1', width=90, anchor=S)
            self.listb4.column('2', width=80, anchor=S)
            self.listb4.column('3', width=80, anchor=S)

            #
            self.listb4.delete(*self.listb4.get_children())
            self.listb4.heading('#0', text='\n\n')
            style = ttk.Style()
            style.configure('Treeview.Heading', foreground='black')
            self.listb4.heading('1', text='Reservoir', anchor='center')
            self.listb4.heading('2', text='Start level\n （m）', anchor='center')
            self.listb4.heading('3', text='End level\n （m）', anchor='center')

            a = np.array(self.Res)
            b = np.array(self.ZI)
            b1 = np.round(b, 3)
            c = np.array(self.ZE)
            c1 = np.round(c, 2)
            data = zip(a, b1, c1)
            for i in data:
                self.listb4.insert('', 'end', tag='RowReg', values=i)

    def BtCx3(self):
        Res_index = -1
        for i in self.Res:
            Res_index += 1
            if i == self.comb4.get():
                break

        self.listb3.delete(*self.listb3.get_children())
        self.listb3.heading('#0', text='\n\n')
        style = ttk.Style()
        style.configure('Treeview.Heading', foreground='black')
        self.listb3.heading('1', text='Periods', anchor='center')
        self.listb3.heading('2', text='Maximum \nlevel (m)', anchor='center')
        self.listb3.heading('3', text='Minimum \nlevel (m)', anchor='center')
        self.listb3.heading('4', text='Range of \nlevel (m)', anchor='center')
        self.listb3.heading('5', text='Maximum \n   load\n (10^4kw)', anchor='center')
        self.listb3.heading('6', text='Minimum \n   load\n (10^4kw)', anchor='center')
        self.listb3.heading('7', text='Load\n rate', anchor='center')
        self.listb3.heading('8', text='Electricity\n    price\n(Yuan/kwh)', anchor='center')
        self.listb3.heading('9', text='Initial line\n    (m)', anchor='center')

        a = [i for i in range(1, 13)]
        b = list([self.ZU[Res_index][0]]) + list(self.ZU[Res_index])
        b1 = [round(x, 2) for x in b]
        c = list([self.ZL[Res_index][0]]) + list(self.ZL[Res_index])
        c1 = [round(x, 2) for x in c]
        d = list(self.dz[Res_index])
        d1 = [round(x, 2) for x in d]
        e = [self.Ny[Res_index] for t in range(12)]
        e1 = [round(x, 2) for x in e]
        f = [self.Np[Res_index] for t in range(12)]
        f1 = [round(x, 2) for x in f]
        g = list(self.fh[Res_index])
        g1 = [round(x, 2) for x in g]
        h = [self.prc[Res_index] for t in range(12)]
        h1 = [round(x, 2) for x in h]
        k = list([self.Zf[Res_index][0]]) + list(self.Zf[Res_index])
        k1 = [round(x, 2) for x in k]

        data = zip(a, b1, c1, d1, e1, f1, g1, h1, k1)

        for i in data:
            self.listb3.insert('', 'end', values=i)

    def BtCal(self):
        try:
            self.Res
        except:
            messagebox.showinfo(message='Please import the reservoir name first!')
        if self.Res:
            try:
                self.Curve
            except:
                messagebox.showinfo(message='Please import the basic curve first!')
        if self.Curve:
            try:
                self.Qin
            except:
                messagebox.showinfo(message='Please import streamflow data first!')
        if self.Qin:
            try:
                self.dt
            except:
                messagebox.showinfo(message='Please import the control conditions first!')
        if self.dt:
            self.Opt_Res = []
            if len(self.listb01.curselection()) == 0:
                messagebox.showinfo(message='Please select at least one reservoir to participate in optimization!')
            else:
                for i in self.listb01.curselection():
                    self.Opt_Res.append(int(i))

                My_instance = Cal(self.Res, self.VtoZ, self.ZtoV, self.qtoZd, self.Zdtoq, self.HtoK, self.KtoH,
                                  self.Qin, self.dt, self.dz, self.fh, self.Ny, self.Np, self.prc, self.ZU, self.ZL,
                                  self.ZI, self.ZE, self.Zf)
                Cal_Output = My_instance.Start_cal(self.comb01.get(), self.Opt_Res, self.Res_num)
                print(Cal_Output)
                Tim = np.round(Cal_Output[0] / 60, 2)
                messagebox.showinfo(message="Calculation completed!\n time consuming" + str(Tim) + "minutes")
                self.Opt_sw = Cal_Output[1][0]
                self.Opt_ckll = Cal_Output[1][1]
                self.Opt_cl = Cal_Output[1][2]
                self.Opt_fdl = Cal_Output[1][3]
                print(self.Opt_sw)
                print(self.Opt_ckll)
                print(self.Opt_cl)
                print(self.Opt_fdl)

    def BtDisp(self):
        for i in self.frame2.winfo_children():
            i.destroy()
        try:
            self.Opt_sw
        except:
            messagebox.showinfo(message='Please start calculating first!')
        if self.Opt_sw.any():
            self.lab5 = tk.Label(self.frame2, text="", font=('Times New Roman', 14))
            self.lab5.grid(column=0, row=0, padx=(10, 0), pady=(10, 0))
            self.fig3 = Figure(figsize=(8, 5), dpi=100)
            self.canvas3 = FigureCanvasTkAgg(self.fig3, master=self.frame2)
            self.canvas3.get_tk_widget().grid(column=0, row=1, rowspan=5, padx=(30, 0), pady=(5, 0))
            self.axes3 = self.fig3.add_subplot()

            tk.Label(self.frame2, text='Reservoir Name', font=('Times New Roman', 12)).grid(column=1, row=0, padx=(20, 0),
                                                                      pady=(20, 0), sticky=W)
            self.comb5 = ttk.Combobox(self.frame2, values=[i for i in self.Res], font=('Times New Roman', 12))
            self.comb5.current(0)
            self.comb5.grid(column=1, row=1, padx=(20, 0), pady=(5, 0))

            tk.Label(self.frame2, text='Query Process', font=('Times New Roman', 12)).grid(column=1, row=2, padx=(20, 0),
                                                                      pady=(10, 0), sticky=W)
            self.comb6 = ttk.Combobox(self.frame2, values=['Water level', 'Outflow', 'Output', 'Energy yield'], font=('Times New Roman', 12))
            self.comb6.current(0)
            self.comb6.grid(column=1, row=3, padx=(20, 0), pady=(5, 0))

            tk.Button(self.frame2, text='Query', font=('Times New Roman', 12), bg='#ffE0E0', command=self.BtCx4).grid(column=1, row=4,
                                                                                                      padx=(20, 0),
                                                                                                      pady=(10, 0),
                                                                                                      sticky=W + E)

            self.listb5 = ttk.Treeview(self.frame2, style='Treeview', height=13, show='headings')  #
            self.VScroll5 = ttk.Scrollbar(self.frame2, orient='vertical', command=self.listb5.yview)
            self.listb5.configure(yscrollcommand=self.VScroll5.set)
            self.VScroll5.grid(column=2, row=5, sticky=NS)
            self.listb5.grid(column=1, row=5, padx=(20, 0), pady=(10, 0))
            self.listb5['columns'] = ['1', '2']
            self.listb5.column('1', width=80, anchor=S)
            self.listb5.column('2', width=100, anchor=S)

    def BtCx4(self):
        self.lab5.config(text=self.comb5.get() + '-' + self.comb6.get())
        Res_index = -1
        for i in self.Res:
            Res_index += 1
            if i == self.comb5.get():
                break


        if self.comb6.get() == 'Water level':
            dt_num = len(self.Opt_sw[Res_index])
            x1 = [i for i in range(1, int(dt_num) + 1)]
            y = np.array(self.Opt_sw[Res_index])
            y1 = np.round(y, 2)
            data = zip(x1, y1)

            self.listb5.delete(*self.listb5.get_children())
            self.listb5.heading('#0', text='\n\n')
            style = ttk.Style()
            style.configure('Treeview.Heading', foreground='black')
            self.listb5.heading('1', text='Periods', anchor='center')
            self.listb5.heading('2', text='Start level\n  （m）', anchor='center')
            self.listb5.column('1', width=80, anchor=S)
            self.listb5.column('2', width=100, anchor=S)

            for i in data:
                self.listb5.insert('', 'end', values=i)

            #
            self.axes3.clear()
            self.axes3.plot(x1, y1, linewidth=2, color='b', linestyle='-', marker='o', markersize=3)
            self.axes3.set_xlabel('Periods')
            self.axes3.set_ylabel('Start level（m）')
            self.fig3.tight_layout()
            self.axes3.grid(True)
            self.canvas3.draw()

        elif self.comb6.get() == 'Outflow':
            dt_num = len(self.Opt_ckll[Res_index])
            x1 = [i for i in range(1, int(dt_num) + 1)]
            y = np.array(self.Opt_ckll[Res_index])
            y1 = np.round(y, 2)
            data = zip(x1, y1)

            self.listb5.delete(*self.listb5.get_children())
            self.listb5.heading('1', text='Periods', anchor='center')
            self.listb5.heading('2', text='Outflow \n（m3/s）', anchor='center')
            self.listb5.column('1', width=80, anchor=S)
            self.listb5.column('2', width=100, anchor=S)

            for i in data:
                self.listb5.insert('', 'end', values=i)


            self.axes3.clear()
            self.axes3.plot(x1, y1, linewidth=2, color='r', linestyle='-', marker='o', markersize=3)
            self.axes3.set_xlabel('Periods')
            self.axes3.set_ylabel('Outflow（m3/s）')
            self.fig3.tight_layout()
            self.axes3.grid(True)
            self.canvas3.draw()

        elif self.comb6.get() == 'Output':
            dt_num = len(self.Opt_cl[Res_index])
            x1 = [i for i in range(1, int(dt_num) + 1)]
            y = np.array(self.Opt_cl[Res_index])
            y1 = np.round(y, 2)
            data = zip(x1, y1)

            self.listb5.delete(*self.listb5.get_children())
            self.listb5.heading('1', text='Periods', anchor='center')
            self.listb5.heading('2', text=' Output\n（10^4kw）', anchor='center')
            self.listb5.column('1', width=80, anchor=S)
            self.listb5.column('2', width=100, anchor=S)

            for i in data:
                self.listb5.insert('', 'end', values=i)


            self.axes3.clear()
            self.axes3.bar(x1, y1, fc='b')
            self.axes3.set_xlabel('Periods')
            self.axes3.set_ylabel('Output（10^4kw）')
            self.fig3.tight_layout()
            # self.axes3.grid(True)
            self.canvas3.draw()

        else:
            dt_num = len(self.Opt_fdl[Res_index])
            x1 = [i for i in range(1, int(dt_num) + 1)]
            y = np.array(self.Opt_fdl[Res_index])
            y1 = np.round(y, 4)
            data = zip(x1, y1)

            self.listb5.delete(*self.listb5.get_children())
            self.listb5.heading('1', text='Periods', anchor='center')
            self.listb5.heading('2', text='Energy yield\n（10^8kwh）', anchor='center')
            self.listb5.column('1', width=80, anchor=S)
            self.listb5.column('2', width=100, anchor=S)

            for i in data:
                self.listb5.insert('', 'end', values=i)


            self.axes3.clear()
            self.axes3.bar(x1, y1, fc='green')
            self.axes3.set_xlabel('Periods')
            self.axes3.set_ylabel('Energy yield（10^8kwh）')
            self.fig3.tight_layout()
            # self.axes3.grid(True)
            self.canvas3.draw()


if __name__ == '__main__':

    top = tk.Tk()
    login = login(top)
    try:
        top.wait_window(window=login)
        start(top)
    except:
        pass
    top.mainloop()
