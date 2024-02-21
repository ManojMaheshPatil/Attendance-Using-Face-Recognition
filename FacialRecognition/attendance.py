from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
from pymongo import MongoClient
import os
import csv
from tkinter import filedialog

mydata=[]

class Attendance:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1275x750+0+0")
        self.root.title("Face Recognition System")

        #variables
        self.var_attendanceID=StringVar()
        # self.var_roll=StringVar()
        self.var_name=StringVar()
        self.var_dept=StringVar()
        self.var_time=StringVar()
        self.var_date=StringVar()
        self.var_attendance=StringVar()
        self.var_pat=StringVar()

        #title and background
        img = Image.open(r"img/bg_grey.jpg") # r is used to convert forward slash to back slash in path
        self.photoimg = ImageTk.PhotoImage(img)

        f_lbl = Label(self.root , image=self.photoimg)
        f_lbl.place(x=0,y=0,width=1275,height=750) # Remember: the dimensions should match with that what you have written earlier

        title_lbl=Label(f_lbl,text="Attendance Record",font=("times new roman",35,"bold"),bg="grey",fg="white")
        title_lbl.place(x=0,y=0,width=1260,height=42)

        # Frame
        main_frame=Frame(f_lbl,bd=2,bg="grey")
        main_frame.place(x=5,y=45,width=1265,height=710)

        # Left label frame
        Left_frame=LabelFrame(main_frame,bd=2,bg="grey",relief=RIDGE,text="Student Details",font=("time new roman",12,"bold"))
        Left_frame.place(x=20,y=20,width=570,height=500)

        #Attendance ID
        attendanceID_label=Label(Left_frame, text="SRN",bg="grey",font=("comicsansns",13,"bold"))
        attendanceID_label.grid(row=0,column=0,padx=5,pady=16,sticky=W)

        attendanceID_entry=ttk.Entry(Left_frame,width=15,textvariable=self.var_attendanceID,font=("time new roman",13,"bold"),state="readonly")
        attendanceID_entry.grid(row=0,column=1,padx=5,pady=16,sticky=W)

        #Name
        nameLabel=Label(Left_frame,text="Name:",bg="grey",font=("comicsansns",13, "bold"))
        nameLabel.grid(row=0,column=2,padx=5,pady=16,sticky=W)

        name_entry=ttk.Entry(Left_frame,width=15,textvariable=self.var_name,font=("comicsansns",13,"bold"),state="readonly")
        name_entry.grid(row=0,column=3,padx=5,pady=16,sticky=W)

        #Department
        deptLabel=Label(Left_frame,text="Department:",bg="grey",font=("comicsansns",13, "bold"))
        deptLabel.grid(row=1,column=0,padx=5,pady=16,sticky=W)

        dept_entry=ttk.Entry(Left_frame,width=15,textvariable=self.var_dept,font=("comicsansns",13,"bold"),state="readonly")
        dept_entry.grid(row=1,column=1,padx=5,pady=16,sticky=W)

        #Time
        timeLabel=Label(Left_frame,text="Time:",bg="grey",font=("comicsansns",13, "bold"))
        timeLabel.grid(row=1,column=2,padx=5,pady=16,sticky=W)

        time_entry=ttk.Entry(Left_frame,width=15,textvariable=self.var_time,font=("comicsansns",13,"bold"),state="readonly")
        time_entry.grid(row=1,column=3,padx=5,pady=16,sticky=W)

        #Date
        dateLabel=Label(Left_frame,text="Date:",bg="grey",font=("comicsansns",13, "bold"))
        dateLabel.grid(row=2,column=0,padx=5,pady=16,sticky=W)

        date_entry=ttk.Entry(Left_frame,width=15,textvariable=self.var_date,font=("comicsansns",13,"bold"),state="readonly")
        date_entry.grid(row=2,column=1,padx=5,pady=16,sticky=W)

        #Attendance as Present/Absent
        rollLabel=Label(Left_frame,text="Status:",bg="grey",font=("comicsansns",13, "bold"))
        rollLabel.grid(row=2,column=2,padx=5,pady=16,sticky=W)

        roll_entry=ttk.Entry(Left_frame,width=15,textvariable=self.var_attendance,font=("comicsansns",13,"bold"),state="readonly")
        roll_entry.grid(row=2,column=3,padx=5,pady=16,sticky=W)
        
        # Predefined Active Time
        pre_active_time_Label=Label(Left_frame,text="Enter Predefined Active Time:",bg="grey",font=("comicsansns",13, "bold"))
        pre_active_time_Label.place(x=2,y=200,height=40,width=275)

        pre_active_time__entry=ttk.Entry(Left_frame,textvariable=self.var_pat,font=("comicsansns",13,"bold"))
        pre_active_time__entry.place(x=265,y=200,height=35,width=150)


        # Teacher Name
        
        self.teacherName=StringVar()
        searchTeacher_label=Label(Left_frame,text="Teacher : ",font=("Helvetica",13,"bold"),bg="grey")
        searchTeacher_label.place(x=2,y=270,width=175,height=40)

        comboValues=tuple()
        comboValues+=("Select",)

        cluster=MongoClient("mongodb+srv://Achyuth:MongoDB123!@cluster0.9eofd.mongodb.net/face_recognition?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
        db=cluster["face_recognition"]
        collect=db["student"]
        teacherNames=list(collect.find({},{"teacher":1}))
       
        s=set()
        for i in teacherNames:
            s.add(i["teacher"])
        
        for i in s:
            comboValues+=(i,)
        
        search_combo=ttk.Combobox(Left_frame,font=("times new roman",13,"bold"),textvariable=self.teacherName,state="readonly",width=155)
        search_combo["values"]=comboValues
        search_combo.current(0)
        search_combo.place(x=265,y=270,width=150,height=35)

        # Mark attendance
        markAttendance=Button(main_frame,text="Mark Attendance",command=self.mark_attendance ,width=17,font=("comicsansns",13, "bold"),bg="white")
        markAttendance.place(x=120,y=370,width=150,height=35) 


        AttendanceReport=Button(main_frame,text="Attendance Report",command=self.generateReport ,width=17,font=("comicsansns",13, "bold"),bg="white")
        AttendanceReport.place(x=120,y=450,width=150,height=35)



        #button frame
        btn_frame=Frame(main_frame,bd=2,relief=RIDGE,bg="grey")
        btn_frame.place(x=250,y=542,width=800,height=35)

        getData=Button(main_frame,text="Store Data",command=self.getData ,width=17,font=("comicsansns",13, "bold"),bg="white")
        getData.place(x=250,y=542,width=200,height=35)

        import_csv=Button(main_frame,text="Import CSV",command=self.importCSV,width=17,font=("comicsansns",13, "bold"),bg="white")
        import_csv.place(x=450,y=542,width=200,height=35)

        Export_csv=Button(main_frame,text="Export CSV",command=self.exportCSV,width=17,font=("comicsansns",13, "bold"),bg="white")
        Export_csv.place(x=650,y=542,width=200,height=35)

        Reset_csv=Button(main_frame,text="Reset",width=17,command=self.reset_data,font=("comicsansns",13, "bold"),bg="white")
        Reset_csv.place(x=850,y=542,width=200,height=35)

        # Right label frame
        Right_frame=LabelFrame(main_frame,bd=2,bg="grey",relief=RIDGE,text="Attendance Details",font=("time new roman",12,"bold"))
        Right_frame.place(x=590,y=20,width=660,height=500)

        table_frame=Frame(Right_frame,bd=2,relief=RIDGE,bg="grey")
        table_frame.place(x=2,y=2,width=650,height=474)

        #scroll bar table
        scroll_x=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(table_frame,orient=VERTICAL)

        self.AttendanceReportTable=ttk.Treeview(table_frame,column=("ID","Name","Department","Active","Date","Attendance"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)

        scroll_x.config(command=self.AttendanceReportTable.xview)
        scroll_y.config(command=self.AttendanceReportTable.yview)

        self.AttendanceReportTable.heading("ID",text="SRN")
        self.AttendanceReportTable.heading("Name",text="Name")
        self.AttendanceReportTable.heading("Department",text="Department")
        self.AttendanceReportTable.heading("Active",text="Active")
        self.AttendanceReportTable.heading("Date",text="Date")
        self.AttendanceReportTable.heading("Attendance",text="Attendance")

        self.AttendanceReportTable["show"]="headings"

        self.AttendanceReportTable.column("ID",width=100)
        self.AttendanceReportTable.column("Name",width=100)
        self.AttendanceReportTable.column("Department",width=100)
        self.AttendanceReportTable.column("Active",width=100)
        self.AttendanceReportTable.column("Date",width=100)
        self.AttendanceReportTable.column("Attendance",width=100)

        self.AttendanceReportTable.pack(fill=BOTH,expand=1)

        self.AttendanceReportTable.bind("<ButtonRelease>",self.get_cursor)

#===========Fetch data===================

    def mark_attendance(self):
        try:
            cluster=MongoClient("mongodb+srv://Achyuth:MongoDB123!@cluster0.9eofd.mongodb.net/face_recognition?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
            db=cluster["face_recognition"]
            collect=db["student"]
            allusersData=list(collect.find({"teacher":self.teacherName.get()},{"_id":1,"name":1,"dept":1}))

            collect=db["attendance"]
            classAttendedUsersData=list(collect.find({}))

            UsersPresent=set()
            for i in classAttendedUsersData:
                UsersPresent.add(i["_id"])

            classAttendedUsers=dict()
            for i in classAttendedUsersData:
                classAttendedUsers[i["_id"]]=i

            

            filename=filedialog.asksaveasfilename(initialdir=os.getcwd(),title="Save as CSV",filetypes=(("CSV File","*.csv"),("All File","*.*")), parent=self.root)
            with open(filename,"w+",newline="\n") as f:
                f.writelines("SRN,Name,Dept,ActiveTime,Date,Status\n")
                for user in allusersData:
                    if user["_id"] in UsersPresent:
                        usr=classAttendedUsers[user["_id"]]
                        ActiveTime=usr["active"]
                        Date=usr["date"]
                        minspresent=int(usr['active'][0:2])*60+int(usr['active'][3:])
                        minsrequired=int(self.var_pat.get()[0:2])*60+int(self.var_pat.get()[3:])
                        if minspresent>=minsrequired:
                            status="Present"
                        else:
                            status="Absent"
                    else:
                        Date="NA"
                        ActiveTime="00:00"
                        status="Absent"

                    f.writelines(f"{user['_id']},{user['name']},{user['dept']},{ActiveTime},{Date},{status}\n")
                    
            self.importCSV()
            
            messagebox.showinfo("SUCCESS",f"Data Stored from database onto {filename}",parent=self.root)
        except Exception as E:
            messagebox.showerror("FAILED",f"Issue : {str(E)}",parent=self.root)
    


    def generateReport(self):

        cluster=MongoClient("mongodb+srv://Achyuth:MongoDB123!@cluster0.9eofd.mongodb.net/face_recognition?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
        db=cluster["face_recognition"]
        collect=db["student"]
        allusersData=list(collect.find({"teacher":self.teacherName.get()},{"_id":1,"name":1,"dept":1}))
        allUsersInfo=dict()
        for i in allusersData:
            allUsersInfo[i["_id"]]=i
            allUsersInfo[i["_id"]]["NoOfPresentDays"]=0
        
        TotalNoOfDays=0

        filenames=filedialog.askopenfilenames(initialdir=os.getcwd(),title="Open CSV files",filetypes=(("CSV File","*.csv"),("All File","*.*")), parent=self.root)
        AttendanceReport=filedialog.asksaveasfilename(initialdir=os.getcwd(),title="Save as CSV",filetypes=(("CSV File","*.csv"),("All File","*.*")), parent=self.root)
        AttendanceReport+='.csv'
        
        # print(filenames)
        for files in filenames:
            flag=0
            with open(files,"r+") as f:
                csvread=list(csv.reader(f))
                print(csvread)
                firstLine=csvread[0]
                print(firstLine)
                if 'Total No of Days' in firstLine:
                    TotalNoOfDays+=int(csvread[1][-1])
                
                else:
                    TotalNoOfDays+=1

                for i in csvread[1:]:
                    print(i)
                    SRN=i[0]
                    
                    if 'Present' in i:
                        cnt=1
                    
                    elif 'Absent' in i:
                        cnt=0

                    else:
                        cnt=int(i[-2])

                    crtVal=int(allUsersInfo[SRN]["NoOfPresentDays"])
                    allUsersInfo[SRN]["NoOfPresentDays"]=crtVal+cnt
                
            
        fields=["SRN","Name","Dept","No of days present","Total No of Days"]

        rows=[]
        for user,val in allUsersInfo.items():
                rows.append([val['_id'],val['name'],val['dept'],str(val['NoOfPresentDays']),str(TotalNoOfDays)])

        with open(AttendanceReport,mode="w",newline="\n") as myfile:
            export_write=csv.writer(myfile,delimiter=",")

            export_write.writerow(fields)
            export_write.writerows(rows)
                


    def getData(self):
        try:
            cluster=MongoClient("mongodb+srv://Achyuth:MongoDB123!@cluster0.9eofd.mongodb.net/face_recognition?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
            db=cluster["face_recognition"]
            collect=db["attendance"]
            allusersData=collect.find({})
            allusersData=list(allusersData)
            filename=filedialog.asksaveasfilename(initialdir=os.getcwd(),title="Open CSV",filetypes=(("CSV File","*.csv"),("All File","*.*")), parent=self.root)
            with open(filename,"w+",newline="\n") as f:
                for user in allusersData:
                    f.writelines(f"{user['_id']},{user['name']},{user['branch']},{user['active']},{user['date']},{user['status']}\n")
                    
            self.importCSV()
            
            messagebox.showinfo("SUCCESS",f"Data Stored from database onto {filename}",parent=self.root)
        except Exception as E:
            messagebox.showerror("FAILED",f"Issue : {str(E)}",parent=self.root)
            

    def fetchData(self,rows):
        self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
        for i in rows[1:]:
            self.AttendanceReportTable.insert("",END,values=i)
    
    #import CSV working
    def importCSV(self):
        global mydata
        mydata.clear()
        filename=filedialog.askopenfilename(initialdir=os.getcwd(),title="Open CSV",filetypes=(("CSV File","*.csv"),("All File","*.*")), parent=self.root)
        print(filename)
        with open(filename) as myfile:
            csvread=csv.reader(myfile,delimiter=",")
            for i in csvread:
                mydata.append(i)
            self.fetchData(mydata)

    #import CSV working
    def exportCSV(self):
        try:
            if len(mydata)<1:
                messagebox.showerror("No Data","No Data Found to Export",parent=self.root)
                return False
            filename=filedialog.asksaveasfilename(initialdir=os.getcwd(),title="Open CSV",filetypes=(("CSV File","*.csv"),("All File","*.*")), parent=self.root)
            filename+='.csv'
        
            with open(filename,mode="w",newline="") as myfile:
                export_write=csv.writer(myfile,delimiter=",")
                for i in mydata:
                    export_write.writerow(i)
                messagebox.showinfo("Data Export","Data was Exported Successfully to "+os.path.basename(filename),parent=self.root)
        except Exception as es:
            messagebox.showerror("Error",f"Due to:{str(es)}",parent=self.root)
    
    def get_cursor(self,event=""):
        cursor_row=self.AttendanceReportTable.focus()
        content=self.AttendanceReportTable.item(cursor_row)
        rows=content['values']
        self.var_attendanceID.set(rows[0])
        self.var_name.set(rows[1])
        self.var_dept.set(rows[2])
        self.var_time.set(rows[3])
        self.var_date.set(rows[4])
        self.var_attendance.set(rows[5])

    def reset_data(self):
        self.var_attendanceID.set("")
        self.var_name.set("")
        self.var_dept.set("")
        self.var_time.set("")
        self.var_date.set("")
        self.var_attendance.set("")
        

if __name__ == "__main__":
    root=Tk()
    obj=Attendance(root)
    root.mainloop()