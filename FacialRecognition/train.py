import os
from tkinter import *
from tkinter import ttk,messagebox
import PIL
from PIL import Image,ImageTk
import cv2
import numpy as np
from pymongo import MongoClient

class Train:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1275x750+0+0")
        self.root.title("Facial Recognition System")

        self.trainSRN=StringVar()

        img=Image.open(r"img/bgtrain.jpg")
        img=img.resize((1275,770),Image.ANTIALIAS)
        self.background=ImageTk.PhotoImage(img)

        bg_img=Label(self.root,image=self.background)
        bg_img.place(x=0,y=0,width=1275,height=770)

        title_lbl=Label(self.root,text="TRAIN DATASET",font=("Merriweather",36,"bold"),bg="white",fg="teal")
        title_lbl.place(x=15,y=25,height=52,width=1230)

        train_btn=Button(self.root,text="TRAIN DATA",command=self.train_classifier,font=("Merriweather",16,"bold"),bg="red",fg="white")
        train_btn.place(x=590,y=400,height=50,width=150)

        search_label=Label(self.root,text="Train : ",font=("Helvetica",13,"bold"),bg="red")
        search_label.place(x=540,y=280,width=85,height=55)

        comboValues=tuple()
        comboValues+=("Select",)

        cluster=MongoClient("mongodb+srv://Achyuth:MongoDB123!@cluster0.9eofd.mongodb.net/face_recognition?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
        db=cluster["face_recognition"]
        collect=db["student"]
        photoTaken=list(collect.find({"photo":"Yes"},{"_id":1}))
        for i in photoTaken:
            comboValues+=(i["_id"],)
        
        search_combo=ttk.Combobox(self.root,font=("times new roman",13,"bold"),textvariable=self.trainSRN,state="readonly",width=155)
        search_combo["values"]=comboValues
        search_combo.current(0)
        search_combo.place(x=650,y=280,width=155,height=55)

    def train_classifier(self):
        dir="data/"+self.trainSRN.get()
        path=[]

        for img_path in os.listdir(dir):
            imgPath=dir+'/'+img_path
            path.append(imgPath)
        faces,ids=[],[]

        for img in path:
            gray_img=Image.open(img).convert("L") # convert to grayscale
            imgNP=np.array(gray_img,'uint8')
            id=int(os.path.split(img)[1].split('_')[0])
            faces.append(imgNP)
            ids.append(id)
            cv2.imshow("Training",imgNP)
            cv2.waitKey(1)==13
        ids=np.array(ids)

        # save and train the classifier
        clf=cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces,ids)

        clf.write("classifier.xml")
        with open("classifier.xml",'r+',newline="\n") as f:
            clfData=f.readlines()
            f.close()

        cluster=MongoClient("mongodb+srv://Achyuth:MongoDB123!@cluster0.9eofd.mongodb.net/face_recognition?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
        db=cluster["face_recognition"]
        collect=db["clfData"]
        
        tmp=collect.find_one({"_id":self.trainSRN.get()})
        if tmp:
            collect.update_one({"_id":self.trainSRN.get()},{"$set":{'data':clfData,'modified':1}})
        else:
            collect.insert_one({"_id":self.trainSRN.get(),'data':clfData,'modified':1})

        cv2.destroyAllWindows()
        messagebox.showinfo("Success",f"Training dataset of {self.trainSRN.get()} completed",parent=self.root)


if __name__=="__main__":
    root=Tk()
    obj=Train(root)
    root.mainloop()
