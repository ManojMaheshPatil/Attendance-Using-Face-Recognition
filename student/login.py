from tkinter import *
from tkinter import ttk,messagebox
import cv2
from pymongo import MongoClient
from mongotriggers import MongoTrigger
from PIL import Image,ImageTk
import os
from time import strftime
from datetime import datetime

curSec=0
curMin=0

class Login:
    def __init__(self,root,SRN):
        self.root=root
        self.SRN=SRN
        self.root.geometry("1275x650+0+0")
        # self.root.title("Login")

        self.root.configure(background='#8673bd')

        img=Image.open(r"images/loginbg.jpg")
        img=img.resize((1275,650),Image.ANTIALIAS)
        self.background=ImageTk.PhotoImage(img)

        bg_img=Label(self.root,image=self.background)
        bg_img.place(x=0,y=0,width=1275,height=650)


        f_rec_btn=Button(self.root,text="Click Me to Start Face Recognition!👇",command=self.face_recog,cursor="hand2",font=("Merriweather",16,"bold"),bg="#8f82d1",fg="black")
        f_rec_btn.place(x=735,y=345,width=380,height=60)

        cluster=MongoClient("mongodb+srv://Achyuth:MongoDB123!@cluster0.9eofd.mongodb.net/face_recognition?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
        db=cluster["face_recognition"]
        collect=db["student"]
        data=collect.find_one({'_id':self.SRN},{'_id':1,"name":1,"dept":1})
        self.data=tuple(data.values())


    def mark_attendance(self,data):

        cluster=MongoClient("mongodb+srv://Achyuth:MongoDB123!@cluster0.9eofd.mongodb.net/face_recognition?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
        db=cluster["face_recognition"]
        collect=db["attendance"]
        tmp=collect.find_one({"_id":data[0]})
        global curMin,curSec
        if not tmp:
            now=datetime.now()
            cur_date=now.strftime("%d-%m-%Y")
            # cur_time=now.strftime("%H:%M:%S")
            if curMin<10:
                curMin='0'+str(curMin)
            if curSec<10:
                curSec='0'+str(curSec)
            activeTime="{0}:{1:.0f}".format(curMin,curSec)
            collect.insert_one({"_id":data[0],"name":data[1],"branch":data[2],"date":cur_date,"active":activeTime,"status":'NA'})
            


    # -----Face Recognition--------
    def face_recog(self):

        def draw_boundary(img,classifier,scaleFactor,minNeighbors,clf,start):
            global curSec,curMin

            gray_image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image,scaleFactor,minNeighbors) #This contains faces in box 
           
            for (x,y,w,h) in features:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
                id,predict = clf.predict(gray_image[y:y+h,x:x+w])
                id=str(id)
                id='PES22018'+'0'*(5-len(id))+id
            
                # refer to "predict" formula : Remember : Lesser the predict , better is the measure (Don't get confused)
                confidence = int((100*(1-predict/300)))

                if id==self.SRN and confidence>75 : # Random number (But take more)
        
                    cv2.putText(img,f"ID : {self.data[0]}", (x,y-75), cv2.FONT_HERSHEY_COMPLEX, 0.8,(0,255,255),3)
                    cv2.putText(img,f"Name : {self.data[1]}", (x,y-50), cv2.FONT_HERSHEY_COMPLEX, 0.8,(0,255,255),3)
                    cv2.putText(img,f"Dept : {self.data[2]}", (x,y-25), cv2.FONT_HERSHEY_COMPLEX, 0.8,(0,255,255),3)
                    cv2.putText(img,"Active Time : {0}:{1:.0f}".format(curMin,curSec), (x-100,y-100), cv2.FONT_HERSHEY_COMPLEX, 0.8,(0,0,0),3)
                    end=datetime.now()
                    curSec+=float(tuple(str(end-start).split(":"))[-1])
                    if curSec>=60:
                        curMin+=1
                        curSec-=60
                    
                else:    
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
                    cv2.putText(img,"Unknown Face", (x,y-5), cv2.FONT_HERSHEY_COMPLEX, 0.8,(255,255,255),3)
                    cv2.putText(img,"Time : {0}:{1:.0f}".format(curMin,curSec), (x-100,y-100), cv2.FONT_HERSHEY_COMPLEX, 0.8,(0,0,0),3)


        def recognize(img,clf,faceCascade,start):
            draw_boundary(img, faceCascade, 1.1, 10,clf,start)  # 1.1 - Scaling Factor,10 -Min Neighbours
            return img

        faceCascade =  cv2.CascadeClassifier("haarcascade_frontalface_default.xml") # Detects Face (Haar Cascade Algo)
        clf=cv2.face.LBPHFaceRecognizer_create()  # LBPH algo , used to "recognize" . This algo is already trained in train.py
        # read from the classifier.xml file that has already been created in train.py file

        cluster=MongoClient("mongodb+srv://Achyuth:MongoDB123!@cluster0.9eofd.mongodb.net/face_recognition?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
        db=cluster["face_recognition"]
        collect=db["clfData"]

        # If file does not exist
        if not os.path.isfile("data.xml"):
            collect.update_one({"_id":self.SRN},{"$set":{"modified":1}})
            with open("data.xml","a",newline="\n") as f:
                f.close()

        # If file is empty
        if os.stat("data.xml").st_size==0:
            collect.update_one({"_id":self.SRN},{"$set":{"modified":1}})

        trainData=collect.find_one({"_id":self.SRN,"modified":1})
        
        if trainData:
            with open("data.xml",'w+',newline="\n") as f:
                f.writelines(trainData["data"])
                f.close()
            collect.update_one({"_id":self.SRN},{"$set":{"modified":0}})

        # retrieve data already stored 

        clf.read("data.xml") 
        

        #trigger
        # triggeredOn=cluster
        # trigger=MongoTrigger(triggeredOn)
        # trigger.register_update_trigger(self.doSomething,'face_recognition','student')

        # trigger.tail_oplog()


        video_cap = cv2.VideoCapture(0,cv2.CAP_DSHOW) # 0 means default camera

        while True:
            _,img = video_cap.read()
            start=datetime.now()
            img = recognize(img, clf, faceCascade,start)
            cv2.imshow("Welcome to Face Recognition",img)
            if cv2.waitKey(1)==27:
                break
        
        
        # trigger.stop_tail()
        
        self.mark_attendance(self.data)
        video_cap.release()
        cv2.destroyAllWindows()

    def doSomething(self,op_document):
        print("Student details modified")
        

if __name__=="__main__":
    root=Tk()
    obj=Login(root)
    root.mainloop()
