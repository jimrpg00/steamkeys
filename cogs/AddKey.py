import re
import discord
from discord.ext import commands

class AddKey(commands.Cog, description="When adding keys, create a DM so the key is not revealed in the thread. (direct message SteamKeysBot by right clicking on the name in the member list).\n\nThis command requires at mininmum the game title and game key. Platform and region are optional. Please keep in mind the ORDER of the arguments that follow the command -\n\n !addkey _title_ [_platform_] [_region_] _key_\n\nHere's an example with ALL arguments supplied -\n`!addkey Red Dead Redemption 2 [Rockstar] [ROW ex. Japan] AAAAA-BBBBB-CCCCC`\n\nAnother example with only region\n`!addkey Red Dead Redemption 2 [ROW ex. Japan] AAAAA-BBBBB-CCCCC`\n\nAnother example with only platform\n`!addkey Red Dead Redemption 2 [Rockstar] AAAAA-BBBBB-CCCCC`\n\nAnd finally another one with just the key and title\n`!addkey Red Dead Redemption 2 AAAAA-BBBBB-CCCCC`\n\nFor more information about regions and platforms type `!about`"):

    def __init__(self, client):
        self.client = client
        self.db = self.client.firestoreDb
        self.platforms = {
            "Origin",
            "Uplay",
            "Epic",
            "GOG",
            "Rockstar",
            "Steam",
        }
        self.regions = {
            "RF",
            "US",
            "EU",
            "AS",
            "ME",
            "ROW",
            "ex.",
        }

    @commands.command(brief="add a key into the database for others (use DM)")
    # async def addkey(self, ctx, game_title, platform=None, region=None, key=None):
    async def addkey(self, ctx):

        # split into an array to remove parts
        # delete message to prevent other users from using before if added to the public channel
        # we'll delete the message if the channel is not of type private/dm. Keys should not be publicly exposed.
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.message.delete()            

        # cleanse the input from the key and cmd to leave the game title including the region and platform
        args = ctx.message.content.split(" ")
        key = args.pop(-1) #remove key from array
        cmd = args.pop(0) # remove the cmd from the array

        gameTitle = " ".join(args)
        gameTitle = gameTitle.replace('[','').replace(']','')

        # a check for key format correctness
        match = re.search("([a-zA-Z0-9]){3,}-{1}", key) # regex matches AAAAA-12345-C3A3F, most keys are expected to have this format
        if not match:
            await ctx.author.send(f"The format for the cd-key is incorrect. You entered {key}. Please try using the command again, here's an example - _!addkey Battlefield V AAAAA-BBBBB-CCCCC.")
            return

        await ctx.author.send("one moment, adding key...")

        # get the key document on firebase
        key_doc = self.db.collection("game_list").document(gameTitle).collection("keys").document(key)
        doc = key_doc.get()

        # regex to check the format with square brackets
        # my_regex = re.compile(r'\[([^][]+)\]')
        # args = my_regex.findall(ctx.message.content)
        # if len(args) != 4:
        #     await ctx.channel.send("**A parameter is missing.** Check what was entered and use the following format i.e. !addkey [GameTitle] [Platform] [Region] key")

        if not doc.exists:
            # add exists field to game
            self.db.collection("game_list").document(gameTitle).set({"exists": 1})

            # add key to game
            key_doc.set({
                "key" : key,
                "user" : ctx.author.name
            })

            # add key to user's profile as a game they've contributed
            user_doc = self.db.collection("user").document(f"{ctx.author.id}").collection(gameTitle).document(key)
            user_doc.set({
                "key" : key,
                "user" : ctx.author.name,
            })

            output = f"Thanks for giving back to the community {ctx.author.name}."
            await ctx.author.send(output)
        else:   
            output = f"The key already exists. You may try again and add unique key."
            await ctx.author.send(output)

def setup(client):
    client.add_cog(AddKey(client))