import time
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import os
import pickle
import cvzone
import cv2
import face_recognition
import firebase_admin
import pandas as pd
from firebase_admin import credentials, db, storage
from datetime import datetime
import numpy as np
from firebase_admin import db as firebase_db
from EncodeGenerator import findEncodings

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://faceattendance-4a806-default-rtdb.firebaseio.com/',
    'storageBucket': 'faceattendance-4a806.appspot.com'
})
bucket = storage.bucket()

# Create Images directory if it doesn't exist
if not os.path.exists('Images'):
    os.makedirs('Images')
# Load user information from CSV file
# if os.path.exists('users.csv'):
#     users_df = pd.read_csv('users.csv')
# else:
#     users_df = pd.DataFrame(
#         columns=['ID', 'Name', 'Major', 'Starting Year', 'Year'])
folder_path = 'Images'
filenames = os.listdir(folder_path)
# root
root = tk.Tk()
# Function to capture images

# Lấy thời gian hiện tại
current_time = datetime.now()

# Định dạng thời gian thành chuỗi
formatted_time = current_time.strftime("%m-%d")

def capture_images(ID):
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        messagebox.showerror("Error", "Cannot open camera")
        return

    img_counter = 0
    root.withdraw()
    capture_window = tk.Toplevel(root)
    capture_window.title("Capture Face")
    capture_window.configure(bg='#f0f0f0')

    lmain = tk.Label(capture_window)
    lmain.pack()

    def show_frame():
        ret, frame = cam.read()
        if ret:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(10, show_frame)

    def capture_image(event):
        nonlocal img_counter
        ret, frame = cam.read()
        if ret:
            resized_frame = cv2.resize(frame, (216, 216))
            # Save the image locally
            img_name = f"Images/{ID}.png"
            cv2.imwrite(img_name, resized_frame)
            print(f"{img_name} được lưu!")

            # Upload the image to Firebase Storage
            # blob = bucket.blob(f'Images/{ID}.png')
            # blob.upload_from_filename(img_name)
            # print(f"Image uploaded to Firebase Storage as {ID}.png")
            img_counter += 1
            if img_counter >= 1:
                cam.release()
                capture_window.destroy()
                messagebox.showinfo("Thành công", "Chụp ảnh thành công!")
                root.deiconify()
    messagebox.showinfo("Lưu ý", "Nhấn space để chụp hình")
    capture_window.bind('<space>', capture_image)
    show_frame()


# Function to save user information
def save_user_info():
    ID = ID_entry.get()
    name = name_entry.get()
    major = major_entry.get()
    starting_year = starting_year_entry.get()
    year = year_entry.get()

    if not all([ID, name, major, starting_year, year]):
        messagebox.showerror("Error", "Please fill in all fields")
        return

    # Save user information to Firebase
    ref = db.reference('Students/')
    data = {
        ID: {
            "ID": ID,
            "name": name,
            "major": major,
            "starting_year": int(starting_year),
            "year": int(year),
        }
    }
    for key, value in data.items():
        ref.child(key).set(value)
    # Save user information to CSV for local backup
    # user_id = len(users_df) + 1
    # users_df.loc[user_id] = [ID, name, major, starting_year, year]

    # users_df.to_csv('users.csv', index=False)
    user_info_window.destroy()
    root.deiconify()

    capture_images(ID)
