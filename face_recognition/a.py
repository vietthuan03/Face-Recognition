import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db as firebase_db

# Initialize Firebase Admin SDK (replace with your credentials)
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://faceattendance-4a806-default-rtdb.firebaseio.com/',
    'storageBucket': 'https://faceattendance-4a806-default-rtdb.firebaseio.com/'
})


folder_path = 'Images'  # Replace with your folder path


# Function to list all filenames in the folder and handle errors
def get_filenames(folder_path):
    try:
        filenames = os.listdir(folder_path)
        if filenames is None:
            raise ValueError("The folder path is valid but contains no files.")
        return filenames
    except FileNotFoundError:
        raise FileNotFoundError(f"Folder path '{folder_path}' not found.")
    except Exception as e:
        raise Exception(f"An error occurred while listing files: {e}")


# Function to sanitize the filename to be Firebase-compatible
def sanitize_filename(filename):
    return filename.replace('.', '_')  # Replace "." with "_"


# Get list of filenames and handle potential errors
try:
    filenames = get_filenames(folder_path)
except Exception as e:
    print(e)
    filenames = []

# Iterate through each filename and retrieve studentInfo from Firebase
for filename in filenames:
    sanitized_filename = sanitize_filename(filename)
    ref_path = f"Images/{sanitized_filename}"

    try:
        student_info = firebase_db.reference(ref_path).get()
        if student_info:
            print(f"Student info for {filename}: {student_info}")
        else:
            print(f"No student info found for {filename}")
    except Exception as e:
        print(f"An error occurred while retrieving data for {filename}: {e}")
