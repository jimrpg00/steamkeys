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
    async def addkey(self, ctx, game_title, platform=None, region=None, key=None):
        
        if not game_title or not region or not platform or not key:
            regionsList = self.regions.join(" ")
            platformList = self.platforms.join(" ")
            await ctx.channel.send("A parameter is missing. Please check what was entered and use the following format i.e. !addkey [GameTitle] [Platform] [Region] [key]")
            await ctx.channel.send(f"{regionsList}")
            await ctx.channel.send(platformList)
            return

        #regex to check the format
        my_regex = re.compile(r'\[([^][]+)\]')
        args = my_regex.findall(ctx.message.content)
        if len(args) != 4:
            await ctx.channel.send("**A parameter is missing.** Check what was entered and use the following format i.e. !addkey [GameTitle] [Platform] [Region] key")
            await ctx.channel.send("""Use on of the following for the region
US: US
Europe: EU
AS: Asia
ME: Middle East
ROW: Rest of World
ex. = except""")
            await ctx.channel.send("""Use one of the following for the platform
Steam: Steam
Origin: EA Origin
Uplay: Ubisoft Uplay
Epic: Epic Games
GOG: GOG
Rockstar: Rockstar
Others: label as needed""")
            return

        # separate args into their respective variables
        key = args.pop(-1)
        region = args.pop(-1)
        platform = args.pop(-1)

        # check region and platform match the list
        r = region.split(" ")
        if bool(set(r).difference(self.regions)):
            await ctx.channel.send("**The region is incorrect.** Check what was entered and use the following format i.e. !addkey [GameTitle] [Platform] [Region] key")
            await ctx.channel.send("""Use on of the following for the region
US: US
Europe: EU
AS: Asia
ME: Middle East
ROW: Rest of World
ex. = except""")
            await ctx.channel.send("i.e. [US] or [ROW ex. ME]")
            return

        if platform not in self.platforms:
            await ctx.channel.send("**The platform is incorrect.** Check what was entered and use the following format i.e. !addkey [GameTitle] [Platform] [Region] key")
            await ctx.channel.send("""Use one of the following for the platform
Steam: Steam
Origin: EA Origin
Uplay: Ubisoft Uplay
Epic: Epic Games
GOG: GOG
Rockstar: Rockstar
Others: label as needed""")
            await ctx.channel.send("i.e. [Origin] or [Steam]")
            return

        # checks complete
        # save and remove the command from argList
        await ctx.channel.send("one moment, adding key...")
        # join remaining words together
        gameTitle = ' '.join(args)
        # reformat title
        gameTitle = f"{gameTitle} {platform} {region}"

        # ensure the key is correct otherwise warn the user and exit early
        match = re.search("([a-zA-Z0-9]){3,}-{1}", key) # regex matches AAAAA-12345-C3A3F, most keys are expected to have this format
        if not match:
            await ctx.channel.send(f"The format for the cd-key is incorrect. You entered {key}. Please try using the command again, here's an example - _!addkey Battlefield V AAAAA-BBBBB-CCCCC_.")
            return

        # get the key document on firebase
        key_doc = self.db.collection("game_list").document(gameTitle).collection("keys").document(key)
        doc = key_doc.get()

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
            await ctx.channel.send(output)
        else:   
            output = f"The key already exists. You may try again and add unique key."
            await ctx.channel.send(output)
        await ctx.message.delete()

  
def setup(client):
    client.add_cog(AddKey(client))

