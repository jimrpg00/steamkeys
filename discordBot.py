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
if currUser == "markwong": # replace with your name or a new detection for your development machine
    # test server 
    TOKEN = 'ODgxNTM2OTY5Mzc5ODQwMTEw.YSuRRw.WfJMItxoL0lcKxRv7jAedcwv604' # discord bot token
    serviceJson = 'serviceAccountD.json'
    client.staticChannel = 880273688052772874
    client.staticChannelStr = "steam-keys"
else:
    # live prod server - JimRpg
    TOKEN = 'ODk3ODIyOTY3Mjk0MTk3ODEw.YWbQzA.bixdf6IS_ZOdksHsI8MgbRRmksE'
    serviceJson = 'serviceAccountP.json'
    client.staticChannel = 898977014139199568
    client.staticChannelStr = "🔑-steam-keys"

# initialise database
dbCred = firebase_admin.credentials.Certificate(serviceJson)
firebase_admin.initialize_app(dbCred)
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
