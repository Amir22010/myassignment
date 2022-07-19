# -*- coding: utf-8 -*-
"""
Created on Fri July 15 2022

@author: Amir Khan
"""
from flask import Flask, render_template,request,url_for,jsonify,send_file,redirect,flash
import cv2
import os
import time
import numpy as np
import base64
import urllib
from utils import Model
import sqlite3

app = Flask(__name__)
app.secret_key = 'super secret key'

def get_db_connection():
    '''
    Get db sqlite3 connection
    '''
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

print("[INFO] loading face detector...")
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def crop_face(image):
    '''
    for now only applicable to one face of input image
    '''
    #convert rgb to gray
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #detect faces
    faces = face_cascade.detectMultiScale(grayImage, 1.3, 2)
    # no of faces
    numfaces = len(faces)
    if len(faces) == 0:
        print("No faces found")
        return False
    else:
        print("Number of faces detected: " + str(faces.shape[0]))
        for (x,y,w,h) in faces:
            #crop face from input image feed
            faces = image[y:y + h, x:x + w]
        try:
            #create directory for input image saving
            os.makedirs(os.path.join('application_data', 'input_image'), exist_ok=True)
            #save input image
            cv2.imwrite(os.path.join('application_data', 'input_image', 'input_image.jpg'),faces)
        except Exception as e:
            print(e)
        return True

def crop_face_register(image):
    '''
    for now only applicable to one face of input image to register
    '''
    #convert rgb to gray
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #detect faces
    faces = face_cascade.detectMultiScale(grayImage, 1.3, 2)
    numfaces = len(faces)
    if len(faces) == 0:
        return "No faces found"
    else:
        print("Number of faces detected: " + str(faces.shape[0]))
        for (x,y,w,h) in faces:
            #crop face from input image feed
            faces = image[y:y + h, x:x + w]
        return faces

## route to default page
@app.route('/')
def index():
    '''
    Default flask route to main page
    '''
    conn = get_db_connection()
    ## route to retrive the list of registered users from database
    name_lists = conn.execute('SELECT user,created FROM users').fetchall()
    ## route to retrive the list of siamese model results from database
    result_lists = conn.execute('SELECT result,created FROM results').fetchall()
    conn.close()
    return render_template('index.html', posts=name_lists, results=result_lists)

## route to authenticate user
@app.route('/analyse',methods=['GET','POST'])
def analyse():
    '''
    Authenticate Function
    only applicable to 1 face, for now
    '''
    if request.method == 'POST':
        ## get input video feed face
        file = request.form['file']
        ## convert input image string to valid string
        response = urllib.request.urlopen(file)
        ## get db connection
        conn = get_db_connection()
        ## decode the input image string
        inimage = cv2.imdecode(np.fromstring(response.file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        #check if input image contains face or not
        if crop_face(inimage):
            conn = get_db_connection()
            ## get all registered user's names with their faces
            registered_users = conn.execute('SELECT user,content FROM users').fetchall()
            if len(registered_users) !=0:
                ## iterate all users 
                for index,value in enumerate(registered_users):
                    ## make each folder of user name
                    os.makedirs(os.path.join('application_data', 'verification_images', value['user']), exist_ok=True)
                    response = urllib.request.urlopen(value['content'])
                    reg_user = cv2.imdecode(np.fromstring(response.file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
                    # save the processed cropped face to particular user folder
                    cv2.imwrite(os.path.join('application_data', 'verification_images', value['user'], value['user']+'_'+str(index)+'.jpg'),reg_user)
                ## load siamese trained model
                p = Model()
                ## call authenticate function
                r = p.verify()
                ## if contains results
                if len(r) !=0:
                    ## get max confidence score and name given by siamese model
                    Keymax = max(zip(r.values(), r.keys()))
                    ## if confidence score > 0.4 [its ok to start with this score, later we can increase score]
                    if Keymax[0] >= 0.4:
                        result = 'Authenticate User name - {}, Confidence Score - {:.2f} %'.format(Keymax[1],Keymax[0]*100)
                    else:
                        result = 'Please register your name and face'
                else:
                    result = 'Please register your name and face'
            else:
                result = 'Please register at least one of your name and face'
        else:
            result = 'No face detected'
        ## insert results into db
        conn.execute('INSERT INTO results (result) VALUES (?)',(result,))
        conn.commit()
        conn.close()
    return render_template('index.html')

### route to register new users to database
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        ## get user name from register form
        user = request.form['user']
        ## get image content from registered form
        content = request.form['content']
        response = urllib.request.urlopen(content)
        inimage = cv2.imdecode(np.fromstring(response.file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        ## get cropped face
        newface = crop_face_register(inimage)
        ## if face detected
        if newface != "No faces found":
            if not user:
                flash('name is required!')
            else:
                ## encode cropped face as base64 string
                image_content = cv2.imencode('.jpg', newface)[1].tostring()
                encoded_image = base64.encodestring(image_content)
                to_send = 'data:image/jpg;base64,' + str(encoded_image, 'utf-8')
                conn = get_db_connection()
                ## register new user name and encoded face to database
                conn.execute('INSERT INTO users (user, content) VALUES (?, ?)',(user, to_send))
                conn.commit()
                conn.close()
                flash_msg = 'New user name - {} registerd sucessfully'.format(user)
                flash(flash_msg)
                return redirect(url_for('index'))
        else:
            flash_msg = 'No faces found for name - {}'.format(user)
            flash(flash_msg)
            return redirect(url_for('index'))
    return render_template('create.html')

if __name__ == '__main__':
	app.run(debug=False)