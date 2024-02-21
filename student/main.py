from tkinter import *
from tkinter import ttk,messagebox
from tkinter import font
from pymongo import MongoClient
from index import Index
import tkinter as tk
from change_pswd import ChangePassword

class Entry(tk.Entry):
    def __init__(self, master, placeholder,**argv):
        super().__init__(master)

        self.font=argv['font']
        self.txt_var=argv['textvariable']
        self.width=argv['width']
        self.placeholder = placeholder
        self._is_password = (True if placeholder == "Enter password" else False)

        self.configure(width=self.width,font=self.font,textvariable=self.txt_var)

        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

        self._state = 'placeholder'
        self.insert(0, self.placeholder)

    def on_focus_in(self, event):

        if self._is_password:
          self.configure(show='')

        if self._state == 'placeholder':
            self._state = ''
            self.delete('0', 'end')

    def on_focus_out(self, event):
        if not self.get():
          if self._is_password:
            self.configure(show='')

          self._state = 'placeholder'
          self.insert(0, self.placeholder)


class Student:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1275x650+0+0")
        self.root.title("Student")

        self.root.configure(background='#9e69cf')

        self.SRN=StringVar()
        self.pswd=StringVar()

        login_frame=Frame(self.root,bd=2,bg="#5b295e")
        login_frame.place(x=440,y=110,height=400,width=400)

        txt_frame=Label(self.root,text="LOGIN PAGE",bg="#5b295e",fg="#1e1c1f",font=("Merriweather",20,"bold"))
        txt_frame.place(x=555,y=160,height=40,width=170)

        # SRN FIELD
        sID_entry=Entry(self.root,"Enter SRN",textvariable=self.SRN,width=25,font=("Helvetica",13,"bold"))
        sID_entry.pack()
        sID_entry.place(x=545,y=245,width=190,height=50)

        # PASSWORD FIELD
        pswd_entry=Entry(self.root,"Enter password",textvariable=self.pswd,width=25,font=("Helvetica",13,"bold"))
        pswd_entry.pack()
        pswd_entry.place(x=545,y=315,width=190,height=50)

        # New password btn
        newpswdBtn=Button(self.root,text="CHANGE PASSWORD",command=self.change_pswd)
        newpswdBtn.place(x=510,y=395,height=40,width=135)

        # Submit Button
        sbmtBtn=ttk.Button(self.root,text="SUBMIT",command=self.validate_user)
        sbmtBtn.place(x=665,y=395,height=40,width=90)




    def validate_user(self):
        cluster=MongoClient("mongodb+srv://Achyuth:MongoDB123!@cluster0.9eofd.mongodb.net/face_recognition?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
        db=cluster["face_recognition"]
        collect=db["password"]

        check=collect.find_one({"_id":self.SRN.get()},{"_id":1,"name":1,'password':1})
    
        if check and check["password"]==self.pswd.get():
            messagebox.showinfo("SUCCESS",f"Welcome {check['name']}",parent=self.root)
            self.newWindow=Toplevel(self.root)
            self.app=Index(self.newWindow,self.SRN.get())
            
        else:
            messagebox.showerror("FAILED","INVALID USER",parent=self.root)
        
    
    def change_pswd(self):
        self.newWindow=Toplevel(self.root)
        self.app=ChangePassword(self.newWindow)


if __name__=="__main__":
    root=Tk()
    obj=Student(root)
    root.mainloop()
