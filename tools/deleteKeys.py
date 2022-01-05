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

def delete_in_batch():
    print('Deleting documents in batch')
    doc_refs = db.collection('game_list').stream()
    batch = db.batch()
    appendedGamesStr = ""

    for doc in doc_refs:
        batch.delete(doc.reference)
    batch.commit()

# comment/uncomment this line to wipe everything in the database on firebase
delete_in_batch()