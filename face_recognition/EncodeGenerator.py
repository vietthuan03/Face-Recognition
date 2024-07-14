import cv2
import os
import face_recognition
import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

def findEncodings(folderPath):
    pathList = os.listdir(folderPath)
    print("Images found: ", pathList)
    imgList = []
    studentNames = []

    # Read images and extract student Names
    for path in pathList:
        imgList.append(cv2.imread(os.path.join(folderPath, path)))
        studentNames.append(os.path.splitext(path)[0])

        fileName = f'{folderPath}/{path}'
        bucket = storage.bucket()
        blob = bucket.blob(fileName)
        blob.upload_from_filename(fileName)

    print("Student Names: ", studentNames)

    def encodeImages(imagesList):
        encodeList = []
        for img in imagesList:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(img)
            if encodings:
                encode = encodings[0]
                encodeList.append(encode)
                print("Encoding for an image:", encode)
            else:
                print("No face found in image")
        return encodeList

    print("Encoding Started ...")
    encodeListKnown = encodeImages(imgList)
    encodeListKnownWithNames = [encodeListKnown, studentNames]
    print("Encoding Complete")

    # Save the encodings and IDs to a file
    with open("EncodeFile.p", 'wb') as file:
        pickle.dump(encodeListKnownWithNames, file)
    print("File Saved")


# Call the function with the path to the folder containing images
# findEncodings('dataset')