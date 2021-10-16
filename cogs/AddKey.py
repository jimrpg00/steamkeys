import re
import discord
from discord.ext import commands

class AddKey(commands.Cog, description="When adding keys, create a DM so the key is not revealed in the thread. (direct message SteamKeysBot by right clicking on the name in the member list).\n\nThis command requires at mininmum the game title and game key. Platform and region are optional. Please keep in mind the ORDER of the arguments that follow the command -\n\n !addkey _title_ [_platform_] [_region_] _key_\n\nHere's an example with ALL arguments supplied -\n`!addkey Red Dead Redemption 2 [Rockstar] [ROW ex. Japan] AAAAA-BBBBB-CCCCC`\n\nAnother example with only region\n`!addkey Red Dead Redemption 2 [ROW ex. Japan] AAAAA-BBBBB-CCCCC`\n\nAnother example with only platform\n`!addkey Red Dead Redemption 2 [Rockstar] AAAAA-BBBBB-CCCCC`\n\nAnd finally another one with just the key and title\n`!addkey Red Dead Redemption 2 AAAAA-BBBBB-CCCCC`\n\nFor more information about regions and platforms type `!about`"):

    def __init__(self, client):
        self.client = client
        self.db = self.client.firestoreDb

    @commands.command(brief="add a key into the database for others (use DM)")
    async def addkey(self, ctx, game_title, platform, region, key):
        # print(game_title, platform, region, key)
        print(ctx.message.content)
        #regex to check the format
        argList = ctx.message.content.split(' ')
        # save and remove the command from argList
        command = argList.pop(0) # unused

        key = argList.pop(-1) # check if key is correct length
        # argList should be stripped down without the command and key
        match = re.search("([a-zA-Z0-9]){3,}-{1}", key) #matches AAAAA-12345-C3A3F, most keys are expected to have this format
        if not match:
            await ctx.channel.send(f"The format for the cd-key is incorrect. You entered {key}. Please try using the command again, here's an example - _!addkey Battlefield V AAAAA-BBBBB-CCCCC_.")
            return 

        gameTitle = ' '.join(argList)

        key_doc = self.db.collection("game_list").document(gameTitle).collection("keys").document(key)
        doc = key_doc.get()
        if not doc.exists:
            # add key
            key_doc.set({
                "key" : key,
                "user" : ctx.author.name
            })

            # add key to user's profile
            user_doc = self.db.collection("user").document(f"{ctx.author.id}").collection(uppercaseGameTitle).document(key)
            user_doc.set({
                "key" : key,
                "user" : ctx.author.name,
            })

            # add key to game list
            self.db.collection("game_list").document(gameTitle).collection("keys").document(key).set({"exists" : 1})


            output = f"Thanks for giving back to the community {ctx.author.name}. {gameTitle} key was received for another."
            await ctx.channel.send(output)
        else:   
            output = f"The key already exists. Please remember to only use valid keys. You may try again and add unique key."
            await ctx.channel.send(output)
        await ctx.message.delete()

def setup(client):
    client.add_cog(AddKey(client))

