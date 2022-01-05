# Key aggregator
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os.path
import pwd

# check whether the current system is development.
currUser = pwd.getpwuid(os.getuid()).pw_name
if currUser == "markwong":
    # use development credentials
    cred = firebase_admin.credentials.Certificate('../serviceAccountD.json')
else:
    # use production credentials
    cred = firebase_admin.credentials.Certificate('../serviceAccountP.json')
    
firebase_admin.initialize_app(cred)
db = firestore.client()
file = "keys.txt"
if not os.path.exists(file): 
    print("File does not exist")

def addKey(gameSplit):
    gameTitle = gameSplit[0]
    key = gameSplit[1]
    # key_doc = db.collection(uppercaseGameTitle).document(key)
    key_doc = db.collection("game_list").document(gameTitle).collection("keys").document(key)
    doc = key_doc.get()
    if not doc.exists:
        # add key
        key_doc.set({
            "key" : key,
            "user" : "JimRPG"
        })
        db.collection("game_list").document(f'{gameTitle}').set({"exists" : 1})

def addGames():
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

addGames()

