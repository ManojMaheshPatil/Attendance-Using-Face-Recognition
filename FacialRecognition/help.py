from tkinter import *
from tkinter import ttk
from time import strftime
from datetime import datetime
from PIL import Image,ImageTk
from tkinter import messagebox


class Help:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1275x750+0+0")
        self.root.title("Facial Recognition System")

        # Title 
        title_lbl=Label(self.root,text="HELP",font=("times new roman",25,"bold"),bg="white",fg="red") 
        title_lbl.place(x=0, y=0,width=1280,height=50)
        
        #Time
        def time():
           string = strftime('%H:%M:%S %p')
           lbl.config(text = string)
           lbl.after (1000, time)
        
        lbl = Label(title_lbl, font = ('times new roman',14, 'bold'), background='white', foreground='blue')
        lbl.place(x=0,y=0,width=110,height=50) 
        time()

        # Bckgrd img 
        img_top=Image.open(r"img\background.jpg")
        img_top=img_top.resize((1920,1080),Image.ANTIALIAS)
        self.photoimg_top=ImageTk.PhotoImage(img_top)

        f_lbl=Label(self.root,image=self.photoimg_top)
        f_lbl.place(x=0,y=52,width=1530,height=635) 

        # Frame      
        main_frame=Frame(f_lbl,bd=2,bg="white")
        main_frame.place(x=345,y=100,height=460,width=600)

        #help desk img
        img_top1=Image.open(r"img\help.jpg")
        img_top1=img_top1.resize((600,360),Image.ANTIALIAS)
        self.photoimg_top1=ImageTk.PhotoImage(img_top1)

        f_lbl=Label(main_frame,image=self.photoimg_top1)
        f_lbl.place(x=0,y=0,width=600,height=360)

        # Help Info
        help_label=Label(main_frame,text="If you have any queries,send us a message at",font=("times new roman",18,"bold"),bg="white",fg="darkblue")
        help_label.place(x=70,y=360) 

        help_label=Label(main_frame,text="kowshik.achyuth@gmail.com",font=("times new roman",25,"bold"),bg="white",fg="darkblue")
        help_label.place(x=90,y=400) 

        
if __name__=="__main__":
    root=Tk()
    obj=Help(root)
    root.mainloop()