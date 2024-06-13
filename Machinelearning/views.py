from django.utils import timezone
from .models import *
# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from public.models import *
from django.contrib import messages

from random import randint
import os
from PIL import Image
import tkinter as tk
from tkinter import *
import csv
import numpy as np
from PIL import Image,ImageTk
import pandas as pd
import datetime
import time
from datetime import date
from django.shortcuts import render,redirect

import cv2
import numpy as np
import tensorflow as tf
import math

from tensorflow.keras import Model
from tensorflow.keras.layers import (
    Add,
    Concatenate,
    Conv2D,
    Input,
    Lambda,
    LeakyReLU,
    UpSampling2D,
    ZeroPadding2D,
    BatchNormalization
)
from tensorflow.keras.regularizers import l2
import wget
#####Window is our Main frame of system
window = tk.Tk()
window.title("FAMS-Face Recognition Based Attendance Management System")

window.geometry('1280x720')
window.configure(background='snow')


# final_out = {

#     "head_down": 0,
#     "head_up": 0,
#     "head_right": 0,
#     "head_left" : 0,
#     "mouth_open" : 0,
#     "looking_left" : 0,
#     "looking_right" : 0,
#     "looking_up" : 0,
#     "phone_detected": 0,
#     "no_person": 0,
#     "mutiple_person":0
#     }





   

# #person & phone



#     # return render_template("detection.html")


























def getImagesAndLabels(path):
    
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    
    # create empth face list
    faceSamples = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        
        # getting the Id from the image

        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        
        # extract the face from the training image sample
        faces = detector.detectMultiScale(imageNp)
        
        # If a face is there then append that in the list as well as Id of it
        for (x, y, w, h) in faces:
            
            faceSamples.append(imageNp[y:y + h, x:x + w])
            Ids.append(Id)
    return faceSamples, Ids



