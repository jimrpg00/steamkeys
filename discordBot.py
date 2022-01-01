import os
import pwd
from MyHelp import MyHelp
import discord
from discord.ext import commands
import firebase_admin
from firebase_admin import firestore


# discord bot token


modRole = 'Moderator'

# check user for dev or prod region
currUser = pwd.getpwuid(os.getuid()).pw_name

initial_extensions = []

intents = discord.Intents.default()
intents.members = True

# initialist bot
client = commands.Bot(command_prefix='!',help_command=None)
client._BotBase__cogs  = commands.core._CaseInsensitiveDict()
if currUser == "markwong":
    # test server 
    TOKEN = 'ODgxNTM2OTY5Mzc5ODQwMTEw.YSuRRw.WfJMItxoL0lcKxRv7jAedcwv604' #discord bot token
    cred = firebase_admin.credentials.Certificate('serviceAccountD.json')
    client.staticChannel = 880273688052772874
    client.staticChannelStr = "steam-keys"
else:
    # live prod server - JimRpg
    TOKEN = 'ODk3ODIyOTY3Mjk0MTk3ODEw.YWbQzA.bixdf6IS_ZOdksHsI8MgbRRmksE' #discord bot token
    cred = firebase_admin.credentials.Certificate('serviceAccountP.json')
    client.staticChannel = 898977014139199568
    client.staticChannelStr = "🔑-steam-keys"
firebase_admin.initialize_app(cred)
db = firestore.client()
client.firestoreDb = db

# client.help_command = MyHelp()
client.remove_command('help')


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print('Bot is now live')

@client.event
async def on_message(message):
    await client.process_commands(message)  
    if message.author == client.user:
        return

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

# @client.command(brief="lottery")
# async def lottery(ctx):
#     """Randomly selects a key
#     """
#     pass


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        initial_extensions.append("cogs." + filename[:-3]) # -3 removes the extension

for extension in initial_extensions:
    client.load_extension(extension)

client.run(TOKEN)
