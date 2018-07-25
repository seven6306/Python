# -*- coding: utf-8 -*-

from tkinter import ttk, Tk, Label, Frame
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo, showerror, askokcancel


class Windows(Frame):

    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        
        # 執行檔標題
        self.master.title('Program Name       Support Ver : Python3.5 (less)')

        # 視窗大小
        self.master.geometry('400x160')

        # 禁用視窗放大縮小
        self.master.resizable(0, 0)

        # 執行檔圖示
        self.master.iconbitmap(default='')
        self.createWidgets()

    def createWidgets(self):

        # 建立文字方塊 (物件名稱可以自訂)
        self.master.LB = Label(self.master, text="Specified file : ", fg="blue")
        self.master.LB.place(x=10, y=18)

        self.master.LB = Label(self.master, text="Message box : ", fg="blue")
        self.master.LB.place(x=10, y=120)

        self.master.displayText = Label(self.master, text="Execution message", fg="brown")
        self.master.displayText.place(x=90, y=120)

        # 建立按鈕, command 為按鈕功能
        self.master.Run = ttk.Button(self.master, text='GO', command=self.method)
        self.master.Run.place(x=310, y=120)

    # 按鈕功能
    def method(self):
        self.master.displayText["text"] = 'Commant here'

if __name__ == '__main__':

    root = Tk()
    app = Windows(master=root)
    app.mainloop()

