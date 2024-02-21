from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image,ImageTk
from user_details import User
from login import Login

class Index:

    def __init__(self,root,SRN):
        self.root=root
        self.SRN=SRN
        self.root.geometry("1275x650+0+0")
        # self.root.title("Index")

        self.root.configure(background='#8673bd')

        img=Image.open(r"images/indexbg.jpg")
        img=img.resize((1275,770),Image.ANTIALIAS)
        self.background=ImageTk.PhotoImage(img)

        bg_img=Label(self.root,image=self.background)
        bg_img.place(x=0,y=0,width=1275,height=650)


        student_btn=Button(self.root,text="User Info",command=self.userInfo,font=("Merriweather",16,"bold"),bg="#5f1e66",fg="white")
        student_btn.place(x=240,y=385,height=40,width=120)

        login_btn=Button(self.root,text="Login",command=self.login,font=("Merriweather",16,"bold"),bg="#5f1e66",fg="white")
        login_btn.place(x=600,y=385,height=40,width=120)

        logout_btn=Button(self.root,text="Logout",font=("Merriweather",16,"bold"),command=self.logout,bg="#5f1e66",fg="white")
        logout_btn.place(x=940,y=385,height=40,width=120)
    

    def userInfo(self):
        self.newWindow=Toplevel(self.root)
        self.app=User(self.newWindow,self.SRN)
    
    def login(self):
        self.newWindow=Toplevel(self.root)
        self.app=Login(self.newWindow,self.SRN)
    
    def logout(self):
        info=messagebox.askyesno("EXIT","Are you sure you want to exit ?",parent=self.root)
        if info>0:
            self.root.destroy()


if __name__=="__main__":
    root=Tk()
    obj=Index(root)
    root.mainloop()
