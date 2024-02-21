import re
from tkinter import *
from tkinter import ttk,messagebox
from pymongo import MongoClient

class User:

    def __init__(self,root,SRN):
        self.root=root
        self.SRN=SRN
        self.root.geometry("1275x650+0+0")
        # self.root.title("User")

        self.root.configure(background='#0f663e')

        cluster=MongoClient("mongodb+srv://Achyuth:MongoDB123!@cluster0.9eofd.mongodb.net/face_recognition?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
        db=cluster["face_recognition"]
        collect=db["student"]

        userData=collect.find_one({"_id":self.SRN})
        
        self.newName=StringVar(self.root,value=userData['name'])
        self.newEmail=StringVar(self.root,value=userData['email'])
        self.newPhone=StringVar(self.root,value=userData['phone'])
        self.newGender=StringVar(self.root,value=userData['gender'])

        title_lbl=Label(self.root,text="USER DETAILS",font=("Merriweather",36,"bold"),bg="white",fg="teal")
        title_lbl.place(x=15,y=25,height=52,width=1230)

        cur_course_frame=LabelFrame(self.root,bd=2,bg="#99c98d",relief=RIDGE,font=("times new roman",15,"bold"))
        cur_course_frame.place(x=325,y=110,width=600,height=425)

        # ------Dept----
        dep_label=Label(cur_course_frame,text="Department",font=("times new roman",15,"bold"),bg="#99c98d")
        dep_label.grid(row=0,column=0,padx=12,pady=12,sticky=W)

        dep_label=Label(cur_course_frame,text=userData['dept'],font=("times new roman",15,"bold"),bg="#99c98d")
        dep_label.grid(row=0,column=1,padx=12,pady=12,sticky=W)

        # -----Course----
        course_label=Label(cur_course_frame,text="Course",font=("times new roman",15,"bold"),bg="#99c98d")
        course_label.grid(row=0,column=2,padx=12,pady=12,sticky=W)

        course_label=Label(cur_course_frame,text=userData['course'],font=("times new roman",15,"bold"),bg="#99c98d")
        course_label.grid(row=0,column=3,padx=12,pady=12,sticky=W)

        # -----Sem----
        sem_label=Label(cur_course_frame,text="Semester",font=("times new roman",15,"bold"),bg="#99c98d")
        sem_label.grid(row=1,column=0,padx=12,pady=12,sticky=W)

        sem_label=Label(cur_course_frame,text=userData['sem'],font=("times new roman",15,"bold"),bg="#99c98d")
        sem_label.grid(row=1,column=1,padx=12,pady=12,sticky=W)

        #----year---
        year_label=Label(cur_course_frame,text="Year",font=("times new roman",15,"bold"),bg="#99c98d")
        year_label.grid(row=1,column=2,padx=12,pady=12,sticky=W)

        year_label=Label(cur_course_frame,text=userData['year'],font=("times new roman",15,"bold"),bg="#99c98d")
        year_label.grid(row=1,column=3,padx=12,pady=12,sticky=W)

        #----SRN-----
        SRN_label=Label(cur_course_frame,text="SRN",font=("times new roman",15,"bold"),bg="#99c98d")
        SRN_label.grid(row=2,column=0,padx=12,pady=12,sticky=W)

        SRN_label=Label(cur_course_frame,text=userData['_id'],font=("times new roman",15,"bold"),bg="#99c98d")
        SRN_label.grid(row=2,column=1,padx=12,pady=12,sticky=W)

        #---Teacher----
        teacher_label=Label(cur_course_frame,text="Teacher",font=("times new roman",15,"bold"),bg="#99c98d")
        teacher_label.grid(row=2,column=2,padx=12,pady=12,sticky=W)

        teacher_label=Label(cur_course_frame,text=userData['teacher'],font=("times new roman",15,"bold"),bg="#99c98d")
        teacher_label.grid(row=2,column=3,padx=12,pady=12,sticky=W)

        #---Name---
        name_label=Label(cur_course_frame,text="Name",font=("times new roman",15,"bold"),bg="#99c98d")
        name_label.grid(row=3,column=0,padx=12,pady=12,sticky=W)

        name_entry=ttk.Entry(cur_course_frame,textvariable=self.newName,width=16,font=("times new roman",13,"bold"))
        name_entry.grid(row=3,column=1,padx=12,pady=12,sticky=W)

        #---Email---
        email_label=Label(cur_course_frame,text="Email",font=("times new roman",15,"bold"),bg="#99c98d")
        email_label.grid(row=3,column=2,padx=12,pady=12,sticky=W)

        email_entry=ttk.Entry(cur_course_frame,textvariable=self.newEmail,width=16,font=("times new roman",13,"bold"))
        email_entry.grid(row=3,column=3,padx=12,pady=12,sticky=W)

        #---Phone---
        phone_label=Label(cur_course_frame,text="Phone",font=("times new roman",15,"bold"),bg="#99c98d")
        phone_label.grid(row=4,column=0,padx=12,pady=12,sticky=W)

        phone_entry=ttk.Entry(cur_course_frame,textvariable=self.newPhone,width=16,font=("times new roman",13,"bold"))
        phone_entry.grid(row=4,column=1,padx=12,pady=12,sticky=W)

        #---Gender---
        gender_label=Label(cur_course_frame,text="Gender",font=("times new roman",15,"bold"),bg="#99c98d")
        gender_label.grid(row=4,column=2,padx=12,pady=12,sticky=W)

        gender_entry=ttk.Entry(cur_course_frame,textvariable=self.newGender,width=16,font=("times new roman",13,"bold"))
        gender_entry.grid(row=4,column=3,padx=12,pady=12,sticky=W)

        #---Edit Button---
        edit_btn=Button(self.root,text="Edit",font=("Merriweather",16,"bold"),command=self.modify_details,bg="#966c7c",fg="white")
        edit_btn.place(x=560,y=420,height=40,width=120)
    

    # Modify student details
    def modify_details(self):
        try:
            cluster=MongoClient("mongodb+srv://Achyuth:MongoDB123!@cluster0.9eofd.mongodb.net/face_recognition?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
            db=cluster["face_recognition"]
            collect=db["student"]
            pswd=db['password']

            if self.checkName(self.newName.get()) and self.checkEmailID(self.newEmail.get()) and self.checkPhoneNumber(self.newPhone.get()) and self.checkGender(self.newGender.get()):
                collect.update_one({"_id":self.SRN},{"$set":{"name":self.newName.get(),"email":self.newEmail.get(),"phone":self.newPhone.get(),"gender":self.newGender.get()}})
                pswd.update_one({"_id":self.SRN},{"$set":{"name":self.newName.get()}})

                messagebox.showinfo("SUCCESS","User details modified",parent=self.root)
        except Exception as E:
            messagebox.showerror("ERROR",f"Issue : {str(E)}",parent=self.root)
        
    
    def checkName(self,Name):
        lowercase=set(chr(i+97) for i in range(26))
        uppercase=set(chr(i+65) for i in range(26))

        valid=lowercase.union(uppercase)
        for i in Name:
            if i not in valid:
                messagebox.showerror("ERROR","Name field should contain only alphabets",parent=self.root)
                return 0
        
        return 1
    
    def checkEmailID(self,Email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex,Email):
            return 1
        else:
            messagebox.showerror("ERROR","Invalid Email Field",parent=self.root)
            return 0
    
    def checkPhoneNumber(self,phNo):

        valid=set(str(i) for i in range(10))
        cnt,tmp=0,1

        for i in phNo:
            if i not in valid:
                messagebox.showerror("ERROR","Phone field should contain only digits",parent=self.root)
                return 0
            cnt+=1
        
        if cnt!=10:
            messagebox.showerror("ERROR","Phone field should contain exactly 10 digits",parent=self.root)
            tmp=0
        
        return tmp

    def checkGender(self,gender):
        lowercase=set(chr(i+97) for i in range(26))
        uppercase=set(chr(i+65) for i in range(26))

        valid=lowercase.union(uppercase)
        for i in gender:
            if i not in valid:
                messagebox.showerror("ERROR","Gender field should contain only alphabets",parent=self.root)
                return 0
        
        return 1

            
        



if __name__=="__main__":
    root=Tk()
    obj=User(root)
    root.mainloop()