# def center_window(window, width, height):
#     screen_width = window.winfo_screenwidth()
#     screen_height = window.winfo_screenheight()
#     x = (screen_width // 2) - (width // 2)
#     y = (screen_height // 2) - (height // 2)
#     window.geometry(f'{width}x{height}+{x}+{y}')
# Function to show user information entry window
def show_user_info_window():
    global ID_entry, name_entry, major_entry, starting_year_entry, year_entry, user_info_window

    root.withdraw()
    user_info_window = tk.Toplevel(root)
    user_info_window.title("Enter User Information")

    # Define window size
    window_width = 800
    window_height = 600

    # Center the window
    screen_width = user_info_window.winfo_screenwidth()
    screen_height = user_info_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    user_info_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    # Add background image
    background_image = Image.open("Background\\nen.jpg")  # Replace with the path to your background image
    background_image = background_image.resize((window_width, window_height), Image.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)

    background_label = tk.Label(user_info_window, image=background_photo)
    background_label.place(relwidth=1, relheight=1)

    # Create a frame and place it in the center of the window
    form_frame = ttk.Frame(user_info_window, padding="20 20 20 20", style='Card.TFrame')
    form_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Ensure labels and entries have a transparent background
    style = ttk.Style()
    style.configure('TLabel', background='#ffffff')
    style.configure('TEntry', background='#ffffff')

    # Add form fields to the frame
    ttk.Label(form_frame, text="ID").grid(row=0, column=0, sticky=tk.W, pady=10)
    ID_entry = ttk.Entry(form_frame, width=30)
    ID_entry.grid(row=0, column=1, pady=10)

    ttk.Label(form_frame, text="Name").grid(row=1, column=0, sticky=tk.W, pady=10)
    name_entry = ttk.Entry(form_frame, width=30)
    name_entry.grid(row=1, column=1, pady=10)

    ttk.Label(form_frame, text="Major").grid(row=2, column=0, sticky=tk.W, pady=10)
    major_entry = ttk.Entry(form_frame, width=30)
    major_entry.grid(row=2, column=1, pady=10)

    ttk.Label(form_frame, text="Starting Year").grid(row=3, column=0, sticky=tk.W, pady=10)
    starting_year_entry = ttk.Entry(form_frame, width=30)
    starting_year_entry.grid(row=3, column=1, pady=10)

    ttk.Label(form_frame, text="Year").grid(row=4, column=0, sticky=tk.W, pady=10)
    year_entry = ttk.Entry(form_frame, width=30)
    year_entry.grid(row=4, column=1, pady=10)

    # Add buttons to the frame
    back_button = ttk.Button(form_frame, text="Return", command=main_screen)
    back_button.grid(row=5, column=0, pady=15, padx=(0, 5))

    save_button = ttk.Button(form_frame, text="Save", command=save_user_info)
    save_button.grid(row=5, column=1, pady=15, padx=(5, 0))

    # Keep a reference to the background image to prevent it from being garbage collected
    background_label.image = background_photo

    user_info_window.mainloop()
