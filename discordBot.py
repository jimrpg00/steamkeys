import os
import re
import logging

import discord
from discord.ext import commands
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
import time

TOKEN = 'ODgxNTM2OTY5Mzc5ODQwMTEw.YSuRRw.WfJMItxoL0lcKxRv7jAedcwv604'
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
modRole = 'Moderator'

initial_extensions = []

client = commands.Bot(command_prefix='!')
cred = firebase_admin.credentials.Certificate('serviceAccount.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
client.firestoreDB = db

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        initial_extensions.append("cogs." + filename[:-3]) # -3 removes the extension

for extension in initial_extensions:
    client.load_extension(extension)   



    



# before = datetime.datetime.now()
# before.replace(tzinfo=None)
# time.sleep(1)
# after = datetime.datetime.now()
# after.replace(tzinfo=None)
# print(abs(after-before))

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    await client.process_commands(message)
    
    if message.author == client.user:
        return

#     if message.content.startswith('!help'):
        
#         await message.channel.send(helpText)
        
    #
    # list all games with valid keys
    #
    # if message.content.startswith('!listgames'):
    #     doc_refs = db.collection('game_list').stream()
    #     appendedGamesStr = ""

    #     for doc in doc_refs:
    #         # format game title
    #         # gameTitle = re.split("\[\w+\]", doc.id)
    #         # gameDistinctions = re.split("\[\w+\]", doc.id)
    #         # print(gameTitle)
    #         formattedTitle = doc.id.capitalize()
    #         appendedGamesStr = appendedGamesStr + (f'{formattedTitle}\n')

    #     await message.channel.send("Listing the steam key depository..")
    #     await message.channel.send(appendedGamesStr)

    #
    # show my keys
    #
    # if message.content.startswith('!listmygames'):
    #     await message.author.send("One moment, grabbing a list of games.")
    #     keys_refs = db.collection('user').document(str(message.author.id)).collection('keys').stream()
    #     appendedGamesStr = ""
    #     for game in keys_refs:
    #         appendedGamesStr = appendedGamesStr + (f'{game.id}\n')
    #     await message.channel.send(appendedGamesStr)

    #
    # reserve key for user
    #
    # if message.content.startswith('!requestkey'):
        # commandArr = message.content.split(' ')
        # commandArr.pop(0)
        # gameTitle = ' '.join(commandArr)
        # uppercaseGameTitle = gameTitle.upper()
        # availableKey_docs = db.collection(uppercaseGameTitle).limit(1).stream()

        # if len(list(availableKey_docs)) != 0:
        #     availableKey_docs = db.collection(uppercaseGameTitle).limit(1).stream()
        #     gameKey = list(availableKey_docs)[0].id
            
        #     # User checks
        #     userGame_refs = db.collection('user').document(str(message.author.id)).collection(f'{uppercaseGameTitle}').stream()
        #     numberOfKeys = len(list(userGame_refs))

        #     # get user date fields
        #     user_doc = db.collection('user').document(str(message.author.id))
        #     doc_fields = user_doc.get()
        #     if "date" in doc_fields.to_dict():
        #         prevDateNoTz = doc_fields.to_dict()["date"].replace(tzinfo=None)
        #         currDate = datetime.datetime.now().replace(tzinfo=None)
        #         dailyLimit = (abs(currDate - prevDateNoTz).days)
        #         if dailyLimit >= 1:
        #             user_doc.update({
        #                 "date" : datetime.datetime.now().replace(tzinfo=None)
        #             })
        #         else:
        #             await message.author.send(f'You have reached your daily limit of 1 key per day.')
        #             return
        #     else:
        #         user_doc.update({
        #             "date" : datetime.datetime.now().replace(tzinfo=None)
        #         })
            
        #     # a limit of 5 keys per game is allowed, this includes other members of the family
        #     if numberOfKeys < 5:
        #         # add key to user list
        #         db.collection('user').document(str(message.author.id)).update({
        #             "name" : message.author.name,
        #             "rating" : firestore.Increment(1) # INCREMENT RATING
        #         })
                
        #         user_refs = db.collection('user').document(str(message.author.id)).collection(f'{gameTitle}').document(f'{gameKey}')
        #         user_refs.set({
        #             "key" : gameKey
        #         })
        #         logging.info(f'{gameKey} successfully added to {message.author.id}')

        #         db.collection(uppercaseGameTitle).document(f'{gameKey}').delete()
        #         logging.info(f'{gameKey} successfully deleted')
        #         await message.channel.send(f'Congrats {message.author.name}, check your DM for the key!')
        #         await message.author.send(f'Your game key for {gameTitle} is {gameKey}. Enjoy!')
        #     else:
        #         await message.author.send(f'To keep the community fair, a limit of 5 keys is applied per user. This allows other users in the community have a fair chance of enjoying the game.')
        # else:
        #     await message.channel.send(f'Hello, unfortunately there are no keys available for {gameTitle}.')

    #
    # add key to game list
    #
    # if message.content.startswith('!addkey'):
        
        # #regex to check the format
        # argList = message.content.split(' ')
        # # save and remove the command from argList
        # command = argList.pop(0)

        # key = argList.pop(-1) # check if key is correct length
        # # argList should be stripped down without the command and key
        # match = re.search("([a-zA-Z0-9]){3,}-{1}", key) #matches AAAAA-12345-C3A3F, most keys are expected to have this format
        # if not match:
        #     await message.channel.send(f"The format for the cd-key is incorrect. You entered {key}. Please try using the command again, here's an example - _!addkey Battlefield V AAAAA-BBBBB-CCCCC_.")
        #     return 

        # gameTitle = ' '.join(argList)

        # uppercaseGameTitle = gameTitle.upper()

        # key_doc = db.collection(uppercaseGameTitle).document(key)
        # doc = key_doc.get()
        # if not doc.exists:
        #     # add key
        #     key_doc.set({
        #         "key" : key,
        #         "user" : message.author.name
        #     })

        #     # add key to user's profile
        #     user_doc = db.collection("user").document(f"{message.author.id}").collection(uppercaseGameTitle).document(key)
        #     user_doc.set({
        #         "key" : key,
        #         "user" : message.author.name,
        #     })

        #     # add key to game list
        #     db.collection("game_list").document(f'{uppercaseGameTitle}').set({"exists" : 1})


        #     output = f"Thanks for giving back to the community {message.author.name}. {gameTitle} key was received for another."
        #     await message.channel.send(output)
        # else:   
        #     output = f"The key already exists. Please remember to only use valid keys. You may try again and add unique key."
        #     await message.channel.send(output)
        # await message.delete()

    #
    # ADMIN COMMANDS
    #

    #
    # remove key for game. use when an invalid key is found
    #
    if message.content.startswith('!_removegamekey'):
        if modRole in role_names:
            await message.author.send('Moderator user now removing key')
            print("removing")

    #
    # remove key for user
    #
    if message.content.startswith('!_removeuserkey'):
        if modRole in role_names:
            await message.author.send('Moderator user now removing user key')

    #
    #
    #
    if message.content.startswith('!_testdm'):
        await message.author.send("this is a dm with your key")

    #
    #
    #
    if message.content.startswith('!_myDetails'):
        userRole = message.author.roles
        userId = message.author.id
        userName = message.author.name
        userRating = db.collection('user').document(str(message.author.id)).get().to_dict()["rating"]
        await message.author.send(f'role(s): {userRole}\nid: {userId}\nusername: {userName}\nrating: {userRating}')
    
    #
    # admin
    #
    if message.content.startswith('!_getUserDetails'):
        commandArr = message.content.split(' ')
        userRole = message.author.roles
        userId = message.author.id
        userName = message.author.name
        userRating = db.collection('user').document(str(commandArr[1])).get().to_dict()["rating"]
        await message.author.send(f'role(s): {userRole}\nid: {userId}\nusername: {userName}\nrating: {userRating}')

@client.command(brief="lottery")
async def lottery(ctx):
    """Randomly selects a key
    """
    pass

@client.command(brief="requestkey")
async def requestkey(ctx):
    commandArr = message.content.split(' ')
    commandArr.pop(0)
    gameTitle = ' '.join(commandArr)
    uppercaseGameTitle = gameTitle.upper()
    availableKey_docs = db.collection(uppercaseGameTitle).limit(1).stream()

    if len(list(availableKey_docs)) != 0:
        availableKey_docs = db.collection(uppercaseGameTitle).limit(1).stream()
        gameKey = list(availableKey_docs)[0].id
        
        # User checks
        userGame_refs = db.collection('user').document(str(message.author.id)).collection(f'{uppercaseGameTitle}').stream()
        numberOfKeys = len(list(userGame_refs))

        # get user date fields
        user_doc = db.collection('user').document(str(message.author.id))
        doc_fields = user_doc.get()
        if "date" in doc_fields.to_dict():
            prevDateNoTz = doc_fields.to_dict()["date"].replace(tzinfo=None)
            currDate = datetime.datetime.now().replace(tzinfo=None)
            dailyLimit = (abs(currDate - prevDateNoTz).days)
            if dailyLimit >= 1:
                user_doc.update({
                    "date" : datetime.datetime.now().replace(tzinfo=None)
                })
            else:
                await message.author.send(f'You have reached your daily limit of 1 key per day.')
                return
        else:
            user_doc.update({
                "date" : datetime.datetime.now().replace(tzinfo=None)
            })
        
        # a limit of 5 keys per game is allowed, this includes other members of the family
        if numberOfKeys < 5:
            # add key to user list
            db.collection('user').document(str(message.author.id)).update({
                "name" : message.author.name,
                "rating" : firestore.Increment(1) # INCREMENT RATING
            })
            
            user_refs = db.collection('user').document(str(message.author.id)).collection(f'{gameTitle}').document(f'{gameKey}')
            user_refs.set({
                "key" : gameKey
            })
            logging.info(f'{gameKey} successfully added to {message.author.id}')

            db.collection(uppercaseGameTitle).document(f'{gameKey}').delete()
            logging.info(f'{gameKey} successfully deleted')
            await message.channel.send(f'Congrats {message.author.name}, check your DM for the key!')
            await message.author.send(f'Your game key for {gameTitle} is {gameKey}. Enjoy!')
        else:
            await message.author.send(f'To keep the community fair, a limit of 5 keys is applied per user. This allows other users in the community have a fair chance of enjoying the game.')
    else:
        await message.channel.send(f'Hello, unfortunately there are no keys available for {gameTitle}.')

@client.command(brief="Add key")
async def addgame(ctx):
            
        #regex to check the format
        argList = ctx.content.split(' ')
        # save and remove the command from argList
        command = argList.pop(0)

        key = argList.pop(-1) # check if key is correct length
        # argList should be stripped down without the command and key
        match = re.search("([a-zA-Z0-9]){3,}-{1}", key) #matches AAAAA-12345-C3A3F, most keys are expected to have this format
        if not match:
            await ctx.channel.send(f"The format for the cd-key is incorrect. You entered {key}. Please try using the command again, here's an example - _!addkey Battlefield V AAAAA-BBBBB-CCCCC_.")
            return 

        gameTitle = ' '.join(argList)

        uppercaseGameTitle = gameTitle.upper()

        key_doc = db.collection(uppercaseGameTitle).document(key)
        doc = key_doc.get()
        if not doc.exists:
            # add key
            key_doc.set({
                "key" : key,
                "user" : ctx.author.name
            })

            # add key to user's profile
            user_doc = db.collection("user").document(f"{ctx.author.id}").collection(uppercaseGameTitle).document(key)
            user_doc.set({
                "key" : key,
                "user" : ctx.author.name,
            })

            # add key to game list
            db.collection("game_list").document(f'{uppercaseGameTitle}').set({"exists" : 1})


            output = f"Thanks for giving back to the community {ctx.author.name}. {gameTitle} key was received for another."
            await ctx.channel.send(output)
        else:   
            output = f"The key already exists. Please remember to only use valid keys. You may try again and add unique key."
            await ctx.channel.send(output)
        await ctx.delete()

@client.command(brief="Lists available games with valid keys")
async def listgames(ctx):
    doc_refs = db.collection('game_list').stream()
    appendedGamesStr = ""

    for doc in doc_refs:
        # format game title
        # gameTitle = re.split("\[\w+\]", doc.id)
        # gameDistinctions = re.split("\[\w+\]", doc.id)
        # print(gameTitle)
        formattedTitle = doc.id.capitalize()
        appendedGamesStr = appendedGamesStr + (f'{formattedTitle}\n')
    await ctx.channel.send("Listing the steam key depository..")
    await ctx.channel.send(appendedGamesStr)

@client.command(brief="lists games you have already acquired")
async def listmygames(ctx):
    await ctx.author.send("One moment, grabbing a list of games.")
    keys_refs = db.collection('user').document(str(ctx.author.id)).collection('keys').stream()
    appendedGamesStr = ""
    for game in keys_refs:
        appendedGamesStr = appendedGamesStr + (f'{game.id}\n')
    await ctx.channel.send(appendedGamesStr)

@client.command(brief='This is the brief description', description='This is the full description')
async def info(ctx):
    helpText = """**Welcome to the JimRPG Steam Key Depository**
This area is where Discord members can add/take PC CD keys (games only, no DLC). Please enjoy the games for personal use. They are not for resale as these are member donations. There is a limit of 1 key per person a day.

**1. Commands**
!help - this help message 
!listgames - lists available games with valid keys 
!listmygames - lists games you have already acquired 
!addkey “Game Name” “CD Key”– add a key into the database for others (use DM)
!requestkey “game name” - grants a free and valid key

**2. Adding CD keys**
When adding keys, create a DM so the key is not revealed in the thread. (direct message SteamKeysBot by right clicking on the name in the member list).

The command to use is –
!addkey “Game Name” “CD Key”
e.g. !addkey Battlefield V AAAAA-BBBBB-CCCCC

**2.1 Platform Differentiation**
Please add a platform (with square brackets) if it is something other than Steam. For Steam, leave empty.
e.g. !addkey Battlefield V [Origin] AAAA-BBBB-CCCC-DDDD-EEEE

**Platforms:**
EA Origin – Origin
Ubisoft Uplay – Uplay
Epic Games – Epic
GOG – GOG
Rockstar – Rockstar
Others – label as needed

**2.2 Region Differentiation**
Please add a region (with square brackets) if you know the key is for a specific region. If its region free, leave empty.
e.g. !addkey Battlefield V [Origin] [AS] AAAA-BBBB-CCCC-DDDD-EEEE
(This is a Battlefield V key for Origin in the Asia region)
or
e.g. !addkey Red Dead Redemption 2 [ROW ex. Japan] AAAAA-BBBBB-CCCCC
(This is a RDR2 key for Steam for rest of world except Japan)

**Regions:**
US: US
Europe: EU
AS: Asia
ME: Middle East
ROW: Rest of World
ex. = except

**3. Taking CD Keys**
When taking keys, request the key in the thread. SteamKeysBot will direct message you the key.

The command to use is –
!requestkey “Game Name”
e.g. !requestkey Battlefield V [Origin] [EU]

**4. Invalid Keys**
Report any invalid keys and user that added it, we may contact them to fix any issues. Do not add back in DB.
"""
    await ctx.send(helpText)

client.run(TOKEN)