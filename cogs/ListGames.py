import discord
from discord.ext import commands

class ListGames(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def listgames(self, ctx):
        print("list games from cogs")
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

def setup(client):
    client.add_cog(ListGames(client))