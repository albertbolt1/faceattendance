
import tkinter as tk
from tkinter import Message ,Text
import cv2,os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font
from keras_facenet import FaceNet
from teja import dictq
from teja import extract_face
import matplotlib.pyplot as plt
import sqlite3

window = tk.Tk()

window.title("Face_Recogniser")

dialog_title = 'QUIT'
dialog_text = 'Are you sure?'


window.configure(background='blue')


window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

def trackimage():
    embedder = FaceNet()
    b=[]
    cap = cv2.VideoCapture(0)
    while True:
        ret,frame=cap.read()
        img1=extract_face(frame)
        plt.imshow(frame)
        img1=np.expand_dims(img1,axis=0)
        if(img1.any()):
            emb=embedder.embeddings(img1)
            emb=np.transpose(emb)
            min_dist=100
            for key,value in dictq.items():
                dist=np.linalg.norm(emb-value)
                b.append(dist)
                if dist<min_dist:
                    min_dist=dist
                    identity=key
            print(identity)
            if min_dist < 1.0:
                cv2.putText(frame, "Face : " + identity,(100,100),cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0,255), 2)
                unknown_yes_or_no='no'
            else:
                cv2.putText(frame,'no match',(100,100),cv2.FONT_HERSHEY_PLAIN,1.5,(0,0,255),2)
                unknown_yes_or_no='yes'
            cv2.imshow('face',frame)

            if cv2.waitKey(1) & 0xFF==27:
                break

    cap.release()
    cv2.destroyAllWindows()
    import pyttsx3
    engine = pyttsx3.init()
    if(unknown_yes_or_no=="yes"):
        engine.say("Good morning sorry we couldn't recognise you")
    else:
        str1="good morning "+identity+" your attendance has been recorded"
        engine.say(str1)
        import mysql.connector
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="albertbolt23",
            database="faceproject",
            auth_plugin='mysql_native_password'
            )

        mycursor = mydb.cursor()
        from datetime import date
        today1 = date.today() 

        sql = "INSERT INTO attendance values('%s','%s','morning')"%(identity,str(today1))

        mycursor.execute(sql)
        mydb.commit()

    engine.runAndWait()



message = tk.Label(window, text="attendance system",bg="Green"  ,fg="white"  ,width=30  ,height=3,font=('times', 30, 'italic bold underline')) 

message.place(x=200, y=20)


def exit1():
    exit()


trackImg = tk.Button(window, text="click here to mark attendance and wait till ur name shows up",wraplength=200,justify='left',command=trackimage  ,fg="red"  ,bg="yellow"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
trackImg.place(x=200, y=500)
quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,fg="red"  ,bg="yellow"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
quitWindow.place(x=800, y=500)
 
window.mainloop()