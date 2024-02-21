from tkinter import *
from tkinter import ttk,messagebox
import tkinter
import PIL
from PIL import Image,ImageTk
from student import Student
from train import Train
from attendance import Attendance
from help import Help
import os


class Face_Recognition_System:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1275x750+0+0")
        self.root.title("Facial Recognition System")

        # Background Image
        img=Image.open(r"img\perfback.jpg")
        img=img.resize((1275,770),Image.ANTIALIAS)
        self.background=ImageTk.PhotoImage(img)

        bg_img=Label(self.root,image=self.background)
        bg_img.place(x=0,y=0,width=1275,height=750)

        # Title
        # title_lbl=Label(bg_img,text="FACE RECOGNITION ATTENDANCE SYSTEM",font=("Merriweather",36,"bold"),bg="white",fg="teal")
        # title_lbl.place(x=15,y=25,height=52,width=1230)


        # Buttons
        # 1) Student Details

        st_img=Image.open(r"img\view_studs.jpg")
        # st_img=st_img.resize((210,210),Image.ANTIALIAS)
        self.st_photoImg=ImageTk.PhotoImage(st_img)

        st_btn=Button(bg_img,image=self.st_photoImg,command=self.student_details,cursor="hand2")
        st_btn.place(x=740,y=175,height=45,width=360)


        # 2) Photos

        photo_img = Image.open(r"img\opdir.jpg")
        # photo_img=photo_img.resize((220,220),Image.ANTIALIAS)
        self.photo_photoImg = ImageTk.PhotoImage(photo_img)

        photo_btn = Button(bg_img, image=self.photo_photoImg,cursor="hand2", command=self.open_img)
        photo_btn.place(x=740, y=260, width=365, height=45)

        # 3) Train

        train_img = Image.open(r"img\traindata.jpg")
        # train_img=train_img.resize((220,220),Image.ANTIALIAS)
        self.train_photoImg = ImageTk.PhotoImage(train_img)

        train_btn = Button(bg_img, image=self.train_photoImg,cursor="hand2", command=self.train_data)
        train_btn.place(x=740, y=365, width=360, height=45)

        # 4) Attendance Button
 
        att_img = Image.open(r"img\markattend.jpg")
        # att_img=att_img.resize((220,220),Image.ANTIALIAS)
        self.att_photoImg = ImageTk.PhotoImage(att_img)

        att_btn = Button(bg_img, image=self.att_photoImg, cursor="hand2",command=self.attendance)
        att_btn.place(x=740, y=470, width=360, height=45)

        # 5 Exit 

        exit_img = Image.open(r"img\exitbtn.jpg")
        # exit_img=exit_img.resize((220,220),Image.ANTIALIAS)
        self.exit_photoImg = ImageTk.PhotoImage(exit_img)

        exit_btn = Button(bg_img, image=self.exit_photoImg, cursor="hand2",command=self.exit,bg="purple")
        exit_btn.place(x=740, y=575, width=360, height=45)


        # 6 Help
        help_img=Image.open(r"img\help.png")
        help_img=help_img.resize((50,50))
        self.help_photoImg=ImageTk.PhotoImage(help_img)

        help_btn = Button(bg_img, image=self.help_photoImg, cursor="hand2",command=self.help,bg="white")
        help_btn.place(x=1195, y=590, width=50, height=50)
        

    # --------------Functionalities to the Buttons---------
    def student_details(self):
        self.newWindow=Toplevel(self.root)
        self.app=Student(self.newWindow)
    
    def train_data(self):
        self.newWindow=Toplevel(self.root)
        self.app=Train(self.newWindow)
    
    def attendance(self):
        self.newWindow=Toplevel(self.root)
        self.app=Attendance(self.newWindow)

    def open_img(self):
        os.startfile("data")
    
    def exit(self):
        info=messagebox.askyesno("EXIT","Are you sure you want to exit",parent=self.root)
        if info>0:
            self.root.destroy()
    
    def help(self):
        self.newWindow=Toplevel(self.root)
        self.app=Help(self.newWindow)


if __name__=="__main__":
    root=Tk()
    obj=Face_Recognition_System(root)
    root.attributes("-fullscreen", True)
    root.bind("<F11>", lambda event: root.attributes(
        "-fullscreen", not root.attributes("-fullscreen")))
    root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))
    root.mainloop()
