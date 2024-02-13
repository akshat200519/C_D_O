from tkinter import *

from sub_files.seller_interface import FrontEndTwo
from sub_files.staff_interface import FrontEndOne


class Main:
    def __init__(self, window):
        self.root = window
        self.root.title("Car Showroom Management System")
        self.root.geometry("597x220+300+100")
        self.root.resizable(False, False)

        self.title = Label(self.root, text="Car Showroom Management System", bd=4, relief=GROOVE,
                           font=("times new roman", 40, "bold"))
        self.title.pack(side=TOP, fill=X)

        self.login_frame = Frame(self.root, bd=4, relief=RIDGE)
        self.login_frame.place(x=0, y=70, width=595, height=150)

        self.login_lbl = Label(self.login_frame, text="Which application do you want to open?",
                               font=("times new roman", 17, "bold"))
        self.login_lbl.grid(row=2, columnspan=2, pady=25, padx=30)

        self.staff_btn = Button(self.login_frame, text="Staff", width="21", font=("times new roman", 15, "bold"),
                                command=self.staff)
        self.staff_btn.grid(row=3, column=0, padx=20, pady=10)

        self.seller_btn = Button(self.login_frame, text="Seller", width="21", font=("times new roman", 15, "bold"),
                                 command=self.seller)
        self.seller_btn.grid(row=3, column=1, padx=5, pady=10)

    def staff(self):
        self.root.destroy()
        window = Tk()
        FrontEndOne(window)
        window.mainloop()

    def seller(self):
        self.root.destroy()
        window = Tk()
        FrontEndTwo(window)
        window.mainloop()


root = Tk()
ob = Main(root)
root.mainloop()
