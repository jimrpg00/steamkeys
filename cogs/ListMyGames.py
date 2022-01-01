import discord
from discord.ext import commands

class ListMyGames(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db = self.client.firestoreDb

    @commands.command(brief="Lists games you have already acquired")
    async def listmygames(self, ctx):
        await ctx.author.send("One moment, grabbing a list of games.")
        keys_refs = self.db.collection('user').document(str(ctx.author.id)).collection('keys').stream()
        appendedGamesStr = ""
        
        if not (keys_refs):
            appendedGamesStr = "Your game list is empty."
        else:
            for game in keys_refs:
                appendedGamesStr = appendedGamesStr + (f'{game.id}\n')
            await ctx.channel.send(f"""```{appendedGamesStr}```""")

def setup(client):
    client.add_cog(ListMyGames(client))