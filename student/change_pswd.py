from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from pymongo import MongoClient


class ChangePassword:

    def __init__(self,root):
        self.root=root
        self.root.geometry("1275x650+0+0")
        self.root.configure(background='#0f663e')
        self.root.title("CHANGE PASSWORD")

        self.SRN=StringVar(self.root)
        self.curpswd=StringVar(self.root)
        self.newpswd=StringVar(self.root)
        self.re_newpswd=StringVar(self.root)

        cur_course_frame=LabelFrame(self.root,bd=2,relief=RIDGE,font=("times new roman",15,"bold"),bg="#a8325e")
        cur_course_frame.place(x=375,y=110,width=500,height=300)

        # SRN
        SRN_label=Label(cur_course_frame,text="Enter your SRN",font=("times new roman",15,"bold"),bg="#5bbd42")
        SRN_label.grid(row=0,column=0,padx=12,pady=12,sticky=W)

        SRN_entry=ttk.Entry(cur_course_frame,textvariable=self.SRN,width=16,font=("times new roman",13,"bold"))
        SRN_entry.grid(row=0,column=1,padx=12,pady=12,sticky=W)

        # Current Password
        curpswd_label=Label(cur_course_frame,text="Enter your current password",font=("times new roman",15,"bold"),bg="#5bbd42")
        curpswd_label.grid(row=2,column=0,padx=12,pady=12,sticky=W)

        curpswd_entry=ttk.Entry(cur_course_frame,textvariable=self.curpswd,show='',width=16,font=("times new roman",13,"bold"))
        curpswd_entry.grid(row=2,column=1,padx=12,pady=12,sticky=W)

        # New Password
        newpswd_label=Label(cur_course_frame,text="Enter your new password",font=("times new roman",15,"bold"),bg="#5bbd42")
        newpswd_label.grid(row=4,column=0,padx=12,pady=12,sticky=W)

        newpswd_entry=ttk.Entry(cur_course_frame,textvariable=self.newpswd,show='',width=16,font=("times new roman",13,"bold"))
        newpswd_entry.grid(row=4,column=1,padx=12,pady=12,sticky=W)

        # Re-enter New Password
        re_newpswd_label=Label(cur_course_frame,text="Re-enter your new password",font=("times new roman",15,"bold"),bg="#5bbd42")
        re_newpswd_label.grid(row=6,column=0,padx=12,pady=12,sticky=W)

        re_newpswd_entry=ttk.Entry(cur_course_frame,textvariable=self.re_newpswd,show='',width=16,font=("times new roman",13,"bold"))
        re_newpswd_entry.grid(row=6,column=1,padx=12,pady=12,sticky=W)

        # Submit button
        sbmtBtn=ttk.Button(self.root,text="SUBMIT",command=self.validate_pswd_change)
        sbmtBtn.place(x=600,y=340,height=40,width=90)
    

    def validate_pswd_change(self):
        cluster=MongoClient("mongodb+srv://Achyuth:MongoDB123!@cluster0.9eofd.mongodb.net/face_recognition?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
        db=cluster["face_recognition"]
        collect=db["password"]

        check=collect.find_one({"_id":self.SRN.get()},{'_id':1})
        if not check:
            messagebox.showerror("ERROR","NO SUCH SRN PRESENT",parent=self.root)

        check=collect.find_one({"_id":self.SRN.get(),"password":self.curpswd.get()},{'password':1})
        if not check:
            messagebox.showerror("ERROR","WRONG ENTRY FOR CURRENT PASSWORD FIELD",parent=self.root)
        
        elif self.re_newpswd.get()!=self.newpswd.get():
            messagebox.showerror("PASSWORDS NOT MATCHING","RE-ENTER NEW PASSWORDS",parent=self.root)
        
        else:
            lowercase,uppercase,digits='','',''
            for i in range(26):
                if i<10:
                    digits+=str(i)
                lowercase+=chr(i+97)
                uppercase+=chr(i+65)
                
            specialChars='!@#$&?'  

            if len(self.newpswd.get())<8:
                messagebox.showerror("PASSWORD LENGTH","The length of the new password should be of atleast 8 characters",parent=self.root)

            lcase,ucase,dig,sp=0,0,0,0
            for i in self.newpswd.get():
                if i in lowercase:
                    lcase+=1
                
                if i in uppercase:
                    ucase+=1
                
                if i in digits:
                    dig+=1
                
                if i in specialChars:
                    sp+=1
            
            prob=''
            if lcase==0:
                prob+='Atleast one lowercase letter should be present.'

            if ucase==0:
                prob+='Atleast one uppercase letter should be present.'

            if dig==0:
                prob+='Atleast one digit should be present.'

            if sp==0:
                prob+='Atleast one special character should be present.'
            
            if prob:
                messagebox.showerror("ERROR","The issues are :"+prob,parent=self.root)
            
            # print(self.newpswd.get(),self.re_newpswd.get())
            if not prob and len(self.re_newpswd.get())>=8:
                collect.update_one({"_id":self.SRN.get()},{"$set":{"password":self.re_newpswd.get()}})
                messagebox.showinfo("SUCCESS","PASSWORDS SUCCESSFULLY UPDATED",parent=self.root)