import logging
import datetime
import discord
from discord.ext import commands
from firebase_admin import firestore

class RequestKey(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db = self.client.firestoreDb
        self.keyLimit = 1

    @commands.command(brief="Grants a free and valid key")
    async def requestkey(self, ctx):
        commandArr = ctx.message.content.split(' ')
        commandArr.pop(0) # command - !requestkey
        gameTitle = ' '.join(commandArr)
        print(gameTitle)

        # uppercaseGameTitle = gameTitle.upper()

        availableKey_docs = self.db.collection("game_list").document(gameTitle).collection("keys").limit(1).stream()

        if len(list(availableKey_docs)) != 0:
            # need to redeclare because len() and list() destroys the availableKey_docs variable above

            availableKey_docs = self.db.collection("game_list").document(gameTitle).collection("keys").limit(1).stream()

            gameKey = list(availableKey_docs)[0].id
            
            # User checks
            user = self.db.collection("user").document(f"{ctx.author.id}").get()
            if user.exists:
                print("exists")
            else:
                print("does not")
                newUser = self.db.collection("user").document(f"{ctx.author.id}")
                newUser.set({
                    "name" : ctx.author.name,
                    "date" : datetime.datetime.now().replace(tzinfo=None),
                    "keyLimit" : 0
                })

            userGame_refs = self.db.collection('user').document(f"{ctx.author.id}").collection(f'{gameTitle}').stream()
            numberOfKeys = len(list(userGame_refs))
            
            # user_doc = self.db.collection("user").document(f"{ctx.author.id}").collection(gameTitle).document(key)
            # user_doc.set({
            #     "key" : key,
            #     "user" : ctx.author.name,
            # })

            # get user date fields
            user_doc = self.db.collection('user').document(str(ctx.author.id))
            doc_fields = user_doc.get()
            if "date" in doc_fields.to_dict():
                prevDateNoTz = doc_fields.to_dict()["date"].replace(tzinfo=None)
                if "keyLimit" not in doc_fields.to_dict():
                    user_doc.update({
                        "keyLimit" : 1
                    })
                # get updated user profile
                doc_fields = user_doc.get()
                currDate = datetime.datetime.now().replace(tzinfo=None)
                daySince = (abs(currDate - prevDateNoTz).days)
                userKeyLimit = doc_fields.to_dict()["keyLimit"]

                if daySince >= 1:
                    user_doc.update({
                        "keyLimit" : 0,                        
                })
                if daySince >= 1 or userKeyLimit < self.keyLimit:
                    
                    user_doc.update({
                        "keyLimit" : firestore.Increment(1), # INCREMENT RATING
                        "date" : datetime.datetime.now().replace(tzinfo=None)
                    })
                else:
                    await ctx.author.send(f'You have reached your daily limit of {self.keyLimit} keys per day.')
                    return
            else:
                user_doc.update({
                    "date" : datetime.datetime.now().replace(tzinfo=None)
                })
            
            # a limit of 5 keys per game
            if numberOfKeys < self.keyLimit:
                # add key to user list
                self.db.collection('user').document(str(ctx.author.id)).update({
                    "name" : ctx.author.name,
                    "rating" : firestore.Increment(1) # INCREMENT RATING
                })
                
                user_refs = self.db.collection('user').document(str(ctx.author.id)).collection(f'{gameTitle}').document(f'{gameKey}')
                user_refs.set({
                    "key" : gameKey
                })
                logging.info(f'{gameKey} successfully added to {ctx.author.id}')

                # turn back on
                self.db.collection("game_list").document(gameTitle).collection("keys").document(f'{gameKey}').delete()
                logging.info(f'{gameKey} successfully deleted and taken')
                await ctx.channel.send(f'Congrats {ctx.author.name}, check your DM for the key!')
                await ctx.author.send(f'Your game key for {gameTitle} is {gameKey}. Enjoy!')
            else:
                await ctx.author.send(f'To keep the community fair, a limit of 5 keys is applied per user. This allows other users in the community have a fair chance of enjoying the game.')
        else:
            await ctx.channel.send(f'Hello, unfortunately there are no keys available for {gameTitle}.')

def setup(client):
    client.add_cog(RequestKey(client))