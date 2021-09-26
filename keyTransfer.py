# Key aggregator
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os.path

firebaseConfig = {
  "apiKey": "AIzaSyAY7VjY4T1wphjziRQATkzniJRk255W9CA",
  "authDomain": "steamkeys-discord.firebaseapp.com",
  "databaseURL": "https://portfolio-e79d0.firebaseio.com",
  "projectId": "steamkeys-discord",
  "storageBucket": "steamkeys-discord.appspot.com",
  "messagingSenderId": "689124544209",
  "appId": "1:689124544209:web:b045d6cbe27699d20d3ff0",
  "measurementId": "G-X3THVYCFSP",
  "serviceAccount": "serviceAccount.json"
};

cred = firebase_admin.credentials.Certificate('serviceAccount.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
file = "keys.txt"
if not os.path.exists(file): 
    print("File does not exist")

def addKey(gameSplit):
    uppercaseGameTitle = gameSplit[0].upper()
    key = gameSplit[1]

    key_doc = db.collection(uppercaseGameTitle).document(key)
    doc = key_doc.get()
    if not doc.exists:
        # add key
        key_doc.set({
            "key" : key,
            "user" : "JimRPG"
        })
        db.collection("game_list").document(f'{uppercaseGameTitle}').set({"exists" : 1})
    pass

with open(file, 'r') as fp:
    while True:
        game = fp.readline()
        if game:
            gameSplit = game.split("|")
            print(gameSplit[0])
            addKey(gameSplit)
        else:
            print("EOF")
            break
    