def run_face_recognition():
    # Load the encoding data and ID of student
    print("Loading Encode File ...")
    # Mở tệp 'EncodeFile.p' trong chế độ đọc nhị ph ân ('rb'). read binarry
    file = open('EncodeFile.p', 'rb')
    encodeListKnownWithIds = pickle.load(file)
    file.close()
    encodeListKnown, studentIds = encodeListKnownWithIds
    # print(studentNames)
    print("Encode File Loaded")

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    imgBackground = cv2.imread('Resources/background.png')
    # Importing the mode images into a list
    folderModePath = 'Resources/Modes'
    modePathList = os.listdir(folderModePath)
    imgModeList = []
    # print(modePathList)
    img_counter = 0

    for path in modePathList:
        imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
    # print(len(imgModeList))

    modeType = 0
    counter = 0
    ID = -1
    imgStudent = []
    # Hiển thị thông báo
    messagebox.showinfo("Gợi ý", "Gõ q để thoát!")
    max_iterations = 100
    # for _ in range(max_iterations):
    while True:
        success, img = cap.read()
        if not success:
            break

        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        faceCurFrame = face_recognition.face_locations(imgS) # sử dụng CNN để phát hiện các vị trí khuôn mặt trong ảnh. thu nhỏ xuống 25%(0,25 so vs ban đầu)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)# CNN  tạo ra các mã hóa (encoding) của khuôn mặt dựa trên các mô hình mạng nơ-ron sâu. Các mã hóa này là các vector 128 chiều đại diện cho các đặc trưng của khuôn mặt.
        imgBackground[162:162 + 480, 55:55 + 640] = img
        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

        if faceCurFrame:
            for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace) # sử dụng thuật toán so sánh khuôn mặt bằng cách tính toán khoảng cách Euclidean giữa các vector mã hóa. Nếu khoảng cách nhỏ hơn một ngưỡng xác định, hai khuôn mặt được coi là trùng khớp.
                face_distances = face_recognition. face_distance(encodeListKnown, encodeFace)
                print("Matches: ", matches)
                print("face: ", face_distances)
                if face_distances.size > 0:
                    matchIndex = np.argmin(face_distances)

                    print("Match Index", matchIndex) # tìm chỉ số của mã hóa khuôn mặt đã biết có khoảng cách nhỏ nhất với mã hóa khuôn mặt hiện tại, tương đương với thuật toán KNN tìm điểm gần nhất.

                    if matches[matchIndex]:
                        # print("Known Face Detected")
                        # print(studentIds[matchIndex])
                        y1, x2, y2, x1 = faceLoc
                        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                        bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                        imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=1)
                        id = studentIds[matchIndex]
                        # print(id)
                        if counter == 0:
                            cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                            cv2.imshow("Face Attendance", imgBackground)
                            cv2.waitKey(1)
                            counter = 1
                            modeType = 1

            if counter != 0:
                if counter == 1:
                    # Retrieve student information from the Firebase database
                    studentInfo = db.reference(f'Students/{id}').get()
                    print(studentInfo)

                    # Get the student image from Firebase storage
                    blob = bucket.get_blob(f'Images/{id}.png')
                    array = np.frombuffer(blob.download_as_string(), np.uint8)
                    imgStudent = cv2.imdecode(array, cv2.IMREAD_COLOR)

                    # Resize imgStudent to fit into the destination area (216x216)
                    imgStudent = cv2.resize(imgStudent, (216, 216))

                if modeType != 3:
                    if 5 < counter < 10:
                        modeType = 2
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                    if counter <= 5:
                        # Display student information
                        cv2.putText(imgBackground, str(formatted_time), (861, 125),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

                        cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(imgBackground, str(id), (1006, 493),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                        offset = (414 - w) // 2
                        cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)
                        imgBackground[175:175 + 216, 909:909 + 216] = imgStudent
                        # cv2.imshow("Face Attendance", imgBackground)
                        # cv2.waitKey(1)
                        # time.sleep(10)
                    counter += 1

                    if counter >= 10:
                        counter = 0
                        modeType = 0
                        studentInfo = []
                        imgStudent = []
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                # elif modeType==3:
                #     modeType = 3
                #     counter = 0
                #     imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

        else:
            modeType = 0
            counter = 0

        cv2.imshow("Face Attendance", imgBackground)
        # Check for window close event
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    cap.release()
# Function to be called by the button
def train_model():
    folder_path = 'Images'  # Specify your Images folder path
    if not os.path.exists(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return
    findEncodings(folder_path)

def main_screen():

    # Initialize the main application window

    root.title("Face Recognition System")
    root.geometry("1200x710")  # Minimal size to see the root window
    root.configure(bg='#f0f0f0')
    # Add background image
    background_image = Image.open("Background\\nen.jpg")  # Replace with the path to your background image
    background_image = background_image.resize((1200, 710), Image.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)

    background_label = tk.Label(root, image=background_photo)
    background_label.place(relwidth=1, relheight=1)

    style = ttk.Style()
    style.configure('TButton', font=('Helvetica', 12), padding=10)

    # Add color to buttons
    style.configure('Enter.TButton', background='#4CAF50', foreground='blue')
    style.map('Enter.TButton', background=[('active', '#45a049')])
    style.configure('TLabel', font=('Helvetica', 12), padding=10)
    style.configure('Card.TFrame', background='#ffffff', borderwidth=1, relief='solid')

    style.configure('Train.TButton', background='#008CBA', foreground='green')
    style.map('Train.TButton', background=[('active', '#007bb5')])

    style.configure('Recognize.TButton', background='#f44336', foreground='red')
    style.map('Recognize.TButton', background=[('active', '#da190b')])

    # Create buttons with specified width and colors, directly on the root window
    enter_button = ttk.Button(root, text="Enter User Information", command=show_user_info_window, style='Enter.TButton')
    enter_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER, relwidth=0.2)

    train_button = ttk.Button(root, text="Train Model", command=train_model, style='Train.TButton')
    train_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.2)

    recognize_button = ttk.Button(root, text="Face Recognition", command=run_face_recognition,
                                  style='Recognize.TButton')
    recognize_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER, relwidth=0.2)
    root.deiconify()
    root.mainloop()
main_screen()