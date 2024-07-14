import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Initialize the Firebase app
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://faceattendance-4a806-default-rtdb.firebaseio.com/'
})

# Reference to the 'Students/' path in the database
ref = db.reference('Students/')

# Data to be added
data = {
    "Vo Dung": {
        "name": "Vo Dung",
        "major": "Software",
        "starting_year": 2021,
        "total_attendance": 0,
        "standing": "G",
        "year": 4,
        "last_attendance_time": "2022-12-11 00:54:34"
    },
    "Viet Thuan": {
        "name": "Viet Thuan",
        "major": "Software",
        "starting_year": 2021,
        "total_attendance": 7,
        "standing": "G",
        "year": 4,
        "last_attendance_time": "2022-12-11 00:54:34"
    },
    "Emily Blunt": {
        "name": "Emily Blunt",
        "major": "Economics",
        "starting_year": 2021,
        "total_attendance": 12,
        "standing": "B",
        "year": 1,
        "last_attendance_time": "2022-12-11 00:54:34"
    },
    "Elon Musk": {
        "name": "Elon Musk",
        "major": "Physics",
        "starting_year": 2020,
        "total_attendance": 7,
        "standing": "G",
        "year": 2,
        "last_attendance_time": "2022-12-11 00:54:34"
    }
}

# Push data to Firebase with automatic unique IDs
# for value in data.values():
#     new_ref = ref.push()
#     new_ref.set(value)
for key, value in data.items():
    ref.child(key).set(value)

print("Data added successfully with auto-generated IDs.")