# #train image
def trainimg():
    # print("hello")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    global detector
    detector = cv2.CascadeClassifier("C:/Users/VICTUS/Desktop/NEW_ATTENDENCE/attendence_venv/employe_project/Machinelearning/haarcascade_frontalface_default.xml")
    # detector_local = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    try:
        global faces,Id
        # print("hiiiiii")
        faces, Id = getImagesAndLabels("C:/Users/VICTUS/Desktop/NEW_ATTENDENCE/attendence_venv/employe_project/Machinelearning/TrainingImage")

       
    except Exception as e:
        l='please make "TrainingImage" folder & put Images'
        Notification.configure(text=l, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
        Notification.place(x=350, y=400)
       
    recognizer.train(faces, np.array(Id))
    try:
        
        recognizer.save("C:/Users/VICTUS/Desktop/NEW_ATTENDENCE/attendence_venv/employe_project/Machinelearning/TrainingImageLabel/Trainner.yml")
    except Exception as e:
        
        q='Please make "TrainingImageLabel" folder'
        Notification.configure(text=q, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
        Notification.place(x=350, y=400)

    res = "Model Trained"  # +",".join(str(f) for f in Id)
    Notification.configure(text=res, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
    Notification.place(x=250, y=400)


# #capturing image

def take_img(request):
    print("here is the functionsss calll")
    try:
        print("hiiiiiiiiiiiiii")
        Name = request.POST.get('fname')
        print(Name)
        
        Enrollment = request.POST.get('registration')
        print(Enrollment)
        if Name == '':
            err_screen()
        elif Enrollment == '':
            err_screen()
        else:
            try:

                cam = cv2.VideoCapture(0)
                detector = cv2.CascadeClassifier('C:/Users/VICTUS/Desktop/NEW_ATTENDENCE/attendence_venv/employe_project/Machinelearning/haarcascade_frontalface_default.xml')
                print("qwgdfgywe",detector)
                print("while is true1")
                print("while is true2")
                print("while is true3")
                Name = request.POST.get('fname')
                Enrollment = request.POST.get('registration')
                sampleNum = 0
                while (True):
                    print("while is true")
                    
                    ret, img = cam.read()
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                
                    faces = detector.detectMultiScale(gray, 1.3, 5)
                    print(faces)
                    for (x, y, w, h) in faces:
                        
                        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        # incrementing sample number
                        sampleNum = sampleNum + 1
                        print("Going to store:!!!!!!!!!!!!!")
                        

                        # saving the captured face in the dataset folder
                        cv2.imwrite("C:/Users/VICTUS/Desktop/NEW_ATTENDENCE/attendence_venv/employe_project/Machinelearning/TrainingImage/ " + Name + "." + Enrollment + '.' + str(sampleNum) + ".jpg",
                                    gray[y:y + h, x:x + w])
                        cv2.imshow('Frame', img)
                    # wait for 100 miliseconds
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        
                        break
                    # break if the sample number is morethan 100
                    elif sampleNum > 70:
                        
                        break
                cam.release()
                cv2.destroyAllWindows()
                ts = int(time.time())
                
                Date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                
                Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                
                row = [Enrollment, Name, Date, Time]
                

                with open('C:/Users/VICTUS/Desktop/NEW_ATTENDENCE/attendence_venv/employe_project/Machinelearning/StudentDetails/StudentDetails.csv', 'a+') as csvFile:
                    
                    writer = csv.writer(csvFile, delimiter=',')
                    writer.writerow(row)
                    csvFile.close()
                res = "Images Saved for Enrollment : " + Enrollment + " Name : " + Name
                print("helloooooooooooooooooooooooooooooooooooo",res)
               
                k= trainimg()
                Notification.configure(text=res, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
                Notification.place(x=250, y=400)
                
            except FileExistsError as F:
                f = 'Student Data already exists'
                Notification.configure(text=f, bg="Red", width=21)
                Notification.place(x=450, y=400)
        return JsonResponse({'success': True, 'message': 'Image captured successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
















# ###for choose subject and fill attendance


# import cv2
# # print(cv2._version_)

# # Add the following import at the beginning of your code



# # ...



def Fillattendances(request):
    today = timezone.now().date()

    uni=Attendence.objects.filter(current_date=today,emid=request.user.id,attendence="Present").first()
    if uni:
        messages.error(request, "Already Present")
        return redirect('/view_Attendence')
    now = time.time()
    future = now + 20
    user_detected = False

    if time.time() < future:
        print("---------------2----------------")
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        try:
            print("---------------3----------------")    
            recognizer.read("C:/Users/VICTUS/Desktop/NEW_ATTENDENCE/attendence_venv/employe_project/Machinelearning/TrainingImageLabel/Trainner.yml")
        except Exception as e:
         
            print("---------------4----------------")
            print("Errorsss",e)
            e = 'Model not found,Please train model'
            Notifica.configure(text=e, bg="red", fg="black", width=33, font=('times', 15, 'bold'))
            Notifica.place(x=20, y=250)

        harcascadePath = "C:/Users/VICTUS/Desktop/NEW_ATTENDENCE/attendence_venv/employe_project/Machinelearning/haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath)
        print("---------------5----------------")
        df = pd.read_csv("C:/Users/VICTUS/Desktop/NEW_ATTENDENCE/attendence_venv/employe_project/Machinelearning/StudentDetails/StudentDetails.csv")
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        col_names = ['Enrollment', 'Name', 'Date', 'Time']
        attendance = pd.DataFrame(columns=col_names)
        a = Register.objects.get(id=request.user.id)
        current_user_enrollment = a.registrationid
        current_user_name = a.username
        while True:
            print("---------------6----------------")
            ret, im = cam.read()
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.2, 5)
            for (x, y, w, h) in faces:
                global Id
                Id, conf = recognizer.predict(gray[y:y + h, x:x + w])

                if (conf < 70):
                    print("----------------7------------------")
                    global aa
                    global current_date
                    global current_timeStamp
                    ts = time.time()
                    current_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    current_timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa = df.loc[df['Enrollment'] == Id]['Name'].values
                    global tt
                    tt = str(Id) + "-" + aa
                    En = '15624031' + str(Id)
                    attendance.loc[len(attendance)] = [Id, aa, current_date, current_timeStamp]
                    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 7)

                    cv2.putText(im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4)

                    print("Id",str(Id),"Username",aa, current_user_name)
                    print("Current user",current_user_enrollment)
                    print(type(aa))
                    print("typeof enroll",type(current_user_enrollment))
                    print(str(Id) == current_user_enrollment)
                    print(current_user_name in  aa)
                    user_detected = str(Id) == str(current_user_enrollment) and current_user_name in  aa
                    print("user_detected",user_detected)
                    # print(user_detected)
                    if type(user_detected) == type(True):
                        print("First Conditionsssss")
                        if user_detected:
                            cv2.putText(im, "User detected! Your Attendence Marked.", (10, 30),
                                        font, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
                            today = timezone.now().date()

                            att=Attendence.objects.filter(emid=request.user.id,current_date=today).first()
                            att.attendence = "Present"
                            att.current_time=timezone.now()
                            att.save()           

  
                        else:
                            cv2.putText(im, "User is not detected! Can't mark Attendence", (10, 30),
                                        font, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
                    else:
                        print("Second Conditionssssssssssssssss")
                        if user_detected.any():
                            cv2.putText(im, "User detected! You can now attend the exam.", (10, 30),
                                        font, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
                           
                        else:
                            cv2.putText(im, "User is not detected! You can not attend the exam.", (10, 30),
                                        font, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
                else:
                    Id = 'Unknown'
                    tt = str(Id)
                    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                    cv2.putText(im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4)

            if time.time() > future:
                break

            attendance = attendance.drop_duplicates(['Enrollment'], keep='first')
            cv2.imshow('Filling attedance..', im)
            key = cv2.waitKey(30) & 0xff
            if key == 27:
                break
        ts = time.time()
        current_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        current_timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour, Minute, Second = current_timeStamp.split(":")
        # fileName = "Attendance/" + "_" + current_date + "_" + Hour + "-" + Minute + "-" + Second + ".csv"
        # attendance = attendance.drop_duplicates(['Enrollment'], keep='first')

        # attendance.to_csv(fileName, index=False)
        cam.release()
        cv2.destroyAllWindows()
        print("user Detected",user_detected)
        if type(user_detected) == type(True):
            return redirect('/?user_detected=' + str(user_detected))
        else:
            return redirect('/?user_detected=' + str(user_detected.any()))



    return render("index.html")






    
