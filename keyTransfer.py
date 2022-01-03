# Key aggregator
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os.path
import pwd

currUser = pwd.getpwuid(os.getuid()).pw_name
if currUser == "markwong":
    cred = firebase_admin.credentials.Certificate('serviceAccountD.json')
else:
    cred = firebase_admin.credentials.Certificate('serviceAccountP.json')
    
firebase_admin.initialize_app(cred)
db = firestore.client()
file = "keys.txt"
if not os.path.exists(file): 
    print("File does not exist")

def addKey(gameSplit):
    gameTitle = gameSplit[0] + " Steam" + " ROW"
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

def delete_in_batch():
    print('Deleting documents in batch')
    # now = time()
    # docs = db.collection(u'users').where(u'expires_at', u'<=', int(now)).stream()
    # batch = db.batch()
    # counter = 0
    # for doc in docs:
    #     counter = counter + 1
    #     if counter % 500 == 0:
    #         batch.commit()
    #     batch.delete(doc.reference)
    # batch.commit()

    doc_refs = db.collection('game_list').stream()
    batch = db.batch()
    appendedGamesStr = ""

    for doc in doc_refs:
        batch.delete(doc.reference)
    batch.commit()

# use this to add keys as the base set of keys
addGames()

# uncomment this line to wipe everything
# delete_in_batch()