import logging
import datetime
import discord
from discord.ext import commands

class RequestKey(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db = self.client.firestoreDb

    @commands.command(brief="Grants a free and valid key")
    async def requestkey(self, ctx):
        commandArr = ctx.content.split(' ')
        commandArr.pop(0)
        gameTitle = ' '.join(commandArr)
        uppercaseGameTitle = gameTitle.upper()
        availableKey_docs = self.db.collection(uppercaseGameTitle).limit(1).stream()

        if len(list(availableKey_docs)) != 0:
            availableKey_docs = self.db.collection(uppercaseGameTitle).limit(1).stream()
            gameKey = list(availableKey_docs)[0].id
            
            # User checks
            userGame_refs = self.db.collection('user').document(str(ctx.author.id)).collection(f'{uppercaseGameTitle}').stream()
            numberOfKeys = len(list(userGame_refs))

            # get user date fields
            user_doc = self.db.collection('user').document(str(ctx.author.id))
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
                    await ctx.author.send(f'You have reached your daily limit of 1 key per day.')
                    return
            else:
                user_doc.update({
                    "date" : datetime.datetime.now().replace(tzinfo=None)
                })
            
            # a limit of 5 keys per game is allowed, this includes other members of the family
            if numberOfKeys < 5:
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

                self.db.collection(uppercaseGameTitle).document(f'{gameKey}').delete()
                logging.info(f'{gameKey} successfully deleted')
                await ctx.channel.send(f'Congrats {ctx.author.name}, check your DM for the key!')
                await ctx.author.send(f'Your game key for {gameTitle} is {gameKey}. Enjoy!')
            else:
                await ctx.author.send(f'To keep the community fair, a limit of 5 keys is applied per user. This allows other users in the community have a fair chance of enjoying the game.')
        else:
            await ctx.channel.send(f'Hello, unfortunately there are no keys available for {gameTitle}.')

def setup(client):
    client.add_cog(RequestKey(client))